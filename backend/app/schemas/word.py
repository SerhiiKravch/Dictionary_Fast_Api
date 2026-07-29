from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.enums import (
    DifficultyLevel,
    InflectionType,
    LanguageCode,
    PartOfSpeech,
    RelationType,
    WordOrigin,
)
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


class ExampleSentenceCreate(BaseModel):
    source_text: str = Field(min_length=1)
    translated_text: str = Field(default="")
    position: int = Field(default=1, ge=1)

    @field_validator("source_text", "translated_text")
    @classmethod
    def strip_text_fields(cls, value: str) -> str:
        return value.strip()


class WordSenseCreate(BaseModel):
    part_of_speech: PartOfSpeech = PartOfSpeech.OTHER
    primary_translation: str = Field(min_length=1, max_length=256)
    definition: str = Field(default="")
    position: int = Field(default=1, ge=1)
    example_sentences: list[ExampleSentenceCreate] = Field(default_factory=list)

    @field_validator("primary_translation", "definition")
    @classmethod
    def strip_text_fields(cls, value: str) -> str:
        return value.strip()


class GeneratedWordPayload(BaseModel):
    model_config = ConfigDict(use_enum_values=False)

    source_word: str = Field(min_length=1, max_length=128)
    source_language: LanguageCode
    target_language: LanguageCode
    transcription: str = Field(min_length=1, max_length=128)
    primary_translation: str | None = Field(default=None, min_length=1, max_length=256)
    context_sentence: str | None = Field(default=None, min_length=1)
    difficulty_level: DifficultyLevel | None = None
    origin: WordOrigin = WordOrigin.OPENAI
    tags: list[str] = Field(default_factory=list, max_length=20)
    inflections: list["WordInflectionCreate"] = Field(default_factory=list)
    senses: list[WordSenseCreate] = Field(default_factory=list)
    translation_options: list[GeneratedTranslationOption] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        return [validate_tag_name(tag) for tag in value]

    @model_validator(mode="after")
    def validate_inflection_uniqueness(self) -> "GeneratedWordPayload":
        ensure_unique_inflection_types(self.inflections)
        self.tags = normalize_tags(self.tags)
        apply_legacy_sense_compatibility(self)
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
    primary_translation: str | None = Field(default=None, min_length=1, max_length=256)
    context_sentence: str | None = Field(default=None, min_length=1)
    difficulty_level: DifficultyLevel | None = None
    origin: WordOrigin = WordOrigin.MANUAL
    tags: list[str] = Field(default_factory=list, max_length=20)
    inflections: list[WordInflectionCreate] = Field(default_factory=list)
    senses: list[WordSenseCreate] = Field(default_factory=list)
    translation_options: list[TranslationOptionCreate] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        return [validate_tag_name(tag) for tag in value]

    @model_validator(mode="after")
    def validate_inflection_uniqueness(self) -> "WordCreate":
        ensure_unique_inflection_types(self.inflections)
        self.tags = normalize_tags(self.tags)
        apply_legacy_sense_compatibility(self)
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


class ExampleSentenceRead(BaseModel):
    id: int
    source_text: str
    translated_text: str
    position: int

    model_config = ConfigDict(from_attributes=True)


class WordSenseRead(BaseModel):
    id: int
    part_of_speech: PartOfSpeech
    primary_translation: str
    definition: str
    position: int
    example_sentences: list[ExampleSentenceRead]

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
    senses: list[WordSenseRead]
    translation_options: list[TranslationOptionRead]

    model_config = ConfigDict(from_attributes=True)


class WordListResponse(BaseModel):
    items: list[WordRead]
    total: int
    limit: int
    offset: int


class WordRelationCreate(BaseModel):
    target_word_id: int = Field(ge=1)
    relation_type: RelationType
    notes: str = Field(default="", max_length=255)

    @field_validator("notes")
    @classmethod
    def strip_notes(cls, value: str) -> str:
        return value.strip()


class RelatedWordSummary(BaseModel):
    id: int
    slug: str
    source_word: str
    source_language: LanguageCode
    target_language: LanguageCode
    primary_translation: str

    model_config = ConfigDict(from_attributes=True)


class WordRelationRead(BaseModel):
    id: int
    relation_type: RelationType
    notes: str
    related_word: RelatedWordSummary


class WordRelationListResponse(BaseModel):
    items: list[WordRelationRead]


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


def ensure_unique_sense_positions(senses: list[WordSenseCreate]) -> None:
    seen: set[int] = set()
    duplicates: set[int] = set()

    for sense in senses:
        if sense.position in seen:
            duplicates.add(sense.position)
            continue
        seen.add(sense.position)

    if duplicates:
        duplicate_list = ", ".join(str(position) for position in sorted(duplicates))
        raise ValueError(f"Duplicate sense positions are not allowed: {duplicate_list}.")


def ensure_unique_example_positions(senses: list[WordSenseCreate]) -> None:
    for sense in senses:
        seen: set[int] = set()
        duplicates: set[int] = set()
        for example in sense.example_sentences:
            if example.position in seen:
                duplicates.add(example.position)
                continue
            seen.add(example.position)
        if duplicates:
            duplicate_list = ", ".join(str(position) for position in sorted(duplicates))
            raise ValueError(
                f"Duplicate example positions are not allowed for sense {sense.position}: "
                f"{duplicate_list}."
            )


def apply_legacy_sense_compatibility(payload: GeneratedWordPayload | WordCreate) -> None:
    ensure_unique_sense_positions(payload.senses)
    ensure_unique_example_positions(payload.senses)

    if payload.senses:
        first_sense = min(payload.senses, key=lambda sense: sense.position)
        payload.primary_translation = first_sense.primary_translation
        if first_sense.example_sentences:
            first_example = min(first_sense.example_sentences, key=lambda item: item.position)
            payload.context_sentence = first_example.source_text
        elif payload.context_sentence is None:
            payload.context_sentence = first_sense.primary_translation
        return

    if payload.primary_translation is None or payload.context_sentence is None:
        raise ValueError("Either provide senses or both primary_translation and context_sentence.")

    payload.senses = [
        WordSenseCreate(
            part_of_speech=PartOfSpeech.OTHER,
            primary_translation=payload.primary_translation,
            definition="",
            position=1,
            example_sentences=[
                ExampleSentenceCreate(
                    source_text=payload.context_sentence,
                    translated_text="",
                    position=1,
                )
            ],
        )
    ]
