import re
import secrets

from app.models.enums import LanguageCode

_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
_MULTI_DASH_RE = re.compile(r"-{2,}")


def slugify_text(value: str) -> str:
    normalized = value.strip().lower()
    normalized = _NON_ALNUM_RE.sub("-", normalized)
    normalized = _MULTI_DASH_RE.sub("-", normalized)
    return normalized.strip("-") or "word"


def build_base_slug(
    source_word: str,
    source_language: LanguageCode,
    target_language: LanguageCode,
) -> str:
    normalized_word = slugify_text(source_word)
    return f"{normalized_word}-{source_language.value}-{target_language.value}"


def build_slug_with_suffix(base_slug: str, suffix: str | None = None) -> str:
    if suffix is None:
        return base_slug
    return f"{base_slug}-{suffix}"


def generate_slug_suffix(length: int = 6) -> str:
    return secrets.token_hex(length // 2 + length % 2)[:length]
