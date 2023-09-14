{% if cookiecutter.cloud_provider == 'AWS' -%}
from storages.backends.s3 import S3Storage


class StaticS3Storage(S3Storage):
    location = "static"
    default_acl = "public-read"


class MediaS3Storage(S3Storage):
    location = "media"
    file_overwrite = False
{%- elif cookiecutter.cloud_provider == 'GCP' -%}
from storages.backends.gcloud import GoogleCloudStorage


class StaticGoogleCloudStorage(GoogleCloudStorage):
    location = "static"
    default_acl = "publicRead"


class MediaGoogleCloudStorage(GoogleCloudStorage):
    location = "media"
    file_overwrite = False
{%- elif cookiecutter.cloud_provider == 'Azure' -%}
from storages.backends.azure_storage import AzureStorage


class StaticAzureStorage(AzureStorage):
    location = "static"


class MediaAzureStorage(AzureStorage):
    location = "media"
    file_overwrite = False
{%- endif %}
