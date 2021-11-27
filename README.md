# Latex Suite

This suite of little programs is intended to support creating latex documents that are being written in editor
and console.

If you want to change the default behaviour create a configuration file.
See [Task: conf](#task-conf) on how to create a config file and see [Configuration](#configuration) on the
parameters and their defaults.

## Installation

### Installation with Pip

```bash
  $ python3 -m pip install latexsuite
```

### Manual Installation

```bash
  $ git clone https://github.com/jbuerman/latexsuite
  $ cd latexsuite
  $ python setup.py install
```

### Autocomplete

LatexSuite uses [argcomplete](https://pypi.org/project/argcomplete) for argument autocompletion and is
set up for global completion. See argcomplete's
[pypi site](https://pypi.org/project/argcomplete/#activating-global-completion) or
[github](https://github.com/kislyuk/argcomplete#activating-global-completion) to activate global completion.

## Tasks

The suite different capabilities are determined by the first argument the  **task**.
The different tasks are:
* make: Typeset the default tex
* cmake: Typeset any tex
* bibfile: Create bibliography file from required citations.
* clean: Remove typesetting side files.
* lang: Check common language errors in a document.
* conf: Write the default config file.

### Task: make and cmake

Typeset one or several tex files. The _make_ command will initiate
the typesetting of the main tex file or all compilable tex. The
_cmake_ command will initiate the typesetting of any specified tex.

#### Parameter

___texfile___\
&ensp;&ensp;Positional argument that accepts any compilable tex file in the current directory.
    If no argument is supplied the default tex file is compiles. (Ignored if _--all_ is given.)

___--all___\
&ensp;&ensp;Compile all latex files in the current directory which are deemed self-compilable.
    Self-compilable tex files that contain a `\documentclass` in the first non comment/empty line.
    (Not available for cmake.)

___-b/--bib___\
&ensp;&ensp;Also process the bibliography.

___-v/--verbose___\
&ensp;&ensp;Print the cmd output of the latex and bib engine.

___-l/--listStatus___\
&ensp;&ensp;List the compilation status of file typesetting when _--all_ is given.
    (Ignored if _--all_ is not given. Not available for cmake.)

___-n/--number___\
&ensp;&ensp;Number of latex error to ignore.
    Override the [number_ignore_latex_compile_errors](#configuration) configuration value for the current run.

### Task: bibfile

Creates a bibliography based on the citations in the main tex file. The assumption is that there is
a "database" of bibtex files, i.e. a folder that contains one or several bibtex files.
The task reads in the aux file and searches in the database for all bibliographic blocks for citations
listed in the aux file. The task then writes a local bibliography file with the needed references.

#### Parameter

___-a/--auxFile___\
&ensp;&ensp;The aux file to use. If not supplied the aux file of the main tex file is used.

___-b/--bibsFolder___\
&ensp;&ensp;The folder where the bibliography files are located.

___-o/--output___\
&ensp;&ensp;The output file where the local bibliography is written to.

### Task: clean

Removes the temporary files from the latex typesetting
process based on the configured file extensions.

#### Parameter

___-d___\
&ensp;&ensp;Depth of search into sub-folders for the files.
    Overrides [clean_depth](#configuration) configuration value for the current run.

___-l___\
&ensp;&ensp;Only list the files and do not delete them.

___-f___
&ensp;&ensp;Force delete and not ask for confirmation for every file

### Task: lang

Allows checking a text file for textual errors. The default behaviour is that every line
gets tested for all errors. However, error types can be ignored using the associated flag.
The task tests for the following errors.

- __'An' not in front of a vowel or 'a' in front of a vowel__
  , e.g. 'an car' or 'a apple'. Will also list 'false positives' like 'a hour'.
- __Extra space.__ Lists occasions where a space is followed by one or more spaces.
- __Named reference with lower case.__ Occasions where a reference is not capitalised,
  e.g. "figure 4" instead of "Figure 4".
- __Doubled word.__ Occasions where a word is repeated, e.g. "John had a car _and and_ a house."
- __Citation with name and not shortcite.__
  - Flag for exclusion '-c'.
- __Every sentence in a line.__ Checks that every sentence is in its own line.
  - Flag for exclusion '-l'.

#### Parameter

___file___\
&ensp;&ensp;Positional argument that accepts any text file.

___-l___\
&ensp;&ensp;Ignore (do not list) "Every sentence in a line" errors.

___-c___\
&ensp;&ensp;Ignore (do not list) "Citation with name and not shortcite" errors.

### Task: conf

Write the config file for the suite with the default parameters.

#### Parameter

<dl>
    <dt><strong>-f</strong></dt>
        <dd>
            Overriding the config file if it already exists.
        </dd>
</dl>

### Configuration

The configuration parameters, their meaning and their default
values.

<dl>
    <dt><strong>engine</strong></dt>
        <dd>
            The program to use to typeset the tex file (default value: pdflatex).
        </dd>
    <dt><strong>bib_engine</strong></dt>
        <dd>
            The program to use to process the bibliography (default value: biber).
        </dd>
    <dt><strong>main_tex</strong></dt>
        <dd>
            The main tex file to compile (default value: main.tex).
        </dd>
    <dt><strong>clean_file_extensions</strong></dt>
        <dd>
            The file extensions to use when searching for temporary
            files to delete (default value: [".log", ".aux", ".bbl", ".blg"]).
        </dd>
    <dt><strong>clean_depth</strong></dt>
        <dd>
            The depth (sub-folder traversal) used to search for
            temporary files. 0 means current dir, 1 means include
            sub-folder, 2 means sub-folder of sub-folders, etc. (default value: 0).
        </dd>
    <dt><strong>bib_files_folder</strong></dt>
        <dd>
            The folder where bibliography files are stored
            that shall be parsed when compiling a bib file of relevant
            references (default value: . [i.e. current  dir]).
        </dd>
    <dt><strong>main_bibliography_file</strong></dt>
        <dd>The file to write the relevant references blocks to
            (default value: bibliography.bib").
        </dd>
    <dt><strong>bibliography_fields_to_remove</strong></dt>
        <dd>
            The bibliography blocks fields that are to be removed
            before adding the block to the file of relevant
            references (default value: ["abstract", "file",
            "keywords", "url"]).
        </dd>
    <dt><strong>number_ignore_latex_compile_errors</strong></dt>
        <dd>
            Number of times the latex typesetting program
            should try to ignore un-ended environments
            (default value: 1).
        </dd>
    <dt><strong>language_errors</strong></dt>
        <dd>
            Errors that are checked during the text error check. All errors are matches of the specified
            regular expression.
            Every error must have the following required and can have the following optional parameter.
            <dl>
                <dt>message (required)</dt>
                <dd>
                    The error message.
                </dd>
                <dt>regex (required)</dt>
                <dd>
                    The regular expression used to search for this error.
                </dd>
                <dt>identifier (optional)</dt>
                <dd>
                    Used to create a command line arg to exclude the error during 
                    a check for text errors. Uniqueness should be ensured.
                </dd>
                <dt>exclude_words (optional)</dt>
                <dd>
                    First words for which a match should be ignored. For example, an error checking for capitalisation
                    of references, e.g. 'figure 1' instead of 'Figure 1', should ignore a match with an 'and', e.g.
                    'and 1' out of 'Figure 1 and 2' should not be a match.
                </dd>
                <dt>split_character (optional)</dt>
                <dd>
                    The character to split a match of the regex into substrings.
                    Used in conjunction with exclude_words to determine the first word (default: ' ', i.e. space).
                </dd>
            </dl>
        </dd>
</dl>

# Known Problems

## Messages that start with an asterisk

Some tex files might have an output that starts with an asterisks,
e.g. "&ast;geometry&ast; driver: auto-detecting". In this case the
line will be taken like an unclosed environment error. Setting the
number of errors to process over can circumvent this, e.g.
"*latexsuite make -n 1*".
