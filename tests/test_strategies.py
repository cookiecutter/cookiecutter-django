"""
Tests for the strategies module.

Tests cover:
- Strategy applicability logic
- Operation generation
- Strategy registry
- Integration with ProjectContext
"""

import json
from pathlib import Path

import pytest

from hooks.strategies import (
    ProjectContext,
    ProjectStrategy,
    registry,
    NotOpenSourceStrategy,
    NotGPLv3Strategy,
    UsernameAuthStrategy,
    NonPyCharmStrategy,
    DockerStrategy,
    NonDockerStrategy,
    NonHerokuStrategy,
    NoFrontendPipelineStrategy,
    GulpStrategy,
    WebpackStrategy,
    NonCeleryStrategy,
    NoRestAPIStrategy,
    DRFStrategy,
    NinjaStrategy,
    NonAsyncStrategy,
)


class TestProjectContext:
    """Tests for ProjectContext."""
    
    def test_context_creation(self):
        """Test creating a project context."""
        context = ProjectContext(
            project_slug="my_project",
            open_source_license="MIT",
            username_type="email",
            editor="VS Code",
            use_docker="y",
            cloud_provider="AWS",
            use_heroku="n",
            frontend_pipeline="Webpack",
            use_celery="y",
            use_async="y",
            ci_tool="Github",
            rest_api="DRF",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        assert context.project_slug == "my_project"
        assert context.is_yes(context.use_docker) is True
        assert context.is_yes(context.use_heroku) is False
    
    def test_is_yes_variations(self):
        """Test is_yes with various inputs."""
        context = ProjectContext(
            project_slug="test",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="Y",  # uppercase
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="N",  # uppercase
            use_async="y",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        assert context.is_yes("y") is True
        assert context.is_yes("Y") is True
        assert context.is_yes("n") is False
        assert context.is_yes("N") is False


class TestNotOpenSourceStrategy:
    """Tests for NotOpenSourceStrategy."""
    
    def test_applies_to_not_open_source(self):
        """Test strategy applies to not open source."""
        context = ProjectContext(
            project_slug="test",
            open_source_license="Not open source",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = NotOpenSourceStrategy()
        assert strategy.applies_to(context) is True
        
        ops = strategy.get_operations(context)
        assert len(ops) == 2
        assert any("CONTRIBUTORS.txt" in op.describe() for op in ops)
        assert any("LICENSE" in op.describe() for op in ops)
    
    def test_does_not_apply_to_open_source(self):
        """Test strategy does not apply to open source."""
        context = ProjectContext(
            project_slug="test",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = NotOpenSourceStrategy()
        assert strategy.applies_to(context) is False


class TestNotGPLv3Strategy:
    """Tests for NotGPLv3Strategy."""
    
    def test_applies_to_non_gpl(self):
        """Test strategy applies to non-GPL licenses."""
        context = ProjectContext(
            project_slug="test",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = NotGPLv3Strategy()
        assert strategy.applies_to(context) is True
    
    def test_does_not_apply_to_gpl(self):
        """Test strategy does not apply to GPLv3."""
        context = ProjectContext(
            project_slug="test",
            open_source_license="GPLv3",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = NotGPLv3Strategy()
        assert strategy.applies_to(context) is False


class TestUsernameAuthStrategy:
    """Tests for UsernameAuthStrategy."""
    
    def test_applies_to_username_auth(self):
        """Test strategy applies to username auth."""
        context = ProjectContext(
            project_slug="myproject",
            open_source_license="MIT",
            username_type="username",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = UsernameAuthStrategy()
        assert strategy.applies_to(context) is True
        
        ops = strategy.get_operations(context)
        assert len(ops) == 2
        assert any("managers.py" in op.describe() for op in ops)


class TestNonPyCharmStrategy:
    """Tests for NonPyCharmStrategy."""
    
    def test_applies_to_non_pycharm(self):
        """Test strategy applies to non-PyCharm editors."""
        context = ProjectContext(
            project_slug="test",
            open_source_license="MIT",
            username_type="email",
            editor="VS Code",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = NonPyCharmStrategy()
        assert strategy.applies_to(context) is True
    
    def test_does_not_apply_to_pycharm(self):
        """Test strategy does not apply to PyCharm."""
        context = ProjectContext(
            project_slug="test",
            open_source_license="MIT",
            username_type="email",
            editor="PyCharm",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = NonPyCharmStrategy()
        assert strategy.applies_to(context) is False


class TestDockerStrategy:
    """Tests for DockerStrategy."""
    
    def test_applies_to_docker(self):
        """Test strategy applies to Docker."""
        context = ProjectContext(
            project_slug="test",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="y",
            cloud_provider="AWS",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = DockerStrategy()
        assert strategy.applies_to(context) is True
        
        ops = strategy.get_operations(context)
        # Should delete utility and nginx (with cloud provider)
        assert len(ops) >= 1
    
    def test_removes_nginx_with_cloud_provider(self):
        """Test that nginx is removed when using cloud provider."""
        context = ProjectContext(
            project_slug="test",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="y",
            cloud_provider="AWS",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = DockerStrategy()
        ops = strategy.get_operations(context)
        
        assert any("nginx" in op.describe() for op in ops)


class TestNonDockerStrategy:
    """Tests for NonDockerStrategy."""
    
    def test_applies_to_non_docker(self):
        """Test strategy applies to non-Docker."""
        context = ProjectContext(
            project_slug="test",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = NonDockerStrategy()
        assert strategy.applies_to(context) is True
        
        ops = strategy.get_operations(context)
        assert len(ops) >= 4  # Multiple files and directories
        assert any(".devcontainer" in op.describe() for op in ops)
        assert any("compose" in op.describe() for op in ops)


class TestNonHerokuStrategy:
    """Tests for NonHerokuStrategy."""
    
    def test_applies_to_non_heroku(self):
        """Test strategy applies to non-Heroku."""
        context = ProjectContext(
            project_slug="test",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = NonHerokuStrategy()
        assert strategy.applies_to(context) is True
        
        ops = strategy.get_operations(context)
        assert any("Procfile" in op.describe() for op in ops)


class TestNoFrontendPipelineStrategy:
    """Tests for NoFrontendPipelineStrategy."""
    
    def test_applies_to_no_pipeline(self):
        """Test strategy applies to no frontend pipeline."""
        context = ProjectContext(
            project_slug="myproject",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = NoFrontendPipelineStrategy()
        assert strategy.applies_to(context) is True
        
        ops = strategy.get_operations(context)
        assert len(ops) >= 4
        assert any("gulpfile" in op.describe() for op in ops)
        assert any("webpack" in op.describe() for op in ops)
    
    def test_applies_to_django_compressor(self):
        """Test strategy applies to Django Compressor."""
        context = ProjectContext(
            project_slug="myproject",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="Django Compressor",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = NoFrontendPipelineStrategy()
        assert strategy.applies_to(context) is True


class TestGulpStrategy:
    """Tests for GulpStrategy."""
    
    def test_applies_to_gulp(self):
        """Test strategy applies to Gulp."""
        context = ProjectContext(
            project_slug="myproject",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="Gulp",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = GulpStrategy()
        assert strategy.applies_to(context) is True
        
        ops = strategy.get_operations(context)
        # Should delete webpack and modify package.json
        assert len(ops) >= 3


class TestWebpackStrategy:
    """Tests for WebpackStrategy."""
    
    def test_applies_to_webpack(self):
        """Test strategy applies to Webpack."""
        context = ProjectContext(
            project_slug="myproject",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="Webpack",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = WebpackStrategy()
        assert strategy.applies_to(context) is True
        
        ops = strategy.get_operations(context)
        # Should delete gulpfile and modify package.json
        assert len(ops) >= 2


class TestNonCeleryStrategy:
    """Tests for NonCeleryStrategy."""
    
    def test_applies_to_non_celery(self):
        """Test strategy applies to non-Celery."""
        context = ProjectContext(
            project_slug="myproject",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = NonCeleryStrategy()
        assert strategy.applies_to(context) is True
        
        ops = strategy.get_operations(context)
        assert len(ops) == 3
        assert any("celery_app.py" in op.describe() for op in ops)


class TestNoRestAPIStrategy:
    """Tests for NoRestAPIStrategy."""
    
    def test_applies_to_no_rest_api(self):
        """Test strategy applies to no REST API."""
        context = ProjectContext(
            project_slug="myproject",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = NoRestAPIStrategy()
        assert strategy.applies_to(context) is True
        
        ops = strategy.get_operations(context)
        assert len(ops) >= 4


class TestDRFStrategy:
    """Tests for DRFStrategy."""
    
    def test_applies_to_drf(self):
        """Test strategy applies to DRF."""
        context = ProjectContext(
            project_slug="myproject",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="DRF",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = DRFStrategy()
        assert strategy.applies_to(context) is True
        
        ops = strategy.get_operations(context)
        assert len(ops) == 2
        # Should remove Ninja files
        assert any("api.py" in op.describe() for op in ops)


class TestNinjaStrategy:
    """Tests for NinjaStrategy."""
    
    def test_applies_to_ninja(self):
        """Test strategy applies to Django Ninja."""
        context = ProjectContext(
            project_slug="myproject",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="Django Ninja",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = NinjaStrategy()
        assert strategy.applies_to(context) is True
        
        ops = strategy.get_operations(context)
        assert len(ops) == 2
        # Should remove DRF files
        assert any("api_router.py" in op.describe() for op in ops)


class TestNonAsyncStrategy:
    """Tests for NonAsyncStrategy."""
    
    def test_applies_to_non_async(self):
        """Test strategy applies to non-async."""
        context = ProjectContext(
            project_slug="myproject",
            open_source_license="MIT",
            username_type="email",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategy = NonAsyncStrategy()
        assert strategy.applies_to(context) is True
        
        ops = strategy.get_operations(context)
        assert len(ops) == 2
        assert any("asgi.py" in op.describe() for op in ops)


class TestStrategyRegistry:
    """Tests for StrategyRegistry."""
    
    def test_registry_has_strategies(self):
        """Test that registry contains strategies."""
        assert len(registry._strategies) > 0
    
    def test_get_applicable_strategies(self):
        """Test getting applicable strategies."""
        context = ProjectContext(
            project_slug="myproject",
            open_source_license="Not open source",
            username_type="username",
            editor="VS Code",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        strategies = registry.get_applicable_strategies(context)
        
        # Should have multiple applicable strategies
        assert len(strategies) > 0
        
        # Check specific strategies are included
        strategy_names = [s.get_name() for s in strategies]
        assert "NotOpenSourceStrategy" in strategy_names
        assert "UsernameAuthStrategy" in strategy_names
        assert "NonPyCharmStrategy" in strategy_names
        assert "NonDockerStrategy" in strategy_names
    
    def test_collect_operations(self):
        """Test collecting operations from all strategies."""
        context = ProjectContext(
            project_slug="myproject",
            open_source_license="Not open source",
            username_type="username",
            editor="VS Code",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        operations = registry.collect_operations(context)
        
        # Should collect multiple operations
        assert len(operations) > 0
        
        # Check for specific operations
        descriptions = [op.describe() for op in operations]
        assert any("CONTRIBUTORS.txt" in desc for desc in descriptions)
        assert any("LICENSE" in desc for desc in descriptions)


class TestStrategyIntegration:
    """Integration tests for strategies."""
    
    def test_full_docker_webpack_setup(self):
        """Test a full Docker + Webpack setup."""
        context = ProjectContext(
            project_slug="myproject",
            open_source_license="MIT",
            username_type="email",
            editor="VS Code",
            use_docker="y",
            cloud_provider="AWS",
            use_heroku="n",
            frontend_pipeline="Webpack",
            use_celery="y",
            use_async="y",
            ci_tool="Github",
            rest_api="DRF",
            keep_local_envs_in_vcs="y",
            debug="n",
        )
        
        operations = registry.collect_operations(context)
        
        # Should have operations from multiple strategies
        assert len(operations) > 0
        
        # Docker strategy should apply
        descriptions = [op.describe() for op in operations]
        assert any("utility" in desc for desc in descriptions)
        
        # Webpack strategy should apply
        assert any("gulpfile" in desc for desc in descriptions)
    
    def test_minimal_setup(self):
        """Test a minimal setup with no optional features."""
        context = ProjectContext(
            project_slug="myproject",
            open_source_license="Not open source",
            username_type="username",
            editor="None",
            use_docker="n",
            cloud_provider="None",
            use_heroku="n",
            frontend_pipeline="None",
            use_celery="n",
            use_async="n",
            ci_tool="None",
            rest_api="None",
            keep_local_envs_in_vcs="n",
            debug="n",
        )
        
        operations = registry.collect_operations(context)
        
        # Should have many operations (removing lots of files)
        assert len(operations) > 10
