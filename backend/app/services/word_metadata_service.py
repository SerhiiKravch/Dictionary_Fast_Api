from collections.abc import Sequence

from app.models.word import Tag

MAX_TAG_LENGTH = 32


def normalize_tag_name(tag: str) -> str:
    return tag.strip().lower()


def validate_tag_name(tag: str) -> str:
    normalized = normalize_tag_name(tag)
    if not normalized:
        raise ValueError("Tag cannot be empty.")
    if len(normalized) > MAX_TAG_LENGTH:
        raise ValueError(f"Tag cannot be longer than {MAX_TAG_LENGTH} characters.")
    if not normalized.replace("-", "").replace("_", "").isalnum():
        raise ValueError("Tag may contain only letters, digits, hyphens, and underscores.")
    return normalized


def normalize_tags(tags: Sequence[str]) -> list[str]:
    normalized_tags: list[str] = []
    seen: set[str] = set()

    for tag in tags:
        normalized = validate_tag_name(tag)
        if normalized in seen:
            continue
        seen.add(normalized)
        normalized_tags.append(normalized)

    return sorted(normalized_tags)


def get_or_create_tags(existing_tags: Sequence[Tag], requested_tags: Sequence[str]) -> list[Tag]:
    normalized_tags = normalize_tags(requested_tags)
    existing_tags_by_name = {tag.name: tag for tag in existing_tags}
    resolved_tags = list(existing_tags)

    for tag_name in normalized_tags:
        if tag_name not in existing_tags_by_name:
            tag = Tag(name=tag_name)
            existing_tags_by_name[tag_name] = tag
            resolved_tags.append(tag)

    return resolved_tags
