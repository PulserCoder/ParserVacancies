from abc import ABC, abstractmethod


class ParserVacanciesABC(ABC):

    @abstractmethod
    def get_vacancies(self, text: str):
        pass