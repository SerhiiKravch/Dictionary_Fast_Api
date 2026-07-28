from enum import StrEnum


class LanguageCode(StrEnum):
    ENGLISH = "en"
    UKRAINIAN = "uk"


class LookupDirection(StrEnum):
    ENGLISH_TO_UKRAINIAN = "en:uk"
    UKRAINIAN_TO_ENGLISH = "uk:en"


class WordOrigin(StrEnum):
    MANUAL = "manual"
    OPENAI = "openai"
    IMPORTED = "imported"


class PartOfSpeech(StrEnum):
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    INTERJECTION = "interjection"
    PHRASE = "phrase"
    OTHER = "other"
