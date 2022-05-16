"""
To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         kindledump = kindle_highlight_exporter.kindledump:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys

from kindle_highlight_exporter import __version__

__author__ = "boscacci"
__copyright__ = "boscacci"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from kindle_highlight_exporter.kindledump import import_kindle_textfile`,
# when using this Python module as a library.

from kindle_highlight_exporter.subroutines import import_kindle_textfile
from kindle_highlight_exporter.subroutines import get_clippings_by_author

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Dump kindle data in a nice format"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="kindle-highlight-exporter {ver}".format(ver=__version__),
    )
    parser.add_argument(
        dest="clippings_path",
        help="path of clippings file",
        type=str,
        metavar="CLIPPINGS_PATH",
        # required=True,
    )
    parser.add_argument(
        "--author",
        dest="author",
        help="author name",
        type=str,
        metavar="AUTHOR",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel,
        stream=sys.stdout,
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main(args):
    """Wrapper allowing :func:`kindledump` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`kindledump`, it prints the result to the
    ``stdout`` in a nicely formatted message, or saves to a file.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--author", "John Carreyrou"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting kindle dump")
    args_dict = vars(args)
    clippings_path = import_kindle_textfile(args_dict["clippings_path"])
    if "author" in args_dict:
        authors = args_dict["author"]
        print(f"Getting {authors} clips:")
        author_clips = get_clippings_by_author(
            clippings_path,
            only_these_authors=authors,
        )
        print([(clip, "\n") for clip in author_clips])
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m kindle_highlight_exporter.skeleton 42
    #
    run()
