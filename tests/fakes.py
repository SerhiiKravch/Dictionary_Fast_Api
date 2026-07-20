from __future__ import annotations

from app.models.enums import PartOfSpeech, WordOrigin
from app.schemas.word import GeneratedTranslationOption, GeneratedWordPayload


class FakeOpenAIService:
    def generate_word_payload(self, word, source_language, target_language):
        return GeneratedWordPayload(
            source_word=word,
            source_language=source_language,
            target_language=target_language,
            transcription="[test]",
            primary_translation="тест",
            context_sentence="test sentence",
            origin=WordOrigin.OPENAI,
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
