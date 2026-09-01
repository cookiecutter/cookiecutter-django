import io
import os
import sys
from urllib.parse import unquote_plus

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))

import boto3
from PIL import Image, ImageOps

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("AWS_ENDPOINT_URL") or None,
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)


def _optimized_key(key: str) -> str:
    if key.startswith("media/avatars/source/"):
        return key.replace("media/avatars/source/", "media/avatars/optimized/", 1)
    return key.replace("avatars/", "avatars/optimized/", 1)


def _thumbnail_key(key: str) -> str:
    optimized = _optimized_key(key)
    name = optimized.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    return f"media/avatars/thumbnail/{name}.webp"


def _save_image(image: Image.Image, format_name: str, quality: int) -> bytes:
    output = io.BytesIO()
    image.save(
        output,
        format=format_name,
        quality=quality,
        optimize=True,
        progressive=format_name == "JPEG",
    )
    return output.getvalue()


def lambda_handler(event, context):
    bucket = event["bucket"]
    key = unquote_plus(event["key"])
    response = s3.get_object(Bucket=bucket, Key=key)
    with Image.open(io.BytesIO(response["Body"].read())) as source:
        source = ImageOps.exif_transpose(source)
        if source.mode not in ("RGB", "RGBA"):
            source = source.convert("RGBA" if "transparency" in source.info else "RGB")

        optimized_key = _optimized_key(key)
        source_format = "PNG" if source.format == "PNG" else "JPEG"
        content_type = "image/png" if source_format == "PNG" else "image/jpeg"
        optimized = _save_image(source, source_format, 88)
        s3.put_object(
            Bucket=bucket,
            Key=optimized_key,
            Body=optimized,
            ContentType=content_type,
            CacheControl="public,max-age=31536000,immutable",
        )

        thumbnail = source.copy()
        thumbnail.thumbnail((200, 200), Image.Resampling.LANCZOS)
        if thumbnail.mode not in ("RGB", "RGBA"):
            thumbnail = thumbnail.convert("RGBA")
        thumbnail_bytes = _save_image(thumbnail, "WEBP", 82)
        thumbnail_key = _thumbnail_key(key)
        s3.put_object(
            Bucket=bucket,
            Key=thumbnail_key,
            Body=thumbnail_bytes,
            ContentType="image/webp",
            CacheControl="public,max-age=31536000,immutable",
        )

    return {
        "bucket": bucket,
        "source_key": key,
        "optimized_key": optimized_key,
        "thumbnail_key": thumbnail_key,
    }
