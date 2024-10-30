import psycopg2
from src.basic_class import BasicManager


class DBManager(BasicManager):
    """Базовый класс для управлевления БД."""

    def __init__(self, db_name, params=None):
        """Подключение к БД."""
        self.conn = psycopg2.connect(dbname=db_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        self.cur.execute(
            """
            SELECT employer_name, COUNT(vacancies.employer_id)
            FROM employers
            INNER JOIN vacancies USING (employer_id)
            GROUP BY employer_name
            ORDER BY COUNT DESC
            """
        )
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        self.cur.execute(
            """
            SELECT v.vacancy_id, e.employer_name, a.name AS area_name, v.vacancy_name, v.salary, v.vacancy_url
            FROM vacancies v
            INNER JOIN employers e USING (employer_id)
            INNER JOIN areas a ON v.vacancy_area = a.area_id
            ORDER BY v.salary DESC
            """
        )
        return self.cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        self.cur.execute(
            """
            SELECT AVG(salary)
            FROM vacancies
            """
        )
        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        self.cur.execute(
            """
            SELECT v.vacancy_id, e.employer_name, a.name AS area_name, v.vacancy_name, v.salary, v.vacancy_url
            FROM vacancies v
            INNER JOIN employers e USING (employer_id)
            INNER JOIN areas a ON v.vacancy_area = a.area_id
            WHERE v.salary >= (SELECT AVG(salary) FROM vacancies)
            ORDER BY v.salary DESC
            """
        )
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        query = """
            SELECT v.vacancy_id, e.employer_name, a.name AS area_name, v.vacancy_name, v.salary, v.vacancy_url
            FROM vacancies v
            INNER JOIN employers e USING (employer_id)
            INNER JOIN areas a ON v.vacancy_area = a.area_id
            WHERE v.salary >= (SELECT AVG(salary) FROM vacancies)
            """

        q_params = []

        if keyword:
            query += " AND (v.vacancy_name ILIKE %s OR e.employer_name ILIKE %s OR a.name ILIKE %s)"
            q_params.extend([f"%{keyword}%"] * 3)

        query += " ORDER BY v.salary DESC"

        self.cur.execute(query, q_params)
        return self.cur.fetchall()
