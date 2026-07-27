from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import DifficultyLevel, InflectionType, LanguageCode, PartOfSpeech, WordOrigin


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


class TranslationOptionCreate(BaseModel):
    text: str = Field(min_length=1, max_length=256)
    part_of_speech: PartOfSpeech = PartOfSpeech.OTHER
    priority: int = Field(default=1, ge=1)
    usage_note: str = Field(default="", max_length=255)


class WordInflectionCreate(BaseModel):
    form_type: InflectionType
    value: str = Field(min_length=1, max_length=128)
    notes: str = Field(default="", max_length=255)


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


class TranslationOptionRead(BaseModel):
    id: int
    text: str
    part_of_speech: PartOfSpeech
    priority: int
    usage_note: str

    model_config = ConfigDict(from_attributes=True)


class TagRead(BaseModel):
    id: int
    name: str

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
