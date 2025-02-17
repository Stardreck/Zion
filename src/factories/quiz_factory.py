from typing import Any, Dict
from src.models.quiz import Quiz


class QuizFactory:
    @staticmethod
    def create_quiz(quiz_data: Dict[str, Any]) -> Quiz:
        """
        Create a Quiz instance from dictionary data.

        Expected keys in quiz_data:
            - "question": str
            - "answers": list[str]
            - "correct_answer": Optional[str]
            - "type": Optional[str]

        :param quiz_data: Dictionary of quiz data.
        :return: A Quiz instance
        """
        quiz_type = quiz_data.get("type", "quiz")
        if quiz_type == "quiz":
            return Quiz(
                question=quiz_data.get("question", ""),
                answer_options=quiz_data.get("answers", []),
                correct_answer=quiz_data.get("correct_answer_position"),
                solution=quiz_data.get("solution"),
                quiz_type="quiz",
            )
        elif quiz_type == "task":
            return Quiz(
                question=quiz_data.get("question", ""),
                answer_options=[],
                correct_answer=quiz_data.get("correct_value"),
                solution=quiz_data.get("solution"),
                quiz_type="task"
            )
        elif quiz_type == "boolean":
            return Quiz(
                question=quiz_data.get("question", ""),
                answer_options=[],
                correct_answer=quiz_data.get("correct_value"),
                solution=quiz_data.get("solution"),
                quiz_type="boolean"
            )
        else:
            raise Exception(f"Unknown quiz type: {quiz_type}")
