"""
Tests for the bibliography module.
"""

import os
import pytest

from latex_suite import bibliography
from latex_suite import latex
import latex_suite.util
from tests import data

TEST_TIMEOUT = 10


@pytest.mark.timeout(TEST_TIMEOUT)
def test_create_bib_file(tmp_path):
    """
    Test the creation of a bib file from a set of bib files.

    :param tmp_path:
        The tmp test path.
    """
    os.chdir(tmp_path)
    os.mkdir(data.BIBS_FOLDER_NAME)
    os.chdir(data.BIBS_FOLDER_NAME)
    with open(data.FIRST_BIB_FILE_NAME, "w") as bib_file:
        bib_file.write(data.FIRST_BIB_FILE_CONTENT)
        bib_file.flush()
    with open(data.SECOND_BIB_FILE_NAME, "w") as bib_file:
        bib_file.write(data.SECOND_BIB_FILE_CONTENT)
        bib_file.flush()
    os.chdir("..")
    with open(data.SIMPLE_TEX_DOCUMENT_FILE_NAME, "w") as tex_file:
        tex_file.write(data.SIMPLE_TEX_DOCUMENT_WITH_CITATION)
        tex_file.flush()
    latex.compile_file("pdflatex", data.SIMPLE_TEX_DOCUMENT_FILE_NAME)
    assert os.path.isfile(data.SIMPLE_TEX_DOCUMENT_FILE_NAME), "Pdf not created. Error in pdf creation module."
    aux_file_path = latex_suite.util.filename_stem(data.SIMPLE_TEX_DOCUMENT_FILE_NAME) + ".aux"
    bib_folder_path = data.BIBS_FOLDER_NAME
    out_file_path = data.BIBLIOGRAPHY_FILE_NAME
    fields_to_remove = ["abstract", "file", "keywords", "url"]
    bibliography.create_bib_file(aux_file_path, bib_folder_path, out_file_path, fields_to_remove=fields_to_remove)
    assert os.path.isfile(data.BIBLIOGRAPHY_FILE_NAME), "Bibliography file should have been created."
    with open(data.BIBLIOGRAPHY_FILE_NAME, "r") as bib_file:
        bib_file_contents = bib_file.read()
        assert "@inproceedings{ref:aPaper" in bib_file_contents, "Paper entry not in bibliography file."
        assert "@book{ref:aBook" in bib_file_contents, "Book entry not in bibliography file."
        for one_field_to_remove in fields_to_remove:
            assert one_field_to_remove not in bib_file_contents, (
                   f"Entry removal error: '{one_field_to_remove}' has not been removed from the bibliography entries.")
