from app.models.enums import LanguageCode
from app.utils.slug import (
    build_base_slug,
    build_slug_with_suffix,
    generate_slug_suffix,
    slugify_text,
)


def test_slugify_text_normalizes_spaces() -> None:
    assert slugify_text("Ice Cream") == "ice-cream"


def test_slugify_text_removes_special_characters() -> None:
    assert slugify_text("Hello, world!!!") == "hello-world"


def test_slugify_text_collapses_multiple_dashes() -> None:
    assert slugify_text("word---with    spaces") == "word-with-spaces"


def test_slugify_text_returns_fallback_for_empty_result() -> None:
    assert slugify_text("!!!") == "word"


def test_build_base_slug_uses_languages_and_normalized_word() -> None:
    assert (
        build_base_slug(
            "Ice Cream",
            LanguageCode.ENGLISH,
            LanguageCode.UKRAINIAN,
        )
        == "ice-cream-en-uk"
    )


def test_build_slug_with_suffix_appends_suffix() -> None:
    assert build_slug_with_suffix("fixed-slug", "abc123") == "fixed-slug-abc123"


def test_generate_slug_suffix_respects_length() -> None:
    suffix = generate_slug_suffix(8)
    assert len(suffix) == 8
