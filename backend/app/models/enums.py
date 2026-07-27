from enum import StrEnum


class LanguageCode(StrEnum):
    ENGLISH = "en"
    UKRAINIAN = "uk"


class WordOrigin(StrEnum):
    MANUAL = "manual"
    OPENAI = "openai"
    IMPORTED = "imported"


class DifficultyLevel(StrEnum):
    A1 = "a1"
    A2 = "a2"
    B1 = "b1"
    B2 = "b2"
    C1 = "c1"
    C2 = "c2"


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


class InflectionType(StrEnum):
    PLURAL = "plural"
    THIRD_PERSON_SINGULAR = "third_person_singular"
    PAST_SIMPLE = "past_simple"
    PAST_PARTICIPLE = "past_participle"
    PRESENT_PARTICIPLE = "present_participle"
    COMPARATIVE = "comparative"
    SUPERLATIVE = "superlative"
    FEMININE = "feminine"
    MASCULINE = "masculine"
    NEUTER = "neuter"


class RelationType(StrEnum):
    SYNONYM = "synonym"
    ANTONYM = "antonym"
    RELATED = "related"
