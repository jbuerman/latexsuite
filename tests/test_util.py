"""
Test for the utility module.
"""

import os
import pytest
import yaml

import latex_suite.util as util
from latex_suite.search_language_errors import ErrorList
from tests import data


@pytest.fixture(autouse=True, scope='module')
def module_setup_teardown():
    yield


class TestConfiguration:
    """
    Tests for the configuration class.
    """

    def test_init(self, tmp_path):
        with open(data.SAMPLE_YAML_FILE_NAME, 'w') as yaml_file:
            yaml_file.write(data.SIMPLE_YAML_DOCUMENT)
        with open(data.SAMPLE_YAML_FILE_NAME, "r") as config_file:
            config = util.Configuration(yaml.safe_load(config_file))
        assert config.engine == util.Configuration.DEFAULT_CONF["engine"][util.Configuration.IDX_VALUE] + "A"
        assert config.bib_engine == util.Configuration.DEFAULT_CONF["bib_engine"][util.Configuration.IDX_VALUE] + "B"
        assert config.main_tex == util.Configuration.DEFAULT_CONF["main_tex"][util.Configuration.IDX_VALUE] + "C"

    def test_write_default(self, tmp_path):
        config_file_path = tmp_path / "test_conf.yaml"
        util.Configuration.write_default(config_file_path)
        assert os.path.isfile(config_file_path), "Config file should have been created."
        yaml.SafeLoader.add_multi_constructor("ErrorList", ErrorList.from_yaml)
        with open(config_file_path, "r") as config_file:
            loaded_config_dict = yaml.safe_load(config_file)
        assert loaded_config_dict is not None, "A config dict should have been loaded."
        assert util.Configuration.DEFAULT_CONF["engine"][util.Configuration.IDX_TAG] in loaded_config_dict, (
               "No default engine in config file.")
        assert (loaded_config_dict[util.Configuration.DEFAULT_CONF["engine"][util.Configuration.IDX_TAG]]
                == util.Configuration.DEFAULT_CONF["engine"][util.Configuration.IDX_VALUE]), (
                "Wrong default engine in config file.")

    def test_config_attributes_and_properties(self):
        config = util.Configuration()
        for default_entry_key in util.Configuration.DEFAULT_CONF.keys():
            assert (config.__getattribute__("_" + default_entry_key)
                    == util.Configuration.DEFAULT_CONF[default_entry_key][util.Configuration.IDX_VALUE]), (
                    "Variable should be set to default value.")
            assert (config.__getattribute__(default_entry_key)
                    == util.Configuration.DEFAULT_CONF[default_entry_key][util.Configuration.IDX_VALUE]), (
                    "Variable should be set to default value.")
            with pytest.raises(AttributeError):
                config.__setattr__(default_entry_key, 7), "Should not be able to set configurations."


def test_find_compilable_tex(tmp_path):
    os.chdir(tmp_path)
    for letter in data.TEX_FILE_STEM_COMPILE_LETTERS:
        with open(letter + data.TEX_FILE_NAME_STEM, "w") as tex_file:
            tex_file.write("%Comment\n"
                           + " \n"
                           + "%%Comment\n"
                           + "%%Comment\\documentclass\n"
                           + "\t \t\n"
                           + "\t\n"
                           + "%%Comment\n"
                           + "\\documentclass{article}")
    for letter in data.TEX_FILE_STEM_NON_COMPILE_LETTERS:
        with open(letter + data.TEX_FILE_NAME_STEM, "w") as tex_file:
            tex_file.write("%Comment\n"
                           + " \t \n"
                           + "%% Comment \\documentclass"
                           + "\\section{The Section}")
    files = util.find_compilable_tex(".")
    assert len(files) == len(data.TEX_FILE_STEM_COMPILE_LETTERS), "Number of files of compilable files wrong."
    for letter in data.TEX_FILE_STEM_COMPILE_LETTERS:
        assert letter + data.TEX_FILE_NAME_STEM in files
    for letter in data.TEX_FILE_STEM_NON_COMPILE_LETTERS:
        assert letter + data.TEX_FILE_NAME_STEM not in files


def test_remove_files(tmp_path):
    for one_dir_name in data.CLEAN_DIRECTORIES:
        one_dir = tmp_path / one_dir_name
        one_dir.mkdir()
    for one_file_name in data.CLEAN_FILES_LEVEL_1 + data.CLEAN_FILES_LEVEL_2:
        one_file = tmp_path / one_file_name
        one_file.touch()
    util.remove_files(util.Configuration.DEFAULT_CONF["clean_extensions"][util.Configuration.IDX_VALUE],
                      directory=tmp_path, depth=1, force_remove=True)
    for one_file_name in data.CLEAN_FILES_LEVEL_1:
        one_file_path = tmp_path / one_file_name
        assert not os.path.isfile(one_file_path), "File '" + str(one_file_path) + "' should have been deleted."
    for one_file_name in data.CLEAN_FILES_LEVEL_2:
        one_file_path = tmp_path / one_file_name
        assert os.path.isfile(one_file_path), "File '" + str(one_file_path) + "' should not have been deleted."
    util.remove_files(util.Configuration.DEFAULT_CONF["clean_extensions"][util.Configuration.IDX_VALUE],
                      directory=tmp_path, depth=2, force_remove=True)
    for one_file_name in data.CLEAN_FILES_LEVEL_2:
        one_file_path = tmp_path / one_file_name
        assert not os.path.isfile(one_file_path), "File '" + str(one_file_path) + "' should not have been deleted."


def test_add_files_and_extensions_to_file(tmp_path):
    target_file_path = tmp_path / data.FILE_PATTERN_ADD_FILE_NAME
    with open(target_file_path, "w") as file:
        file.write(data.FILE_PATTERN_ADD_FILE_CONTENTS)
        file.flush()
    util.add_files_and_extensions_to_file(data.FILE_PATTERN_ADD_FILE_PATTERNS, target_file_path)
    with open(target_file_path, "r") as file:
        lines = file.readlines()
        contents = "".join(lines)
    assert contents == data.FILE_PATTERN_ADD_FILE_EXPECTED, "File patterns not correctly added to file."
