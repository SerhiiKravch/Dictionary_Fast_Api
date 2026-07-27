from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.enums import DifficultyLevel, InflectionType, LanguageCode, PartOfSpeech, WordOrigin
from app.services.word_metadata_service import MAX_TAG_LENGTH, normalize_tags, validate_tag_name


class WordLookupRequest(BaseModel):
    word: str = Field(min_length=1, max_length=128)
    direction: str = "en:uk"


class AutocompleteItem(BaseModel):
    value: str


class AutocompleteResponse(BaseModel):
    results: list[str]


class GeneratedTranslationOption(BaseModel):
    text: str = Field(min_length=1, max_length=256)
    part_of_speech: PartOfSpeech = PartOfSpeech.OTHER
    priority: int = Field(default=1, ge=1)
    usage_note: str = Field(default="", max_length=255)


class GeneratedWordPayload(BaseModel):
    model_config = ConfigDict(use_enum_values=False)

    source_word: str = Field(min_length=1, max_length=128)
    source_language: LanguageCode
    target_language: LanguageCode
    transcription: str = Field(min_length=1, max_length=128)
    primary_translation: str = Field(min_length=1, max_length=256)
    context_sentence: str = Field(min_length=1)
    difficulty_level: DifficultyLevel | None = None
    origin: WordOrigin = WordOrigin.OPENAI
    tags: list[str] = Field(default_factory=list, max_length=20)
    inflections: list["WordInflectionCreate"] = Field(default_factory=list)
    translation_options: list[GeneratedTranslationOption] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        return [validate_tag_name(tag) for tag in value]

    @model_validator(mode="after")
    def validate_inflection_uniqueness(self) -> "GeneratedWordPayload":
        ensure_unique_inflection_types(self.inflections)
        self.tags = normalize_tags(self.tags)
        return self


class TranslationOptionCreate(BaseModel):
    text: str = Field(min_length=1, max_length=256)
    part_of_speech: PartOfSpeech = PartOfSpeech.OTHER
    priority: int = Field(default=1, ge=1)
    usage_note: str = Field(default="", max_length=255)


class WordInflectionCreate(BaseModel):
    form_type: InflectionType
    value: str = Field(min_length=1, max_length=128)
    notes: str = Field(default="", max_length=255)

    @field_validator("value", "notes")
    @classmethod
    def strip_text_fields(cls, value: str) -> str:
        return value.strip()


class WordCreate(BaseModel):
    source_word: str = Field(min_length=1, max_length=128)
    source_language: LanguageCode
    target_language: LanguageCode
    transcription: str = Field(min_length=1, max_length=128)
    primary_translation: str = Field(min_length=1, max_length=256)
    context_sentence: str = Field(min_length=1)
    difficulty_level: DifficultyLevel | None = None
    origin: WordOrigin = WordOrigin.MANUAL
    tags: list[str] = Field(default_factory=list, max_length=20)
    inflections: list[WordInflectionCreate] = Field(default_factory=list)
    translation_options: list[TranslationOptionCreate] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        return [validate_tag_name(tag) for tag in value]

    @model_validator(mode="after")
    def validate_inflection_uniqueness(self) -> "WordCreate":
        ensure_unique_inflection_types(self.inflections)
        self.tags = normalize_tags(self.tags)
        return self


class TranslationOptionRead(BaseModel):
    id: int
    text: str
    part_of_speech: PartOfSpeech
    priority: int
    usage_note: str

    model_config = ConfigDict(from_attributes=True)


class TagRead(BaseModel):
    id: int
    name: str = Field(max_length=MAX_TAG_LENGTH)

    model_config = ConfigDict(from_attributes=True)


class WordInflectionRead(BaseModel):
    id: int
    form_type: InflectionType
    value: str
    notes: str

    model_config = ConfigDict(from_attributes=True)


class WordRead(BaseModel):
    id: int
    source_word: str
    source_language: LanguageCode
    target_language: LanguageCode
    slug: str
    transcription: str
    primary_translation: str
    context_sentence: str
    difficulty_level: DifficultyLevel | None
    origin: WordOrigin
    created_at: datetime
    updated_at: datetime
    tags: list[TagRead]
    inflections: list[WordInflectionRead]
    translation_options: list[TranslationOptionRead]

    model_config = ConfigDict(from_attributes=True)


class WordListResponse(BaseModel):
    items: list[WordRead]
    total: int
    limit: int
    offset: int


def ensure_unique_inflection_types(inflections: list[WordInflectionCreate]) -> None:
    seen: set[InflectionType] = set()
    duplicates: set[str] = set()

    for inflection in inflections:
        if inflection.form_type in seen:
            duplicates.add(inflection.form_type.value)
            continue
        seen.add(inflection.form_type)

    if duplicates:
        duplicate_list = ", ".join(sorted(duplicates))
        raise ValueError(f"Duplicate inflection types are not allowed: {duplicate_list}.")
