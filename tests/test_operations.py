"""
Tests for the operations module.

Tests cover:
- Operation creation and execution
- Rollback functionality
- Edge cases (missing files, etc.)
"""

import json
import os
from pathlib import Path

import pytest

from hooks.operations import (
    DeleteFileOperation,
    DeleteDirectoryOperation,
    ModifyFileOperation,
    AppendToFileOperation,
    SetFlagOperation,
    FailureStrategy,
    OperationType,
)


@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory for tests."""
    prev_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        yield tmp_path
    finally:
        os.chdir(prev_cwd)


class TestDeleteFileOperation:
    """Tests for DeleteFileOperation."""
    
    def test_delete_existing_file(self, temp_dir):
        """Test deleting an existing file."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        op = DeleteFileOperation(file_path=test_file)
        result = op.execute()
        
        assert result["success"] is True
        assert result["skipped"] is False
        assert not test_file.exists()
    
    def test_delete_nonexistent_file(self, temp_dir):
        """Test deleting a file that doesn't exist."""
        test_file = temp_dir / "nonexistent.txt"
        
        op = DeleteFileOperation(file_path=test_file)
        result = op.execute()
        
        assert result["success"] is True
        assert result["skipped"] is True
        assert result["reason"] == "File does not exist"
    
    def test_rollback_deleted_file(self, temp_dir):
        """Test rolling back a deleted file."""
        test_file = temp_dir / "test.txt"
        original_content = b"original content"
        test_file.write_bytes(original_content)
        
        op = DeleteFileOperation(file_path=test_file)
        result = op.execute()
        
        assert not test_file.exists()
        
        # Rollback
        op.rollback(result)
        
        assert test_file.exists()
        assert test_file.read_bytes() == original_content
    
    def test_describe(self, temp_dir):
        """Test operation description."""
        test_file = temp_dir / "test.txt"
        op = DeleteFileOperation(file_path=test_file)
        
        assert "删除文件" in op.describe()
        assert "test.txt" in op.describe()


class TestDeleteDirectoryOperation:
    """Tests for DeleteDirectoryOperation."""
    
    def test_delete_existing_directory(self, temp_dir):
        """Test deleting an existing directory."""
        test_dir = temp_dir / "test_dir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")
        
        op = DeleteDirectoryOperation(dir_path=test_dir)
        result = op.execute()
        
        assert result["success"] is True
        assert result["skipped"] is False
        assert not test_dir.exists()
    
    def test_delete_nonexistent_directory(self, temp_dir):
        """Test deleting a directory that doesn't exist."""
        test_dir = temp_dir / "nonexistent"
        
        op = DeleteDirectoryOperation(dir_path=test_dir)
        result = op.execute()
        
        assert result["success"] is True
        assert result["skipped"] is True
    
    def test_rollback_deleted_directory(self, temp_dir):
        """Test rolling back a deleted directory."""
        test_dir = temp_dir / "test_dir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content")
        
        op = DeleteDirectoryOperation(dir_path=test_dir)
        result = op.execute()
        
        assert not test_dir.exists()
        
        # Rollback
        op.rollback(result)
        
        assert test_dir.exists()
        assert (test_dir / "file.txt").read_text() == "content"
    
    def test_describe(self, temp_dir):
        """Test operation description."""
        test_dir = temp_dir / "test_dir"
        op = DeleteDirectoryOperation(dir_path=test_dir)
        
        assert "删除目录" in op.describe()


class TestModifyFileOperation:
    """Tests for ModifyFileOperation."""
    
    def test_modify_file(self, temp_dir):
        """Test modifying a file."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("old content")
        
        def modifier(content):
            return content.replace("old", "new")
        
        op = ModifyFileOperation(file_path=test_file, modifier=modifier)
        result = op.execute()
        
        assert result["success"] is True
        assert test_file.read_text() == "new content"
    
    def test_modify_nonexistent_file(self, temp_dir):
        """Test modifying a file that doesn't exist."""
        test_file = temp_dir / "nonexistent.txt"
        
        def modifier(content):
            return content
        
        op = ModifyFileOperation(file_path=test_file, modifier=modifier)
        
        with pytest.raises(FileNotFoundError):
            op.execute()
    
    def test_rollback_modified_file(self, temp_dir):
        """Test rolling back a modified file."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("original content")
        
        def modifier(content):
            return "modified content"
        
        op = ModifyFileOperation(file_path=test_file, modifier=modifier)
        result = op.execute()
        
        assert test_file.read_text() == "modified content"
        
        # Rollback
        op.rollback(result)
        
        assert test_file.read_text() == "original content"


class TestAppendToFileOperation:
    """Tests for AppendToFileOperation."""
    
    def test_append_to_existing_file(self, temp_dir):
        """Test appending to an existing file."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("existing\n")
        
        op = AppendToFileOperation(file_path=test_file, content="appended")
        result = op.execute()
        
        assert result["success"] is True
        assert "appended" in test_file.read_text()
    
    def test_append_to_new_file(self, temp_dir):
        """Test appending to a new file."""
        test_file = temp_dir / "new_file.txt"
        
        op = AppendToFileOperation(file_path=test_file, content="content")
        result = op.execute()
        
        assert result["success"] is True
        assert test_file.read_text() == "content\n"
    
    def test_rollback_append(self, temp_dir):
        """Test rolling back an append operation."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("original\n")
        
        op = AppendToFileOperation(file_path=test_file, content="appended")
        result = op.execute()
        
        assert test_file.read_text() == "original\nappended\n"
        
        # Rollback
        op.rollback(result)
        
        assert test_file.read_text() == "original\n"


class TestSetFlagOperation:
    """Tests for SetFlagOperation."""
    
    def test_set_flag_with_value(self, temp_dir):
        """Test setting a flag with a specific value."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("key = !!!FLAG!!!")
        
        op = SetFlagOperation(
            file_path=test_file,
            flag="!!!FLAG!!!",
            value="new_value"
        )
        result = op.execute()
        
        assert result["success"] is True
        assert test_file.read_text() == "key = new_value"
    
    def test_set_flag_with_generator(self, temp_dir):
        """Test setting a flag with a generator function."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("key = !!!FLAG!!!")
        
        def generator():
            return "generated_value"
        
        op = SetFlagOperation(
            file_path=test_file,
            flag="!!!FLAG!!!",
            generator=generator
        )
        result = op.execute()
        
        assert result["success"] is True
        assert test_file.read_text() == "key = generated_value"
    
    def test_set_flag_nonexistent_file(self, temp_dir):
        """Test setting a flag in a nonexistent file."""
        test_file = temp_dir / "nonexistent.txt"
        
        op = SetFlagOperation(
            file_path=test_file,
            flag="!!!FLAG!!!",
            value="value"
        )
        
        with pytest.raises(FileNotFoundError):
            op.execute()
    
    def test_rollback_set_flag(self, temp_dir):
        """Test rolling back a set flag operation."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("key = !!!FLAG!!!")
        
        op = SetFlagOperation(
            file_path=test_file,
            flag="!!!FLAG!!!",
            value="new_value"
        )
        result = op.execute()
        
        assert test_file.read_text() == "key = new_value"
        
        # Rollback
        op.rollback(result)
        
        assert test_file.read_text() == "key = !!!FLAG!!!"


class TestOperationType:
    """Tests for operation types and metadata."""
    
    def test_operation_types(self):
        """Test that all operations have correct types."""
        delete_file = DeleteFileOperation(file_path=Path("test.txt"))
        assert delete_file.operation_type == OperationType.DELETE_FILE
        
        delete_dir = DeleteDirectoryOperation(dir_path=Path("test_dir"))
        assert delete_dir.operation_type == OperationType.DELETE_DIRECTORY
    
    def test_to_dict(self, temp_dir):
        """Test operation serialization."""
        test_file = temp_dir / "test.txt"
        op = DeleteFileOperation(file_path=test_file)
        
        data = op.to_dict()
        
        assert data["type"] == "DELETE_FILE"
        assert "description" in data
        assert "metadata" in data


class TestFailureStrategy:
    """Tests for failure strategies."""
    
    def test_default_failure_strategy(self):
        """Test default failure strategy."""
        op = DeleteFileOperation(file_path=Path("test.txt"))
        assert op.failure_strategy == FailureStrategy.STOP
