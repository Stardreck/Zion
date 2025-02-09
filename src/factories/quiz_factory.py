from typing import Any, Dict
from src.models.quiz import Quiz


class QuizFactory:
    @staticmethod
    def create_quiz(quiz_data: Dict[str, Any]) -> Quiz:
        """
        Create a Quiz instance from dictionary data.

        Expected keys in quiz_data:
            - "question": str
            - "answers": list[str] (die Antwortoptionen)
            - "correct_answer": Optional[str]
            - "type": Optional[str]

        :param quiz_data: Dictionary mit Quiz-Daten.
        :return: Ein Quiz-Objekt.
        """
        return Quiz(
            question=quiz_data.get("question", ""),
            answer_options=quiz_data.get("answers", []),
            correct_answer=quiz_data.get("correct_answer_position"),
            quiz_type=quiz_data.get("type", "quiz")
        )
