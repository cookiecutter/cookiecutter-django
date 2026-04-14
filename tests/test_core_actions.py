"""Tests for the core actions module."""

import json
import os
import tempfile
from pathlib import Path

import pytest

from hooks.core.actions import (
    Action,
    ActionType,
    AppendFileAction,
    CreateDirectoryAction,
    DeleteDirectoryAction,
    DeleteFileAction,
    ModifyFileAction,
    ModifyJsonFileAction,
    RunCommandAction,
)


class TestDeleteFileAction:
    def test_delete_existing_file(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello world")

        action = DeleteFileAction(file_path=test_file)
        result = action.execute()

        assert result.success
        assert not test_file.exists()
        assert result.backup_data == b"hello world"

    def test_delete_nonexistent_file(self, tmp_path):
        test_file = tmp_path / "nonexistent.txt"

        action = DeleteFileAction(file_path=test_file)
        result = action.execute()

        assert result.success
        assert "does not exist" in result.message

    def test_delete_file_rollback(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello world")

        action = DeleteFileAction(file_path=test_file)
        result = action.execute()
        rollback_result = action.rollback(result.backup_data)

        assert rollback_result.success
        assert test_file.exists()
        assert test_file.read_text() == "hello world"

    def test_dry_run_does_not_delete(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello world")

        action = DeleteFileAction(file_path=test_file)
        result = action.execute(dry_run=True)

        assert result.success
        assert test_file.exists()
        assert "[DRY-RUN]" in result.message


class TestDeleteDirectoryAction:
    def test_delete_existing_directory(self, tmp_path):
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")

        action = DeleteDirectoryAction(dir_path=test_dir)
        result = action.execute()

        assert result.success
        assert not test_dir.exists()

    def test_delete_nonexistent_directory(self, tmp_path):
        test_dir = tmp_path / "nonexistent"

        action = DeleteDirectoryAction(dir_path=test_dir)
        result = action.execute()

        assert result.success
        assert "does not exist" in result.message


class TestCreateDirectoryAction:
    def test_create_new_directory(self, tmp_path):
        new_dir = tmp_path / "new_dir"

        action = CreateDirectoryAction(dir_path=new_dir)
        result = action.execute()

        assert result.success
        assert new_dir.exists()

    def test_create_nested_directory(self, tmp_path):
        new_dir = tmp_path / "parent" / "child" / "grandchild"

        action = CreateDirectoryAction(dir_path=new_dir)
        result = action.execute()

        assert result.success
        assert new_dir.exists()

    def test_create_existing_directory(self, tmp_path):
        existing_dir = tmp_path / "existing"
        existing_dir.mkdir()

        action = CreateDirectoryAction(dir_path=existing_dir)
        result = action.execute()

        assert result.success
        assert "already exists" in result.message


class TestModifyFileAction:
    def test_modify_file_content(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello {{ name }}!")

        action = ModifyFileAction(
            file_path=test_file,
            modifications={"{{ name }}": "World"},
        )
        result = action.execute()

        assert result.success
        assert test_file.read_text() == "Hello World!"

    def test_modify_file_multiple_replacements(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("{{ a }} and {{ b }}")

        action = ModifyFileAction(
            file_path=test_file,
            modifications={"{{ a }}": "1", "{{ b }}": "2"},
        )
        result = action.execute()

        assert result.success
        assert test_file.read_text() == "1 and 2"

    def test_modify_file_rollback(self, tmp_path):
        test_file = tmp_path / "test.txt"
        original_content = "original content"
        test_file.write_text(original_content)

        action = ModifyFileAction(
            file_path=test_file,
            modifications={"original": "modified"},
        )
        result = action.execute()
        rollback_result = action.rollback(result.backup_data)

        assert rollback_result.success
        assert test_file.read_text() == original_content


class TestAppendFileAction:
    def test_append_to_existing_file(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("line1\n")

        action = AppendFileAction(file_path=test_file, content="line2")
        result = action.execute()

        assert result.success
        assert test_file.read_text() == "line1\nline2\n"

    def test_append_to_new_file(self, tmp_path):
        test_file = tmp_path / "new.txt"

        action = AppendFileAction(file_path=test_file, content="first line")
        result = action.execute()

        assert result.success
        assert test_file.read_text() == "first line\n"


class TestModifyJsonFileAction:
    def test_remove_dev_dependencies(self, tmp_path):
        package_json = tmp_path / "package.json"
        package_json.write_text(
            json.dumps(
                {
                    "devDependencies": {
                        "webpack": "5.0.0",
                        "gulp": "4.0.0",
                    },
                    "scripts": {},
                }
            )
        )

        action = ModifyJsonFileAction(
            file_path=package_json,
            remove_dev_deps=["gulp"],
        )
        result = action.execute()

        assert result.success
        content = json.loads(package_json.read_text())
        assert "gulp" not in content["devDependencies"]
        assert "webpack" in content["devDependencies"]

    def test_update_scripts(self, tmp_path):
        package_json = tmp_path / "package.json"
        package_json.write_text(
            json.dumps(
                {
                    "devDependencies": {},
                    "scripts": {"old": "script"},
                }
            )
        )

        action = ModifyJsonFileAction(
            file_path=package_json,
            update_scripts={"new": "script", "old": "updated"},
        )
        result = action.execute()

        assert result.success
        content = json.loads(package_json.read_text())
        assert content["scripts"]["new"] == "script"
        assert content["scripts"]["old"] == "updated"

    def test_remove_keys(self, tmp_path):
        package_json = tmp_path / "package.json"
        package_json.write_text(
            json.dumps(
                {
                    "devDependencies": {},
                    "scripts": {},
                    "babel": {"presets": []},
                }
            )
        )

        action = ModifyJsonFileAction(
            file_path=package_json,
            remove_keys=["babel"],
        )
        result = action.execute()

        assert result.success
        content = json.loads(package_json.read_text())
        assert "babel" not in content


class TestActionDescription:
    def test_action_describe(self, tmp_path):
        action = DeleteFileAction(
            file_path=tmp_path / "test.txt",
            description="Custom description",
        )
        assert action.describe() == "Custom description"

    def test_action_to_dict(self, tmp_path):
        action = DeleteFileAction(file_path=tmp_path / "test.txt")
        d = action.to_dict()

        assert d["type"] == "delete_file"
        assert "file_path" in d
