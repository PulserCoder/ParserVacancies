import os
from dataclasses import dataclass, field
from typing import Optional, List

import requests
from dotenv import load_dotenv

from abc_parser import ParserVacanciesABC


@dataclass
class Vacancy:
    id: int = field(default=0)
    name: str = field(default='')
    salary_avg: int = field(default=0)
    description: str = field(default='')

    def __post_init__(self):
        if not isinstance(self.id, int) or self.id < 0:
            raise ValueError("id must be a non-negative integer")
        if not isinstance(self.name, str):
            raise ValueError("name must be a string")
        if not isinstance(self.salary_avg, int) or self.salary_avg < 0:
            raise ValueError("salary_avg must be a non-negative integer")
        if not isinstance(self.description, str):
            raise ValueError("description must be a string")

    def __eq__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_avg == other.salary_avg

    def __gt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_avg > other.salary_avg

    def __lt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_avg < other.salary_avg

    def __le__(self, other):
        return self == other or self < other

    def __ge__(self, other):
        return self == other or self > other


class SuperJobParser(ParserVacanciesABC):
    url = "https://api.superjob.ru/2.0"
    load_dotenv()
    api_key = os.environ.get("API_KEY")

    def __init__(self):
        self.headers = {
            "Host": "api.superjob.ru",
            "X-Api-App-Id": SuperJobParser.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def get_vacancies(self, text: Optional[str] = None) -> List[Vacancy]:
        params = {}
        all_vacancies = []
        if text is not None:
            params = {
                "keyword": text
            }
        respond = requests.get(f"{self.url}/vacancies/", headers=self.headers, params=params).json()
        for el in respond["objects"]:
            vacancy = Vacancy()
            vacancy.id = el.get('id')
            vacancy.name = el.get('profession', '')
            vacancy.description = el.get('candidat', '')
            vacancy.salary_avg = (el.get('payment_to', 0) + el.get('payment_from', 0)) / 2
            all_vacancies.append(vacancy)

        return all_vacancies
