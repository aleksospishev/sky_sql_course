import json
import os
from configparser import MissingSectionHeaderError, NoOptionError, NoSectionError

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def create_database(database_name: str, params: dict):
    """Создает новую БД."""
    try:
        conn = psycopg2.connect(dbname="postgres", **params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {database_name};")
        cur.execute(f"CREATE DATABASE {database_name};")
        cur.close()
        conn.close()
        with psycopg2.connect(dbname=database_name, **params) as conn:
            conn.autocommit = False
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE areas (
                        area_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        url TEXT
                    );
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE employers (
                        employer_id INTEGER PRIMARY KEY,
                        employer_name TEXT NOT NULL,
                        url TEXT,
                        open_vacancies INTEGER
                    );
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE vacancies (
                        vacancy_id INTEGER PRIMARY KEY,
                        vacancy_name VARCHAR,
                        vacancy_area INTEGER REFERENCES areas(area_id),
                        salary INTEGER,
                        employer_id INTEGER REFERENCES employers(employer_id),
                        vacancy_url VARCHAR
                    );
                    """
                )

            conn.commit()

    except psycopg2.Error as e:
        print(e)
        return False
    return True


def save_to_database(areas: dict, employers: dict, vacancies: list, dbname: str, params: dict):
    """Сохранение данных в БД."""
    try:
        with psycopg2.connect(dbname=dbname, **params) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                for area_id, area_data in areas.items():
                    cur.execute(
                        """
                        INSERT INTO areas (area_id, name, url)
                        VALUES (%s, %s, %s)
                        """,
                        (area_id, area_data.get("name"), area_data.get("url")),
                    )
                for employer_id, employer_data in employers.items():
                    cur.execute(
                        """
                        INSERT INTO employers (employer_id, employer_name, url, open_vacancies)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            employer_id,
                            employer_data.get("name"),
                            employer_data.get("url"),
                            employer_data.get("open_vacancies"),
                        ),
                    )
                for vacancy_item in vacancies:
                    cur.execute(
                        """
                        INSERT INTO vacancies(vacancy_id, vacancy_name, vacancy_area, salary, employer_id, vacancy_url)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            vacancy_item.get("id"),
                            vacancy_item.get("name"),
                            vacancy_item.get("area_id"),
                            vacancy_item.get("salary"),
                            vacancy_item.get("employer_id"),
                            vacancy_item.get("url"),
                        ),
                    )
                cur.execute(
                    """
                    UPDATE employers
                    SET open_vacancies = subquery.vacancy_count
                    FROM (
                        SELECT employer_id, COUNT (*) as vacancy_count
                        FROM vacancies
                        GROUP BY employer_id
                    ) AS subquery
                    WHERE employers.employer_id = subquery.employer_id
                    """
                )

    except psycopg2.Error:
        return False

    return True


def read_db_config() -> dict[str, str]:
    """Считывает и передает параметры БД из файла .env ."""
    try:
        db_config = {
            "host": os.getenv("host"),
            "port": os.getenv("port"),
            "user": os.getenv("user"),
            "password": os.getenv("password"),
        }
        if not all(db_config.values()):
            raise NoOptionError("postgres", "One or more required options are missing")
        return db_config

    except (FileNotFoundError, NoSectionError, NoOptionError, MissingSectionHeaderError) as e:
        print(e)
        return e


def read_employers_list(file_path: str) -> list[int]:
    """Считывет список с ID компаний."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list) and all(isinstance(item, int) for item in data):
                return data
            else:
                raise ValueError("JSON-file must contain a list of integers")

    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(e)
        return []


def fixed_width(left_text, right_text, replace_char="-", width=30):
    """Выравнивает текст по ширине заменяя пробелы."""
    text_length = len(left_text) + len(right_text)

    fill_length = width - text_length - 2
    if fill_length >= 0:
        formated_text = f"{left_text} {replace_char * fill_length} {right_text}"
        return formated_text
    else:
        return f"{left_text} {replace_char} {right_text}"


def print_vacancy_info(item, unknown: str):
    """Вывод информации о компании"""
    print(fixed_width("ID:", f"{item[0] if item[0] else unknown}", "-", 110))
    print(fixed_width("Company:", f"{item[1] if item[1] else unknown}", "-", 110))
    print(fixed_width("Area:", f"{item[2] if item[2] else unknown}", "-", 110))
    print(fixed_width("Vacancy:", f"{item[3] if item[3] else unknown}", "-", 110))
    print(fixed_width("Salary from:", f"{item[4] if item[4] else unknown}", "-", 110))
    print(fixed_width("URL:", f"{item[5] if item[5] else unknown}", "-", 110))
    print("=" * 110, "\n")
