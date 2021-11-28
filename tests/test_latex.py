"""
Tests for the latex module.
"""

import os
import pytest

from latex_suite import latex
from tests import data
from tests.data import TEST_TIMEOUT


@pytest.fixture(autouse=True, scope='module')
def module_setup_teardown():
    yield


class TestLatexBashCompile:
    """
    Test the class to compile latex files.
    """

    @pytest.mark.parametrize("engine", data.SAMPLE_TEX_ENGINES)
    @pytest.mark.timeout(TEST_TIMEOUT)
    def test_compile(self, engine, tmp_path):
        tex_file_name = data.SAMPLE_TEX_FILE_NAME + ".tex"
        os.chdir(tmp_path)
        with open(tex_file_name, 'w') as tex_file:
            tex_file.write(data.SIMPLE_TEX_DOCUMENT)
        compile_result = latex.compile_file(engine, tex_file_name)
        assert compile_result.outcome == latex.Outcome.SUCCESS, "Compile process failed."
        assert os.path.isfile(data.SAMPLE_TEX_FILE_NAME + ".pdf"), "Pdf not generated"
        assert "1 page" in compile_result.output, "A one page pdf should have been created."

    @pytest.mark.parametrize("engine", data.SAMPLE_TEX_ENGINES)
    @pytest.mark.timeout(TEST_TIMEOUT)
    def test_get_warnings(self, engine, tmp_path):
        tex_file_name = data.SAMPLE_TEX_FILE_NAME + ".tex"
        os.chdir(tmp_path)
        with open(tex_file_name, 'w') as tex_file:
            tex_file.write(data.SIMPLE_TEX_DOCUMENT_WITH_ERROR)
        warnings = latex.get_warnings(engine, tex_file_name)
        assert os.path.isfile(data.SAMPLE_TEX_FILE_NAME + ".pdf"), "Pdf not generated"
        assert any("multiply defined" in one_warning for one_warning in warnings), "Label error not found."

    @pytest.mark.parametrize("engine", data.SAMPLE_TEX_ENGINES)
    @pytest.mark.timeout(TEST_TIMEOUT)
    def test_fail(self, engine, tmp_path):
        tex_file_name = data.SAMPLE_TEX_FILE_NAME + ".tex"
        os.chdir(tmp_path)
        with open(tex_file_name, 'w') as tex_file:
            tex_file.write(data.SIMPLE_TEX_DOCUMENT_UNCOMPILABLE)
        compile_result = latex.compile_file(engine, tex_file_name)
        assert compile_result.outcome == latex.Outcome.ABORTED, "Compile should have been aborted."
        assert compile_result.num_errors == 1, "There should have been one error after which was aborted."
        compile_result = latex.compile_file(engine, tex_file_name, max_end_attempts=3)
        assert compile_result.outcome == latex.Outcome.FAILURE, "Compile should have finished with a fail."
        assert compile_result.num_errors == 2, "There should have been two error through which the compile progressed."
        assert "Fatal error occurred, no output PDF file produced!" in compile_result.output, (
               "Pdflatex should have failed.")

    @pytest.mark.parametrize("engine", data.SAMPLE_TEX_ENGINES)
    @pytest.mark.timeout(TEST_TIMEOUT)
    def test_file_not_found(self, engine, tmp_path):
        tex_file_name = data.SAMPLE_TEX_FILE_NAME + ".tex"
        os.chdir(tmp_path)
        compile_result = latex.compile_file(engine, tex_file_name, verbose=True)
        assert compile_result.outcome == latex.Outcome.FILE_NOT_FOUND, "Compile should have been aborted."
        assert not os.path.isfile(data.UNKNOWN_TEX_FILE_NAME + ".pdf"), "Pdf should not Exist."

    @pytest.mark.parametrize("engine", data.SAMPLE_TEX_ENGINES)
    @pytest.mark.timeout(TEST_TIMEOUT)
    def test_unknown(self, engine, tmp_path):
        tex_file_name = data.SAMPLE_TEX_FILE_NAME + ".tex"
        os.chdir(tmp_path)
        with open(tex_file_name, 'w') as tex_file:
            tex_file.write(data.SIMPLE_TEX_DOCUMENT_UNKNOWN_COMMAND)
        compile_result = latex.compile_file(engine, tex_file_name)
        assert compile_result.outcome == latex.Outcome.SUCCESS, "Compile should have finished."
        assert compile_result.num_warnings == 1, ("There should have been one warning "
                                                  + "through which the compile progressed.")
        assert "! Undefined control sequence." in compile_result.output, "Compile should pick up unknown command."
        assert os.path.isfile(data.SAMPLE_TEX_FILE_NAME + ".pdf"), "Pdf not generated"
        assert "1 page" in compile_result.output, "A one page pdf should have been created."


class TestBibBashProcessing:
    """
    Test the class to process bib files.
    """

    @staticmethod
    def create_tex_and_bib(path, text_file_name, tex_content, bib_file_name, bib_content):
        os.chdir(path)
        with open(bib_file_name, "w") as bib_file:
            bib_file.write(bib_content)
            bib_file.flush()
        with open(text_file_name, 'w') as tex_file:
            tex_file.write(tex_content)
            tex_file.flush()

    @pytest.mark.parametrize("tex_engine", data.SAMPLE_TEX_ENGINES)  # ["pdflatex"])  # SAMPLE_TEX_ENGINES)
    @pytest.mark.parametrize("bib_engine", data.SAMPLE_BIB_ENGINES)  # ["bibtex"])  # SAMPLE_BIB_ENGINES)
    @pytest.mark.timeout(TEST_TIMEOUT)
    def test_process(self, tex_engine, bib_engine, tmp_path):
        os.chdir(tmp_path)
        tex_file_name = data.SAMPLE_TEX_FILE_NAME + ".tex"
        if bib_engine == "bibtex":
            tex_content = data.SIMPLE_TEX_DOCUMENT_WITH_CITATION_BIBTEX
        elif bib_engine == "biber":
            tex_content = data.SIMPLE_TEX_DOCUMENT_WITH_CITATION_BIBER
        else:
            assert False, "Unknown bib engine."
        TestBibBashProcessing.create_tex_and_bib(tmp_path, tex_file_name, tex_content,
                                                 data.SAMPLE_BIB_FILE_NAME, data.FIRST_BIB_FILE_CONTENT)
        compile_result = latex.compile_file(tex_engine, tex_file_name)
        assert compile_result.outcome == latex.Outcome.SUCCESS, "Error in pdf compilation."
        assert os.path.isfile(data.SAMPLE_TEX_FILE_NAME + ".aux"), "Error in bib processing."
        if bib_engine == "biber":
            assert "Package biblatex Warning: Please (re)run Biber on the file" in compile_result.output,\
                "Biber not recognised as bib engine."
        bib_result = latex.compile_bib(bib_engine, tex_file_name)
        assert bib_result.outcome == latex.Outcome.SUCCESS, "Bib processing not successful."
        assert os.path.isfile(data.SAMPLE_TEX_FILE_NAME + ".blg"), "Bib logfile not created."
        assert os.path.isfile(data.SAMPLE_TEX_FILE_NAME + ".bbl"), "Bib output file not created."
        compile_result = latex.compile_file(tex_engine, tex_file_name)
        if bib_engine == "bibtex":
            assert "LaTeX Warning: Citation `ref:aPaper'" in compile_result.output,\
                "Citation should not be fully processed."
        if bib_engine == "biber":
            assert "LaTeX Warning: There were undefined references." in compile_result.output,\
                "Citation should not be fully processed."
        compile_result = latex.compile_file(tex_engine, tex_file_name)
        assert "LaTeX Warning: Citation `ref:aPaper'" not in compile_result.output,\
            "Citation should not be fully processed."

    @pytest.mark.parametrize("tex_engine", data.SAMPLE_TEX_ENGINES)  # ["pdflatex"])  # SAMPLE_TEX_ENGINES)
    @pytest.mark.timeout(TEST_TIMEOUT)
    def test_process_bibtex_no_style(self, tex_engine, tmp_path):
        os.chdir(tmp_path)
        tex_file_name = data.SAMPLE_TEX_FILE_NAME + ".tex"
        TestBibBashProcessing.create_tex_and_bib(tmp_path, tex_file_name,
                                                 data.SIMPLE_TEX_DOCUMENT_WITH_CITATION_BIBTEX_NO_STYLE,
                                                 data.SAMPLE_BIB_FILE_NAME, data.FIRST_BIB_FILE_CONTENT)
        compile_result = latex.compile_file(tex_engine, tex_file_name)
        assert compile_result.outcome == latex.Outcome.SUCCESS, "Error in pdf compilation."
        assert os.path.isfile(data.SAMPLE_TEX_FILE_NAME + ".aux"), "Error in bib processing."
        bib_result = latex.compile_bib("bibtex", tex_file_name, verbose=True)
        assert "I found no \\bibstyle command" in bib_result.output, ("Output should contain info that "
                                                                      + "bib style is not set.")
        assert bib_result.outcome == latex.Outcome.FAILURE, "Processing should be logged as failed."
