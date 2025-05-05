import os
import pytest
import tempfile

from src.create_init_file.script import create_init_files


@pytest.fixture
def temp_dir_structure():
    """Create a temporary directory structure for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create sample directory structure
        os.makedirs(os.path.join(tmpdir, "dir1"))
        os.makedirs(os.path.join(tmpdir, "dir2", "subdir"))
        os.makedirs(os.path.join(tmpdir, "__pycache__"))  # Should be excluded
        os.makedirs(os.path.join(tmpdir, "dir3", "exclude_me"))

        yield tmpdir


def assert_init_files_exist(base_dir, expected_dirs, excluded_dirs):
    """Helper function to assert the existence of __init__.py files."""
    for dir_path in expected_dirs:
        assert os.path.exists(os.path.join(base_dir, dir_path, "__init__.py")), f"Missing __init__.py in {dir_path}"

    for dir_path in excluded_dirs:
        assert not os.path.exists(os.path.join(base_dir, dir_path, "__init__.py")), f"Unexpected __init__.py in {dir_path}"


def test_create_init_files_basic(temp_dir_structure):
    """Test that __init__.py files are created in all non-excluded directories."""
    create_init_files(temp_dir_structure, exclude_dirs=["exclude_me"])

    # Expected and excluded directories
    expected_dirs = ["dir1", "dir2", "dir2/subdir", "dir3"]
    excluded_dirs = ["__pycache__", "dir3/exclude_me"]

    # Check files were created or excluded
    assert_init_files_exist(temp_dir_structure, expected_dirs, excluded_dirs)


def test_create_init_files_already_exists(temp_dir_structure):
    """Test that existing __init__.py files aren't overwritten."""
    # Create an existing __init__.py
    existing_init = os.path.join(temp_dir_structure, "dir1", "__init__.py")
    os.makedirs(os.path.dirname(existing_init), exist_ok=True)
    with open(existing_init, "w") as f:
        f.write("Existing content")

    create_init_files(temp_dir_structure)

    # Verify content wasn't overwritten
    with open(existing_init, "r") as f:
        assert f.read() == "Existing content", "Existing __init__.py was overwritten"


def test_create_init_files_permission_error(monkeypatch, temp_dir_structure):
    """Test handling of permission errors."""
    def mock_open(*args, **kwargs):
        raise PermissionError("Test permission error")

    monkeypatch.setattr("builtins.open", mock_open)

    # This should not raise an exception
    try:
        create_init_files(temp_dir_structure)
    except PermissionError:
        pytest.fail("PermissionError was not handled gracefully")


def test_main_with_args(monkeypatch, temp_dir_structure):
    """Test the command-line argument parsing."""
    import argparse
    from src.create_init_file.script import main

    # Mock argparse
    def mock_parse_args(self):
        return argparse.Namespace(
            root_dir=temp_dir_structure,
            exclude=["exclude_me"]
        )

    monkeypatch.setattr(argparse.ArgumentParser, 'parse_args', mock_parse_args)

    # This should run without errors
    main()

    # Expected and excluded directories
    expected_dirs = ["dir1", "dir2", "dir2/subdir", "dir3"]
    excluded_dirs = ["dir3/exclude_me", "__pycache__"]

    # Verify files were created or excluded
    assert_init_files_exist(temp_dir_structure, expected_dirs, excluded_dirs)
