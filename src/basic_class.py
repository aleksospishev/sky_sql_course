from abc import ABC, abstractmethod


class BasicManager(ABC):
    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self, keyword: str):
        pass


class APIBasic(ABC):
    @abstractmethod
    def check_existence(self):
        pass

    @abstractmethod
    def load_vacancy_by_emp_id(self):
        pass
