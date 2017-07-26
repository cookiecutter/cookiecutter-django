from unittest.mock import patch, PropertyMock
import unittest
import entrypoint

class TestEntrypoint(unittest.TestCase):

    """
    We test that the entry point script works.
    """
    def setUp(self):
        self.prop = 'test'

    def test_exports(self):
        with patch.dict(entrypoint.os.environ, {'newkey': 'newvalue'}, clear=True):
            entrypoint.exports()
            self.assertTrue(entrypoint.os.environ['REDIS_URL'])
            self.assertTrue(entrypoint.os.environ['CELERY_BROKER_URL'])
            self.assertTrue(entrypoint.os.environ['newkey'])

    @patch('entrypoint.psycopg2.connect')
    def test_pingpost(self, mockConn):
        """
        We must assert that psycopg2 conn is called
        """
        with patch.dict(entrypoint.os.environ, {
            'POSTGRES_USER': 'newvalue',
            'POSTGRES_PASSWORD': 'test'}, clear=True):
            entrypoint.main(('dir',))
            self.assertTrue(entrypoint.os.environ['DATABASE_URL'])
        self.assertTrue(mockConn.called)


if __name__ == '__main__':
    unittest.main()
