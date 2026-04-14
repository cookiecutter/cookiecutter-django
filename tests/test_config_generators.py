"""
Tests for the config_generators module.

Tests cover:
- Secret generation
- Flag operation creation
- Dependency operation creation
- Warning message generation
"""

from hooks.config_generators import SecretConfig
from hooks.config_generators import create_flag_operations
from hooks.config_generators import generate_random_string
from hooks.config_generators import generate_random_user
from hooks.config_generators import get_warning_messages


class TestGenerateRandomString:
    """Tests for generate_random_string function."""

    def test_generate_with_digits(self):
        """Test generating string with digits."""
        result = generate_random_string(length=10, using_digits=True)

        if result is not None:  # May be None if SystemRandom not available
            assert len(result) == 10
            assert any(c.isdigit() for c in result)

    def test_generate_with_letters(self):
        """Test generating string with letters."""
        result = generate_random_string(length=10, using_ascii_letters=True)

        if result is not None:
            assert len(result) == 10
            assert any(c.isalpha() for c in result)

    def test_generate_with_punctuation(self):
        """Test generating string with punctuation."""
        result = generate_random_string(length=20, using_punctuation=True)

        if result is not None:
            assert len(result) == 20
            # Should not contain problematic characters
            assert "'" not in result
            assert '"' not in result
            assert "\\" not in result
            assert "$" not in result

    def test_generate_combined(self):
        """Test generating string with all character types."""
        result = generate_random_string(
            length=50,
            using_digits=True,
            using_ascii_letters=True,
            using_punctuation=True,
        )

        if result is not None:
            assert len(result) == 50


class TestGenerateRandomUser:
    """Tests for generate_random_user function."""

    def test_generate_user(self):
        """Test generating a random user."""
        user = generate_random_user()

        assert isinstance(user, str)
        assert len(user) > 0


class TestSecretConfig:
    """Tests for SecretConfig dataclass."""

    def test_generate_debug_config(self):
        """Test generating debug configuration."""
        config = SecretConfig.generate(debug=True)

        assert config.django_secret_key == "debug-secret-key-not-for-production"
        assert config.django_admin_url == "admin/"
        assert config.postgres_user == "debug"
        assert config.postgres_password == "debug"
        assert config.celery_flower_user == "debug"
        assert config.celery_flower_password == "debug"

    def test_generate_production_config(self):
        """Test generating production configuration."""
        config = SecretConfig.generate(debug=False)

        # Should generate random values
        assert config.django_secret_key != "debug-secret-key-not-for-production"
        assert len(config.django_secret_key) == 64
        assert "/" in config.django_admin_url
        assert len(config.postgres_user) > 0
        assert len(config.postgres_password) == 64


class TestCreateFlagOperations:
    """Tests for create_flag_operations function."""

    def test_creates_multiple_operations(self):
        """Test that multiple operations are created."""
        config = SecretConfig.generate(debug=True)
        operations = create_flag_operations(config)

        # Should create operations for:
        # - Production django envs (2 flags)
        # - Local postgres envs (2 flags)
        # - Production postgres envs (2 flags)
        # - Local django envs (2 flags - celery)
        # - Production django envs (2 flags - celery)
        # - Local settings (1 flag)
        # - Test settings (1 flag)
        assert len(operations) >= 10

    def test_operations_are_set_flag_type(self):
        """Test that all operations are SetFlagOperation."""
        from hooks.operations import SetFlagOperation

        config = SecretConfig.generate(debug=True)
        operations = create_flag_operations(config)

        for op in operations:
            assert isinstance(op, SetFlagOperation)

    def test_django_secret_key_operations(self):
        """Test that Django secret key operations are created."""
        from hooks.operations import SetFlagOperation

        config = SecretConfig.generate(debug=True)
        operations = create_flag_operations(config)

        # Find operations for Django secret key
        secret_key_ops = [
            op for op in operations if isinstance(op, SetFlagOperation) and op.flag == "!!!SET DJANGO_SECRET_KEY!!!"
        ]

        assert len(secret_key_ops) >= 2  # At least production and settings files


class TestGetWarningMessages:
    """Tests for get_warning_messages function."""

    def test_no_warnings_for_docker_setup(self):
        """Test no warnings for Docker setup."""
        context = {
            "use_docker": "y",
            "use_heroku": "n",
            "cloud_provider": "AWS",
            "keep_local_envs_in_vcs": "y",
        }

        warnings = get_warning_messages(context)

        # Should have no warnings
        assert len(warnings) == 0

    def test_warning_for_no_cloud_no_docker(self):
        """Test warning when no cloud provider and no Docker."""
        context = {
            "use_docker": "n",
            "use_heroku": "n",
            "cloud_provider": "None",
            "keep_local_envs_in_vcs": "y",
        }

        warnings = get_warning_messages(context)

        # Should have warning about media files
        assert len(warnings) >= 1
        assert any("cloud providers" in w for w in warnings)

    def test_warning_for_envs_without_docker_heroku(self):
        """Test warning for keeping envs without Docker or Heroku."""
        context = {
            "use_docker": "n",
            "use_heroku": "n",
            "cloud_provider": "None",
            "keep_local_envs_in_vcs": "y",
        }

        warnings = get_warning_messages(context)

        # Should have warning about .env files
        assert any(".env(s)" in w for w in warnings)


class TestIntegration:
    """Integration tests for config generators."""

    def test_full_config_generation(self):
        """Test full configuration generation flow."""
        # Generate production config
        config = SecretConfig.generate(debug=False)

        # Create flag operations
        operations = create_flag_operations(config)

        # Verify all operations are valid
        for op in operations:
            assert op.file_path is not None
            assert op.flag is not None
            assert op.value is not None

        # Check that we have operations for all required flags
        flags = [op.flag for op in operations]
        assert "!!!SET DJANGO_SECRET_KEY!!!" in flags
        assert "!!!SET DJANGO_ADMIN_URL!!!" in flags
        assert "!!!SET POSTGRES_USER!!!" in flags
        assert "!!!SET POSTGRES_PASSWORD!!!" in flags
        assert "!!!SET CELERY_FLOWER_USER!!!" in flags
        assert "!!!SET CELERY_FLOWER_PASSWORD!!!" in flags
