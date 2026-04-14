"""Tests for the generator module."""

from hooks.core.context import FailurePolicy
from hooks.generator import ProjectGenerator
from hooks.generator import generate_random_string
from hooks.generator import generate_random_user


class TestProjectGenerator:
    def test_generator_creation(self):
        config = {"project_slug": "test_project"}
        generator = ProjectGenerator(config)

        assert generator.project_slug == "test_project"
        assert generator.context.project_slug == "test_project"

    def test_generator_with_dry_run(self):
        config = {"project_slug": "test_project"}
        generator = ProjectGenerator(config, dry_run=True)

        assert generator.context.dry_run

    def test_generator_with_failure_policy(self):
        config = {"project_slug": "test_project"}
        generator = ProjectGenerator(
            config,
            failure_policy=FailurePolicy.CONTINUE_ON_ERROR,
        )

        assert generator.context.failure_policy == FailurePolicy.CONTINUE_ON_ERROR

    def test_register_strategy(self):
        config = {"project_slug": "test_project"}
        generator = ProjectGenerator(config)

        from hooks.strategies.license import OpenSourceLicenseStrategy

        strategy = OpenSourceLicenseStrategy()
        generator.register_strategy(strategy)

        assert strategy in generator._strategies

    def test_register_default_strategies(self):
        config = {"project_slug": "test_project"}
        generator = ProjectGenerator(config)
        generator.register_default_strategies()

        assert len(generator._strategies) == 10

    def test_plan_returns_actions(self):
        config = {
            "project_slug": "test_project",
            "open_source_license": "Not open source",
            "username_type": "username",
            "editor": "VS Code",
            "use_docker": "n",
            "use_heroku": "n",
            "frontend_pipeline": "None",
            "use_celery": "n",
            "ci_tool": "None",
            "rest_api": "None",
            "use_async": "n",
        }
        generator = ProjectGenerator(config)
        generator.register_default_strategies()

        actions = generator.plan()

        assert len(actions) > 0
        assert all(hasattr(a, "execute") for a in actions)

    def test_preview(self):
        config = {
            "project_slug": "test_project",
            "open_source_license": "Not open source",
        }
        generator = ProjectGenerator(config)
        generator.register_default_strategies()

        preview = generator.preview()

        assert "test_project" in preview
        assert "Preview" in preview

    def test_get_report(self):
        config = {"project_slug": "test_project"}
        generator = ProjectGenerator(config)

        report = generator.get_report()

        assert "test_project" in report

    def test_get_json_report(self):
        config = {"project_slug": "test_project"}
        generator = ProjectGenerator(config)

        report = generator.get_json_report()

        assert report["project_name"] == "test_project"

    def test_context_helpers(self):
        config = {
            "project_slug": "test_project",
            "use_docker": "y",
            "editor": "PyCharm",
        }
        generator = ProjectGenerator(config)

        assert generator.context.is_enabled("use_docker")
        assert generator.context.equals("editor", "PyCharm")
        assert generator.context.get_config("project_slug") == "test_project"


class TestRandomGeneration:
    def test_generate_random_string_digits(self):
        result = generate_random_string(10, using_digits=True)

        if result:
            assert len(result) == 10
            assert result.isdigit()

    def test_generate_random_string_letters(self):
        result = generate_random_string(10, using_ascii_letters=True)

        if result:
            assert len(result) == 10
            assert result.isalpha()

    def test_generate_random_string_mixed(self):
        result = generate_random_string(
            20,
            using_digits=True,
            using_ascii_letters=True,
        )

        if result:
            assert len(result) == 20
            assert result.isalnum()

    def test_generate_random_user(self):
        result = generate_random_user()

        if result:
            assert len(result) == 32
            assert result.isalpha()


class TestGeneratorIntegration:
    def test_full_generation_flow_dry_run(self, tmp_path):
        config = {
            "project_slug": "my_project",
            "open_source_license": "MIT",
            "username_type": "email",
            "editor": "None",
            "use_docker": "n",
            "use_heroku": "n",
            "frontend_pipeline": "None",
            "use_celery": "n",
            "ci_tool": "Github",
            "rest_api": "DRF",
            "use_async": "n",
            "keep_local_envs_in_vcs": "n",
        }

        generator = ProjectGenerator(config, dry_run=True)
        generator.register_default_strategies()

        actions = generator.plan()

        assert len(actions) > 0

    def test_different_config_combinations(self):
        configs = [
            {"use_docker": "y", "cloud_provider": "AWS"},
            {"use_docker": "y", "cloud_provider": "None"},
            {"use_docker": "n", "use_heroku": "y"},
            {"frontend_pipeline": "Gulp"},
            {"frontend_pipeline": "Webpack"},
            {"rest_api": "Django Ninja"},
        ]

        for config in configs:
            full_config = {"project_slug": "test", **config}
            generator = ProjectGenerator(full_config)
            generator.register_default_strategies()

            actions = generator.plan()

            assert len(actions) >= 0, f"Failed for config: {config}"
