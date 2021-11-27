"""
Test latex_suite module.
"""
import argparse as ap
import os
import pytest
import sys

from latex_suite import latex_suite


class TestArgumentParserExtensions:

    def test_is_valid_file(self, tmp_path, capsys):
        os.chdir(tmp_path)
        one_file = tmp_path / "a_file.txt"
        one_file.touch()
        out_path = latex_suite.ArgumentParserExtensions.is_valid_file(one_file, None)
        assert out_path == one_file, "The path should be returned if the file exists."
        parser = ap.ArgumentParser()
        not_existing_file_name = "not_a_file.txt"
        with pytest.raises(SystemExit) as wrapped_e:
            latex_suite.ArgumentParserExtensions.is_valid_file(not_existing_file_name, parser)
        assert wrapped_e.type == SystemExit, "Should system exit with non existing file."
        assert not_existing_file_name in capsys.readouterr().err, "Message should inform about filename."
        with pytest.raises(SystemExit) as wrapped_e:
            latex_suite.ArgumentParserExtensions.is_valid_file(latex_suite.NO_TEX_FOUND_WARNING, parser)
        assert wrapped_e.type == SystemExit, "Should system exit with no compatible file."
        assert "compatible" in capsys.readouterr().err, "Message should inform that there is no compatible file."

    def test_is_valid_directory(self, tmp_path, capsys):
        os.chdir(tmp_path)
        one_dir = tmp_path / "a_dir"
        one_dir.mkdir()
        out_path = latex_suite.ArgumentParserExtensions.is_valid_directory(one_dir, None)
        assert out_path == str(one_dir), "The path should be returned if the directory exists."
        parser = ap.ArgumentParser()
        not_existing_dir = "not_a_dir"
        with pytest.raises(SystemExit) as wrapped_e:
            latex_suite.ArgumentParserExtensions.is_valid_directory(not_existing_dir, parser)
        assert wrapped_e.type == SystemExit, "Should system exit with non existing directory."
        assert not_existing_dir in capsys.readouterr().err, "Message should inform about directory name."


def create_clean_up_files(dir_path):
    first_dir_name = "dir_a"
    second_dir_name = "dir_b"
    first_file_name = "file_a.log"
    second_file_name = "file_b.aux"
    third_file_name = "file_c.bbl"
    first_dir = dir_path / first_dir_name
    second_dir = first_dir / second_dir_name
    first_dir.mkdir(exist_ok=True)
    second_dir.mkdir(exist_ok=True)
    first_file = dir_path / first_file_name
    second_file = first_dir / second_file_name
    third_file = second_dir / third_file_name
    first_file.touch()
    second_file.touch()
    third_file.touch()


def count_files(dir_path):
    num_files = 0
    for _, _, files in os.walk(dir_path):
        for name in files:
            num_files += 1
    return num_files


def test_select_task_clean_up(tmp_path, capsys):
    os.chdir(tmp_path)
    create_clean_up_files(tmp_path)
    sys.argv = ["latexsuite", "clean", "-l"]
    latex_suite.main()
    assert "Found 1 file(s)." in capsys.readouterr().out, "One file should have been found."
    for i in [1, 2]:
        sys.argv = ["latexsuite", "clean", "-l", f"-d {i}"]
        latex_suite.main()
        assert f"Found {i + 1} file(s)." in capsys.readouterr().out, f"{i + 1} files should have been found."
    for i in [0, 1, 2]:
        create_clean_up_files(tmp_path)
        sys.argv = ["latexsuite", "clean", f"-d {i}", "-f"]
        latex_suite.main()
        assert f"Removed {i + 1} of {i + 1} file(s)." in capsys.readouterr().out,\
            f"Should inform about removal of {i + 1} files."
        assert count_files(tmp_path) == 3 - i - 1, f"Only {i + 1} files should have been removed."
