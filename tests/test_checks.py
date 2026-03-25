"""Tests for plasmate_audit.checks."""
import pytest
from plasmate_audit.checks import (
    check_title,
    check_headings,
    check_links,
    check_content_length,
    check_images,
    ALL_CHECKS,
)

URL = "https://example.com"


# --- check_title ---

def test_missing_title():
    som = {"title": ""}
    issues = check_title(som, URL)
    assert len(issues) == 1
    assert issues[0]["rule"] == "missing-title"
    assert issues[0]["severity"] == "error"


def test_good_title():
    som = {"title": "A Perfectly Good Page Title"}
    issues = check_title(som, URL)
    assert issues == []


def test_long_title():
    som = {"title": "x" * 65}
    issues = check_title(som, URL)
    assert len(issues) == 1
    assert issues[0]["rule"] == "title-too-long"
    assert issues[0]["severity"] == "warning"


def test_short_title():
    som = {"title": "Hi"}
    issues = check_title(som, URL)
    assert len(issues) == 1
    assert issues[0]["rule"] == "title-too-short"


# --- check_headings ---

def _som_with_headings(levels: list[int]) -> dict:
    elements = [
        {"role": "heading", "attrs": {"level": lv}, "text": f"Heading {lv}"}
        for lv in levels
    ]
    return {"regions": [{"elements": elements}]}


def test_no_headings():
    som = {"regions": [{"elements": []}]}
    issues = check_headings(som, URL)
    rules = [i["rule"] for i in issues]
    assert "no-h1" in rules
    assert "no-headings" in rules


def test_single_h1():
    som = _som_with_headings([1, 2, 3])
    issues = check_headings(som, URL)
    assert issues == []


def test_multiple_h1():
    som = _som_with_headings([1, 1, 2])
    issues = check_headings(som, URL)
    assert len(issues) == 1
    assert issues[0]["rule"] == "multiple-h1"


def test_no_h1_but_has_h2():
    som = _som_with_headings([2, 3])
    issues = check_headings(som, URL)
    assert len(issues) == 1
    assert issues[0]["rule"] == "no-h1"


# --- check_links ---

def test_links_with_text():
    som = {"regions": [{"elements": [
        {"role": "link", "text": "Click here", "attrs": {"href": "/page"}},
    ]}]}
    issues = check_links(som, URL)
    assert issues == []


def test_empty_links():
    som = {"regions": [{"elements": [
        {"role": "link", "text": "", "attrs": {"href": "/page"}},
        {"role": "link", "text": "  ", "attrs": {"href": "/other"}},
    ]}]}
    issues = check_links(som, URL)
    assert len(issues) == 1
    assert issues[0]["rule"] == "empty-links"
    assert "2 links" in issues[0]["message"]


# --- check_content_length ---

def test_thin_content():
    som = {"regions": [{"elements": [
        {"text": "Short."},
    ]}]}
    issues = check_content_length(som, URL)
    assert len(issues) == 1
    assert issues[0]["rule"] == "thin-content"


def test_sufficient_content():
    som = {"regions": [{"elements": [
        {"text": "x" * 200},
    ]}]}
    issues = check_content_length(som, URL)
    assert issues == []


# --- check_images ---

def test_images_with_alt():
    som = {"regions": [{"elements": [
        {"role": "image", "attrs": {"alt": "A photo"}},
    ]}]}
    issues = check_images(som, URL)
    assert issues == []


def test_images_missing_alt():
    som = {"regions": [{"elements": [
        {"role": "image", "attrs": {}},
        {"role": "image", "attrs": {"alt": ""}},
        {"role": "image", "attrs": {"alt": "OK"}},
    ]}]}
    issues = check_images(som, URL)
    assert len(issues) == 1
    assert issues[0]["rule"] == "images-no-alt"
    assert "2/3" in issues[0]["message"]


# --- ALL_CHECKS ---

def test_all_checks_returns_list():
    assert len(ALL_CHECKS) == 5
    som = {"title": "Good Title Here", "regions": [{"elements": [
        {"role": "heading", "attrs": {"level": 1}, "text": "Hello"},
        {"text": "x" * 200},
    ]}]}
    for check in ALL_CHECKS:
        result = check(som, URL)
        assert isinstance(result, list)
