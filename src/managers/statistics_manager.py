from src.managers.manager import Manager
from src.models.quiz import Quiz


class StatisticsManager(Manager):
    def __init__(self):
        super().__init__()
        # Counters for multiple-choice quizzes
        self.quiz_correct_count: int = 0
        self.quiz_incorrect_count: int = 0
        # Counters for task-type quizzes
        self.task_correct_count: int = 0
        self.task_incorrect_count: int = 0

    def record_quiz_task_result(self, quiz: Quiz, correct: bool) -> None:
        ##### quiz #####
        if quiz.quiz_type == "quiz":
            if correct:
                self.quiz_correct_count += 1
            else:
                self.quiz_incorrect_count += 1

        ##### task #####
        if quiz.quiz_type == "task":
            if correct:
                self.task_correct_count += 1
            else:
                self.task_incorrect_count += 1


    def get_total_correct(self):
        return self.quiz_correct_count + self.task_correct_count


    def reset_statistics(self) -> None:
        """
        Reset all statistics counters to zero.
        """
        self.quiz_correct_count = 0
        self.quiz_incorrect_count = 0
        self.task_correct_count = 0
        self.task_incorrect_count = 0