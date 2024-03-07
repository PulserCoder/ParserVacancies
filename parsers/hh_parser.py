from typing import Optional, List

import requests
from dotenv import load_dotenv

from parsers.abc_parser import ParserVacanciesABC
from parsers.super_job_parser import Vacancy


class HeadHunterParser(ParserVacanciesABC):
    load_dotenv()
    url = "https://api.hh.ru"

    def get_vacancies(self, text: Optional[str] = None) -> List[Vacancy]:
        params = {}
        if text is not None:
            params = {
                'text': text,
                'only_with_salary': 'true'
            }

        all_vacancies = []
        data = requests.get(f"{HeadHunterParser.url}/vacancies", params=params).json()
        for el in data['items']:
            vacancy = Vacancy()
            vacancy.id = el.get('id')
            vacancy.name = el.get('name', '')
            vacancy.description = el.get('description', '')
            salary = el.get("salary")
            try:
                vacancy.salary_avg = (salary.get('to', 0) + el.get('from', 0)) / 2
            except TypeError:
                continue
            all_vacancies.append(vacancy)

        return all_vacancies


