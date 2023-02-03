from webpack_loader.loader import WebpackLoader


class DummyWebpackLoader(WebpackLoader):
    def get_bundle(self, _bundle_name: str):
        """
        Dummy loader to run tests.

        Needed to run tests without webpack stats file nor bundle built.
        """
        return [
            {
                "name": "test.bundle.js",
                "url": "http://localhost/static/bundles/test.bundle.js",
            },
        ]
