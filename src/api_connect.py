import requests

from src.basic_class import APIBasic


class HHAPIClient(APIBasic):
    """Клиент для получения данных из публичного API hh.ru"""

    BASE_URL = "https://api.hh.ru/vacancies"
    EMPLOYER_URL = "https://api.hh.ru/employers"

    def __init__(self):
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"per_page": 100, "page": 0, "only_with_salary": True}
        self.data = []

    def load_vacancy_by_emp_id(self, employer_id):
        """Загружает вакансии по одному работодателю"""
        employer_id = self.valid_id(employer_id)
        self.check_existence(employer_id)
        self.params["employer_id"] = employer_id
        self.params["page"] = 0
        while True:
            try:
                response = requests.get(self.BASE_URL, headers=self.headers, params=self.params)
                response.raise_for_status()
                data = response.json()
                vacancies = data["items"]
                self.data.extend(vacancies)
                if self.params["page"] >= data["pages"] - 1:
                    break
                self.params["page"] += 1
            except requests.RequestException:
                break

    def load_vacancies_by_emp_ids(self, emp_ids: list[int]):
        """Загружает вакансии по списку работодателей"""
        for employer_id in emp_ids:
            self.load_vacancy_by_emp_id(employer_id)

    @staticmethod
    def valid_id(employer_id):
        """Проверяет идентификатор работодателя"""
        if isinstance(employer_id, int) and employer_id > 0:
            return employer_id
        raise ValueError("Invalid employer ID")

    @staticmethod
    def check_existence(employer_id):
        """Проверяет, существует ли работодатель_id на hh.ru"""
        url = f"{HHAPIClient.EMPLOYER_URL}/{employer_id}"
        response = requests.get(url)
        print(employer_id)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            raise ValueError("Employer ID does not exist")
        else:
            raise ValueError("Failed to check employer ID")

    def get_info(self):
        return self.data

    def get_areas(self):
        """Возвращает список областей в полученных данных"""
        areas = {}
        for vacancy in self.data:
            area = vacancy.get("area")
            area_id = area.get("id")
            if area_id not in areas:
                areas[area_id] = {"name": area.get("name"), "url": area.get("url")}
        return areas

    def get_employers(self):
        """Возвращает список работодателей в полученных данных"""
        employers = {}
        for vacancy in self.data:
            employer = vacancy.get("employer")
            employer_id = employer.get("id")

            if employer_id not in employers:
                employers[employer_id] = {
                    "name": employer.get("name"),
                    "url": employer.get("url"),
                    "open_vacancies": 0,
                }
        return employers

    def get_vacancies(self):
        """Возвращает список работодателей в полученных данных"""
        vacancies_list = []
        for vacancy in self.data:
            salary = vacancy.get("salary", {})
            salary_from = salary.get("from")
            vacancies_list.append(
                {
                    "id": int(vacancy.get("id")),
                    "name": vacancy.get("name"),
                    "area_id": int(vacancy.get("area", {"id": None}).get("id")),
                    "salary": salary_from,
                    "employer_id": int(vacancy.get("employer").get("id")),
                    "url": vacancy.get("url"),
                }
            )
        return vacancies_list
