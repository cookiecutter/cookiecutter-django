from __future__ import annotations

import json
from io import BytesIO
from pathlib import PurePosixPath

from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import close_old_connections
from django.db import transaction

from {{cookiecutter.project_slug}}.aws import aws_client

from .models import User


def _storage_key(name: str) -> str:
    location = str(getattr(settings, "AWS_S3_LOCATION", "media")).strip("/")
    return f"{location}/{name.lstrip('/')}" if location else name.lstrip("/")


def _relative_name(key: str) -> str:
    location = str(getattr(settings, "AWS_S3_LOCATION", "media")).strip("/")
    prefix = f"{location}/"
    return key[len(prefix):] if location and key.startswith(prefix) else key


def _fallback_optimize(source_name: str) -> tuple[str, str]:
    from PIL import Image
    from PIL import ImageOps

    with default_storage.open(source_name, "rb") as source_file:
        image = ImageOps.exif_transpose(Image.open(source_file))
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA" if "transparency" in image.info else "RGB")

        suffix = PurePosixPath(source_name).suffix.lower()
        source_format = "PNG" if suffix == ".png" else "JPEG"
        stem = PurePosixPath(source_name).stem
        optimized_name = f"avatars/optimized/{stem}.{source_format.lower()}"
        thumb_name = f"avatars/thumbnail/{stem}.webp"

        optimized_buffer = BytesIO()
        image.save(
            optimized_buffer,
            format=source_format,
            quality=88,
            optimize=True,
            progressive=source_format == "JPEG",
        )
        optimized_buffer.seek(0)
        optimized_saved = default_storage.save(optimized_name, ContentFile(optimized_buffer.read()))

        thumbnail = image.copy()
        thumbnail.thumbnail((200, 200), Image.Resampling.LANCZOS)
        if thumbnail.mode not in ("RGB", "RGBA"):
            thumbnail = thumbnail.convert("RGBA")
        thumb_buffer = BytesIO()
        thumbnail.save(thumb_buffer, format="WEBP", quality=82, method=6)
        thumb_buffer.seek(0)
        thumb_saved = default_storage.save(thumb_name, ContentFile(thumb_buffer.read()))

    return optimized_saved, thumb_saved


def _invoke_lambda(bucket: str, key: str) -> tuple[str, str]:
    function_name = str(getattr(settings, "AWS_AVATAR_LAMBDA_FUNCTION_NAME", "") or "").strip()
    if not function_name:
        raise RuntimeError("AWS avatar Lambda is not configured.")
    response = aws_client("lambda").invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        Payload=json.dumps({"bucket": bucket, "key": key}).encode(),
    )
    payload = json.loads(response["Payload"].read().decode())
    if response.get("FunctionError") or "optimized_key" not in payload or "thumbnail_key" not in payload:
        raise RuntimeError(f"Avatar Lambda failed: {payload}")
    return str(payload["optimized_key"]), str(payload["thumbnail_key"])


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=300,
    retry_kwargs={"max_retries": 8},
)
def process_avatar(self, user_id: int, source_name: str) -> None:
    close_old_connections()
    user = User.objects.get(pk=user_id)
    if not user.avatar or user.avatar.name != source_name:
        return

    bucket = str(settings.AWS_STORAGE_BUCKET_NAME)
    source_key = _storage_key(source_name)
    try:
        optimized_key, thumbnail_key = _invoke_lambda(bucket, source_key)
        optimized_name = _relative_name(optimized_key)
        thumbnail_name = _relative_name(thumbnail_key)
    except Exception:
        optimized_name, thumbnail_name = _fallback_optimize(source_name)

    with transaction.atomic():
        user = User.objects.select_for_update().get(pk=user_id)
        if not user.avatar or user.avatar.name != source_name:
            return
        old_name = user.avatar.name
        user.avatar.name = optimized_name
        user.avatar_thumbnail.name = thumbnail_name
        user.save(update_fields=["avatar", "avatar_thumbnail"])
        if old_name and old_name != optimized_name and default_storage.exists(old_name):
            default_storage.delete(old_name)


@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()
