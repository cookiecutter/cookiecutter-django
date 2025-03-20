from storages.backends.azure_storage import AzureStorage


class StaticAzureStorage(AzureStorage):
    location = "static"


class MediaAzureStorage(AzureStorage):
    location = "media"
    file_overwrite = False
