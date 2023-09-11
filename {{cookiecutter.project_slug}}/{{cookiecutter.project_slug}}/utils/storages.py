{% if cookiecutter.cloud_provider == 'AWS' -%}
from storages.backends.s3 import S3Storage


class StaticRootS3Storage(S3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Storage(S3Storage):
    location = "media"
    file_overwrite = False
{%- elif cookiecutter.cloud_provider == 'GCP' -%}
from storages.backends.gcloud import GoogleCloudStorage


class StaticRootGoogleCloudStorage(GoogleCloudStorage):
    location = "static"
    default_acl = "publicRead"


class MediaRootGoogleCloudStorage(GoogleCloudStorage):
    location = "media"
    file_overwrite = False
{%- elif cookiecutter.cloud_provider == 'Azure' -%}
from storages.backends.azure_storage import AzureStorage


class StaticRootAzureStorage(AzureStorage):
    location = "static"


class MediaRootAzureStorage(AzureStorage):
    location = "media"
    file_overwrite = False
{%- endif %}
