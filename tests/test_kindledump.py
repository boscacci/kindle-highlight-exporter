import pytest

from kindle_highlight_exporter.kindledump import main
from kindle_highlight_exporter.kindledump import import_kindle_textfile
from kindle_highlight_exporter.kindledump import get_clippings_by_author

__author__ = "boscacci"
__copyright__ = "boscacci"
__license__ = "MIT"

file_loc = "tests/test_data/2021-06-07_My Clippings.txt"
clippings_list = import_kindle_textfile(file_loc)


def test_import_kindle_textfile():
    """API Tests"""
    assert isinstance(clippings_list, list)
    assert len(clippings_list) > 0


def test_get_clippings_by_author():
    carreyrou_clippings = get_clippings_by_author(
        clippings_list,
        only_these_authors=[
            "John Carreyrou",
        ],
    )
    assert len(carreyrou_clippings) == 4


def test_get_clippings_by_not_author():
    not_carreyrou_clippings = get_clippings_by_author(
        clippings_list,
        exclude_these_authors=[
            "John Carreyrou",
        ],
    )
    assert len(not_carreyrou_clippings) < len(clippings_list)
    assert "being large" in not_carreyrou_clippings[-2]["highlight_text"]


def test_main(capsys):
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
        "firewall between the Journal’s editorial and newsroom staffs"
        in captured.out
    )
