from __future__ import annotations

import random
from typing import TYPE_CHECKING, Optional

from src.managers.manager import Manager
from src.models.quiz import Quiz
from src.views.quiz.boolean_view import BooleanView
from src.views.quiz.error_view import ErrorView
from src.views.quiz.quiz_view import QuizView
from src.views.quiz.task_view import TaskView

if TYPE_CHECKING:
    from src.games.story_game import StoryGame


class QuizManager(Manager):
    """
    Manages quizzes and tasks within the StoryGame.
    """

    def __init__(self, game: StoryGame) -> None:
        """
        Initialize the QuizManager with a reference to the StoryGame instance.
        :param game: The StoryGame instance.
        """
        super().__init__()
        self.game: StoryGame = game
        self.tolerance = self.game.engine.config.quiz_tolerance
        self.is_last_quiz_correct: bool = False

    def run_general_field_action(self):
        quiz = self.get_random_quiz_for_planet("default")
        print("[QuizManager] selected quiz_type: ", quiz.quiz_type)

        if quiz.quiz_type == "quiz":
            self.run_quiz(quiz)
        if quiz.quiz_type == "task":
            self.run_task(quiz)
        if quiz.quiz_type == "boolean":
            self.run_boolean(quiz)

        ##### update statistics #####
        self.game.statistics_manager.record_quiz_task_result(quiz, self.is_last_quiz_correct)

        ##### #####

        # display error view (Nachhilfeunterricht)
        if not self.is_last_quiz_correct:
            self.run_error(quiz)

    def run_quiz(self, quiz: Quiz):
        view = QuizView(self.game, quiz)
        view.run()

    def run_task(self, quiz: Quiz):
        view = TaskView(self.game, quiz)
        view.run()

    def run_boolean(self, quiz: Quiz):
        view = BooleanView(self.game, quiz)
        view.run()

    def run_error(self, quiz: Quiz):
        view = ErrorView(self.game, quiz)
        view.run()

    def process_submit(self, quiz: Quiz, user_input: str | bool):
        is_correct = self.__is_user_input_correct(quiz, user_input)

        if is_correct:
            print("[QuizManager] correct answer")
        else:
            print("[QuizManager] wrong answer")
            print("[QuizManager] user answer: ", user_input)
            print("[QuizManager] correct answer would be: ", quiz.correct_answer)

        self.is_last_quiz_correct = is_correct

    def __is_user_input_correct(self, quiz: Quiz, user_input: str | bool):
        """
        Process user input and determine if the answer is correct.
        :param user_input: User's input as a string.
        :param quiz: the quiz or task data
        :return: True if the input is processed successfully, False otherwise.
        """
        try:
            is_correct = False
            if quiz.quiz_type == "task":
                user_value = float(user_input)
                is_correct = abs(user_value - float(quiz.correct_answer)) <= self.tolerance
            if quiz.quiz_type == "quiz":
                is_correct = int(user_input) == quiz.correct_answer
            if quiz.quiz_type == "boolean":
                is_correct = bool(user_input) == quiz.correct_answer

            return is_correct
        except ValueError:
            return False

    def get_random_quiz_for_planet(self, planet_name: str) -> Optional[Quiz]:
        """
        Retrieve a random quiz for the specified planet.
        :param planet_name: Name of the planet.
        :return: A Quiz object or None.
        """
        quizzes = self.game.planet_quizzes_current.get(planet_name)
        if not quizzes:
            # Reload quizzes if none available
            self.game.planet_quizzes_current[planet_name] = list(self.game.data.planet_quizzes.get(planet_name, []))
            quizzes = self.game.planet_quizzes_current[planet_name]

        if quizzes:
            return quizzes.pop(random.randint(0, len(quizzes) - 1))
        return None
