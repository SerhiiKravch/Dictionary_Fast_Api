from __future__ import annotations

from app.models.enums import PartOfSpeech, WordOrigin
from app.schemas.word import (
    ExampleSentenceCreate,
    GeneratedTranslationOption,
    GeneratedWordPayload,
    WordSenseCreate,
)


class FakeOpenAIService:
    def generate_word_payload(self, word, source_language, target_language):
        return GeneratedWordPayload(
            source_word=word,
            source_language=source_language,
            target_language=target_language,
            transcription="[test]",
            primary_translation=None,
            context_sentence=None,
            origin=WordOrigin.OPENAI,
            senses=[
                WordSenseCreate(
                    part_of_speech=PartOfSpeech.NOUN,
                    primary_translation="тест",
                    definition="generated test meaning",
                    position=1,
                    example_sentences=[
                        ExampleSentenceCreate(
                            source_text="test sentence",
                            translated_text="тестове речення",
                            position=1,
                        )
                    ],
                )
            ],
            translation_options=[
                GeneratedTranslationOption(
                    text="тест",
                    part_of_speech=PartOfSpeech.NOUN,
                    priority=1,
                    usage_note="",
                )
            ],
        )


class FailingOpenAIService:
    def __init__(self) -> None:
        raise AssertionError("OpenAIService should not be called when word already exists")
