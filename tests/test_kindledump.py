import pytest

from kindle_highlight_exporter.kindledump import main
from kindle_highlight_exporter.kindledump import import_kindle_textfile
from kindle_highlight_exporter.kindledump import get_clippings_by_author
from kindle_highlight_exporter.kindledump import get_clippings_by_title
from kindle_highlight_exporter.subroutines import fuzzy_matches

__author__ = "boscacci"
__copyright__ = "boscacci"
__license__ = "MIT"

file_loc = "tests/test_data/2021-06-07_My Clippings.txt"
clippings_list = import_kindle_textfile(file_loc)


def test_import_kindle_textfile():
    """API Tests"""
    assert isinstance(clippings_list, list)
    assert len(clippings_list) > 0


def test_fuzzy_matches():
    assert (
        fuzzy_matches(
            value_from_clip=clippings_list[0]["author"],
            valid_values_list=["carreyrou john"],
        )
        == True
    )


def test_get_clippings_by_title():
    clippings_that_matter = get_clippings_by_title(
        clippings_list,
        only_these=[
            "something that matters",
        ],
    )
    assert len(clippings_that_matter) == 174

    hemingway_clips = get_clippings_by_title(
        clippings_list, only_these=["a farewell to arms"]
    )

    assert len(hemingway_clips) == 3


def test_get_clippings_by_author():
    carreyrou_clippings = get_clippings_by_author(
        clippings_list,
        only_these=[
            "John Carreyrou",
        ],
    )
    assert len(carreyrou_clippings) == 4


def test_get_clippings_by_not_author():
    not_carreyrou_clippings = get_clippings_by_author(
        clippings_list,
        exclude_these=[
            "John Carreyrou",
        ],
    )
    assert len(not_carreyrou_clippings) < len(clippings_list)
    assert "being large" in not_carreyrou_clippings[-2]["highlight_text"]


def test_search_by_author_cli(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(
        [
            file_loc,
            "--author",
            "John Carreyrou",
        ]
    )
    captured = capsys.readouterr()
    assert (
        "firewall between the Journal???s editorial and newsroom staffs"
        in captured.out
    )


def test_search_by_title_cli(capsys):
    main(
        [
            file_loc,
            "--title",
            "something that matters",
        ]
    )
    captured = capsys.readouterr()
    assert (
        "everyone reading this book has the potential to make a difference"
        in captured.out
    )
