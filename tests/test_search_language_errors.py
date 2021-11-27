"""
Test the module to search for textual errors.
"""

import os

import latex_suite.util
from latex_suite import search_language_errors
from tests import data
from latex_suite.util import Configuration


class TestErrorList:

    def test_identifiers(self):
        Configuration()
        all_identifiers = Configuration.get_config().language_errors.identifiers
        assert "spl" in all_identifiers, "Error type identifier missing."
        assert "sc" in all_identifiers, "Error type identifier missing."


class TestTextErrorType:

    @staticmethod
    def test_check_for_error_an():
        example_error_article_error = latex_suite.util.Configuration.DEFAULT_CONF["language_errors"][1][0]
        error = example_error_article_error.check_for_error(data.TEXT_ERROR_AN)
        assert error is not None, "An error should have been found."
        assert error.error_type.error_message == example_error_article_error.error_message,\
            "It should be an ''An' not in front of vowel.' error."
        assert error.start_idx_in_text == 6, "The error starts in index 6."
        assert error.end_idx_in_text == 11, "The error starts in index 11."


def test_check_for_error_and_print(tmp_path):
    error_file = data.SAMPLE_ERROR_FILE
    os.chdir(tmp_path)
    with open(error_file, 'w') as err_file:
        err_file.write(data.ERROR_FILE_CONTENTS)
    errors = latex_suite.util.Configuration.DEFAULT_CONF["language_errors"][1]
    found_errors = search_language_errors.check_for_error_and_print(error_file, errors)
    article_error = next(e for e in latex_suite.util.Configuration.DEFAULT_CONF["language_errors"][1].errors
                         if e.error_message == "'A' in front of vowel.")
    space_error = next(e for e in latex_suite.util.Configuration.DEFAULT_CONF["language_errors"][1].errors
                       if e.error_message == "Extra space.")
    doubled_error = next(e for e in latex_suite.util.Configuration.DEFAULT_CONF["language_errors"][1].errors
                         if e.error_message == "Doubled word.")
    assert article_error in [e.error_type for e in found_errors[1]],\
           "File contains article error in the first line that was not detected."
    assert space_error in [e.error_type for e in found_errors[2]],\
           "File contains extra space error in the second line that was not detected."
    assert doubled_error in [e.error_type for e in found_errors[3]],\
           "File contains doubled word error in the third line that was not detected."
