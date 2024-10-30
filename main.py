from src.DBManager import DBManager
from src.api_connect import HHAPIClient
from src.utils import (
    read_employers_list,
    read_db_config,
    create_database,
    save_to_database,
    fixed_width,
    print_vacancy_info,
)

import os

commands = [
    ("Company", "Получить список всех компаний и количество вакансий у каждой компании."),
    ("All", "Получить список всех вакансий с названием компании, названим вакансии, зарплаты и ссылки на вакансию."),
    ("Avg", "Получить среднюю зарплату по вакансиям."),
    ("Avg-hi", "Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям."),
    ("Word", "Получить список всех вакансий, в названии которых содержатся переданные в метод слова."),
    ("End", "Завершить поиск."),
]


def main() -> bool:
    """Main function"""
    params = read_db_config()
    db_name = "vacancies"
    create_database(db_name, params)
    emp_ids_path = os.path.abspath("./data/employer_id")
    employers_list = read_employers_list(emp_ids_path)
    hh_client = HHAPIClient()
    hh_client.load_vacancies_by_emp_ids(employers_list)
    areas = hh_client.get_areas()
    employers = hh_client.get_employers()
    vacancies = hh_client.get_vacancies()
    save_to_database(areas, employers, vacancies, db_name, params)
    db_manager = DBManager(db_name, params)

    while True:
        print("Выберите действие:")
        for command in commands:
            print(fixed_width(f"'{command[0]}'", f"{command[1]}", "_", 110))
        user_input = input("\n")
        if user_input.lower() == "end":
            return True
        elif user_input.lower() == "company":
            vacancies_count = db_manager.get_companies_and_vacancies_count()
            for item in vacancies_count:
                print(fixed_width(f"Employer: {item[0]}", f"Vacancies: {item[1]}", "-", 110))
            print("=" * 110, "\n")
        elif user_input.lower() == "all":
            all_vacancies = db_manager.get_all_vacancies()
            for item in all_vacancies:
                print_vacancy_info(item, "~Unknown~")

        elif user_input.lower() == "avg":
            avg_sal = db_manager.get_avg_salary()
            print(
                fixed_width("Средняя зарплата:", f"{round(avg_sal[0][0]) if avg_sal[0][0] else '-Unknown-'}", "_", 110)
            )
            print("=" * 110, "\n")

        elif user_input.lower() == "avg-hi":
            higher_than_avg_vacancies = db_manager.get_vacancies_with_higher_salary()
            for item in higher_than_avg_vacancies:
                print_vacancy_info(item, "~Unknown~")

        elif user_input.lower() == "word":
            keyword = input("Введите ключевое слово для поиска: ")
            keyw_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            if len(keyw_vacancies) > 0:
                for item in keyw_vacancies:
                    print_vacancy_info(item, "~Unknown~")
                print()
            else:
                print("Ничего не найдено")
                print("=" * 110, "\n")
        else:
            print("Вы ввели неверное значение.")
            print("=" * 110, "\n")


if __name__ == "__main__":
    main()
