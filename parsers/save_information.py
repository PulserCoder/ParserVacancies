import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict


class JobDataHandlerABC(ABC):

    @abstractmethod
    def add_job(self, job_data: Dict):
        pass

    @abstractmethod
    def get_jobs(self, criteria: Dict) -> List[Dict]:
        pass

    @abstractmethod
    def delete_job(self, job_id: str):
        pass


class JobDataHandlerJSON(JobDataHandlerABC):
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.filepath.touch(exist_ok=True)

    def _read_data(self) -> List[Dict]:
        with open(self.filepath, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def _write_data(self, data: List[Dict]):
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_job(self, job_data: Dict):
        data = self._read_data()
        data.append(job_data)
        self._write_data(data)

    def get_jobs(self, criteria: Dict) -> List[Dict]:
        data = self._read_data()
        if not criteria:
            return data
        filtered_data = [job for job in data if all(job.get(key) == value for key, value in criteria.items())]
        return filtered_data

    def delete_job(self, job_id: str):
        data = self._read_data()
        data = [job for job in data if job.get('id') != job_id]
        self._write_data(data)
