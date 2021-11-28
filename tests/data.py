"""
Constants for tests.
"""

from latex_suite import util

TEST_TIMEOUT = 20

SAMPLE_TEX_FILE_NAME = "test_compile_tex_file"
SAMPLE_BIB_FILE_NAME = "bib_file.bib"
SAMPLE_TEX_ENGINES = ["pdflatex", "lualatex"]
UNKNOWN_TEX_FILE_NAME = "unknown_tex_file"
SAMPLE_BIB_ENGINES = ["bibtex", "biber"]
BIBS_FOLDER_NAME = "bibs_folder"
FIRST_BIB_FILE_NAME = "bib_file_1.bib"
SECOND_BIB_FILE_NAME = "bib_file_2.bib"
SIMPLE_TEX_DOCUMENT_FILE_NAME = "main.tex"
BIBLIOGRAPHY_FILE_NAME = "bibliography.bib"

SIMPLE_TEX_DOCUMENT = ("\\documentclass{article}"
                       + "\\usepackage[utf8]{inputenc}"
                       + "\\title{Sample Document}"
                       + "\\author{Mr Sample}"
                       + "\\begin{document}"
                       + "\\maketitle"
                       + "\\section{Introduction}"
                       + "\\end{document}")
SIMPLE_TEX_DOCUMENT_WITH_CITATION = ("\\documentclass{article}"
                                     + "\\usepackage[utf8]{inputenc}"
                                     + "\\title{Sample Document with Citations}"
                                     + "\\author{The Citer}"
                                     + "\\begin{document}"
                                     + "\\maketitle"
                                     + "\\section{Introduction}"
                                     + "The people in the paper~\\cite{ref:aPaper}"
                                     + " used the techniques described in the book\\cite{ref:aBook}."
                                     + "\\end{document}")
SIMPLE_TEX_DOCUMENT_WITH_ERROR = ("\\documentclass{article}"
                                  + "\\usepackage[utf8]{inputenc}"
                                  + "\\title{Sample Document}"
                                  + "\\author{Mr Sample}"
                                  + "\\begin{document}"
                                  + "\\maketitle"
                                  + "\\section{Introduction}"
                                  + "\\label{sec:intro}"
                                  + "\\subsection{Sub Intro}"
                                  + "\\label{sec:intro}"
                                  + "\\end{document}")
SIMPLE_TEX_DOCUMENT_UNCOMPILABLE = ("\\documentclass{article}"
                                    + "\\usepackage[utf8]{inputenc}"
                                    + "\\title{Sample Document}"
                                    + "\\author{Mr Sample}"
                                    + "\\begin{document}"
                                    + "\\maketitle"
                                    + "\\section{Introduction}"
                                    + "\\label{sec:intro}"
                                    + "\\subsection{Sub Intro}"
                                    + "\\label{sec:intro}")
SIMPLE_TEX_DOCUMENT_UNKNOWN_COMMAND = ("\\documentclass{article}"
                                       + "\\usepackage[utf8]{inputenc}"
                                       + "\\title{Sample Document}"
                                       + "\\author{Mr Sample}"
                                       + "\\begin{document}"
                                       + "\\maketitle"
                                       + "\\section{Introduction}"
                                       + "\\label{sec:intro}"
                                       + "\\subsection{Sub Intro}"
                                       + "\\label{sec:intro}"
                                       + "\\unknownCommand"
                                       + "\\end{document}")
SIMPLE_TEX_DOCUMENT_WITH_CITATION_BIBTEX = ("\\documentclass{article}"
                                            + "\\usepackage[utf8]{inputenc}"
                                            + "\\title{Sample Document}"
                                            + "\\author{Mr Sample}"
                                            + "\\begin{document}"
                                            + "\\maketitle"
                                            + "\\section{Introduction}"
                                            + "The people in the paper~\\cite{ref:aPaper}"
                                            + "\\bibliography{" + SAMPLE_BIB_FILE_NAME + "}"
                                            + "\\bibliographystyle{plain}"
                                            + "\\end{document}")
SIMPLE_TEX_DOCUMENT_WITH_CITATION_BIBTEX_NO_STYLE = ("\\documentclass{article}"
                                                     + "\\usepackage[utf8]{inputenc}"
                                                     + "\\title{Sample Document}"
                                                     + "\\author{Mr Sample}"
                                                     + "\\begin{document}"
                                                     + "\\maketitle"
                                                     + "\\section{Introduction}"
                                                     + "The people in the paper~\\cite{ref:aPaper}"
                                                     + "\\bibliography{" + SAMPLE_BIB_FILE_NAME + "}"
                                                     + "\\end{document}")
SIMPLE_TEX_DOCUMENT_WITH_CITATION_BIBER = ("\\documentclass{article}"
                                           + "\\usepackage[utf8]{inputenc}"
                                           + "\\usepackage{biblatex}"
                                           + "\\addbibresource{" + SAMPLE_BIB_FILE_NAME + "}"
                                           + "\\title{Sample Document}"
                                           + "\\author{Mr Sample}"
                                           + "\\begin{document}"
                                           + "\\maketitle"
                                           + "\\section{Introduction}"
                                           + "The people in the paper~\\cite{ref:aPaper}"
                                           + "\\printbibliography"
                                           + "\\end{document}")
FIRST_BIB_FILE_CONTENT = ("@inproceedings{ref:aPaper,"
                          + "abstract = {Interesting paper.},"
                          + "address = {Near You},"
                          + "author = {Noether, Emmy},"
                          + "booktitle = {Proceedings of the First Interesting Paper Conference},"
                          + "doi = {10.1001/123-4-567-89101-1_12},"
                          + "file = {:home/user/paper.pdf:pdf},"
                          + "isbn = {123-4-567-89121-1},"
                          + "pages = {123--456},"
                          + "publisher = {Paper Random House},"
                          + "title = {{Interesting Progress in Science}},"
                          + "url = {http://webpage.com/thePaper},"
                          + "year = {2012}"
                          + "}")
SECOND_BIB_FILE_CONTENT = ("@book{ref:aBook,"
                           + "abstract = {Interesting book.},"
                           + "address = {Near You},"
                           + "author = {Fletcher, Jessica Beatrice},"
                           + "booktitle = {Handbook of Doing Science},"
                           + "doi = {10.1001/ABC12345678910111},"
                           + "file = {:home/user/book.pdf:pdf},"
                           + "isbn = {ABC12345678910111},"
                           + "pages = {1--1345},"
                           + "publisher = {Books Publisher Ltd},"
                           + "title = {{Handbook of Doing Science}},"
                           + "year = {2017}"
                           + "}")

SIMPLE_YAML_DOCUMENT = ("engine: "
                        + util.Configuration.DEFAULT_CONF["engine"][util.Configuration.IDX_VALUE] + "A\n"
                        + "bib_engine : "
                        + util.Configuration.DEFAULT_CONF["bib_engine"][util.Configuration.IDX_VALUE] + "B\n"
                        + "main_tex: "
                        + util.Configuration.DEFAULT_CONF["main_tex"][util.Configuration.IDX_VALUE] + "C")
SAMPLE_YAML_FILE_NAME = "test_yaml.yaml"
TEX_FILE_NAME_STEM = "text.tex"
TEX_FILE_STEM_NON_COMPILE_LETTERS = ["A", "B", "C"]
TEX_FILE_STEM_COMPILE_LETTERS = ["X", "Y", "Z"]
CLEAN_DIRECTORIES = ["a", "a/1", "a/2",
                     "b", "b/1"]
CLEAN_FILES_LEVEL_1 = ["kpl.log",
                       "a/x.log",
                       "b/z.aux", "b/z.log"]
CLEAN_FILES_LEVEL_2 = ["a/1/x.aux",
                       "a/2/y.log", "a/2/y.aux",
                       "b/1/zk.aux"]
FILE_PATTERN_ADD_FILE_NAME = ".gitignore"
FILE_PATTERN_ADD_FILE_CONTENTS = ("abc.txt\n"
                                  + "def.doc\n"
                                  + "xyz.doc\n"
                                  + "*.log\n"
                                  + "*.jpg\n"
                                  + "*.png\n"
                                  + "foo.doc\n"
                                  + "*.mp3\n"
                                  + "*.mp4\n"
                                  + "*.mux\n"
                                  + "*.flog\n"
                                  + "corn.pptx\n")
FILE_PATTERN_ADD_FILE_EXPECTED = ("abc.txt\n"
                                  + "def.doc\n"
                                  + "xyz.doc\n"
                                  + "*.log\n"
                                  + "*.jpg\n"
                                  + "*.png\n"
                                  + "foo.doc\n"
                                  + "*.mp3\n"
                                  + "*.mp4\n"
                                  + "*.mux\n"
                                  + "*.flog\n"
                                  + "*.aux\n"
                                  + "*.bbl\n"
                                  + "corn.pptx\n"
                                  + "main.pdf\n"
                                  + "figure1.pdf\n")
FILE_PATTERN_ADD_FILE_PATTERNS = ["*.aux", "*.log", "main.pdf", "*.bbl", "figure1.pdf"]

SAMPLE_ERROR_FILE = "file_with_text_error.txt"
ERROR_FILE_CONTENTS = "I have a apple\nI eat  fruits.\nThe tree is is in the forest."
TEXT_ERROR_AN = "I have an car."
