from typing import List, Optional

class Quiz:
    """
    Model representing a quiz.

    Attributes:
        question: The quiz question text.
        answer_options: A list of possible answers.
        correct_answer: (Optional) The correct answer.
        quiz_type: The type of quiz (default: "quiz").
    """

    def __init__(self, question: str, answer_options: List[str],
                 correct_answer: Optional[str] = None, quiz_type: str = "quiz"):
        self.question = question
        self.answer_options = answer_options
        self.correct_answer = correct_answer
        self.quiz_type = quiz_type
