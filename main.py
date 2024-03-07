from parsers.super_job_parser import SuperJobParser
from parsers.hh_parser import HeadHunterParser
from parsers.save_information import JobDataHandlerJSON


def interact_with_user():
    handler = JobDataHandlerJSON('vacancies.json')
    hh_parser = HeadHunterParser()
    sj_parser = SuperJobParser()

    while True:
        print("\nДоступные действия:")
        print("1. Добавить вакансию в файл")
        print("2. Показать вакансии из файла")
        print("3. Удалить вакансию из файла")
        print("4. Показать спарсенные вакансии с HeadHunter")
        print("5. Показать спарсенные вакансии с SuperJob")
        print("6. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            job_data = {}
            job_data['id'] = input("Введите ID вакансии: ")
            job_data['name'] = input("Введите название вакансии: ")
            job_data['description'] = input("Введите описание вакансии: ")
            job_data['salary'] = input("Введите зарплату: ")
            handler.add_job(job_data)
            print("Вакансия добавлена.")

        elif choice == "2":
            criteria = {}
            search_criteria = input(
                "Введите критерии поиска в формате 'ключ=значение' (оставьте пустым для показа всех вакансий): ")
            if search_criteria:
                key, value = search_criteria.split("=")
                criteria[key] = value
            vacancies = handler.get_jobs(criteria)
            print(f"Найдено вакансий: {len(vacancies)}")
            for vacancy in vacancies:
                print(vacancy)

        elif choice == "3":
            job_id = input("Введите ID вакансии для удаления: ")
            handler.delete_job(job_id)
            print("Вакансия удалена.")


        elif choice == "4" or choice == "5":
            search_query = input("Введите поисковый запрос (например, 'Python разработчик'): ")
            if choice == "4":
                vacancies = hh_parser.get_vacancies(text=search_query)
                platform_name = "HeadHunter"
            else:
                vacancies = sj_parser.get_vacancies(text=search_query)
                platform_name = "SuperJob"
            print(f"Найдено вакансий на {platform_name} по запросу '{search_query}': {len(vacancies)}")
            for vacancy in vacancies[:10]:
                print(
                    f"Название: {vacancy.name}, Средняя зарплата: {vacancy.salary_avg}, Описание: {vacancy.description[:50]}... ID: {vacancy.id}")

        elif choice == "6":
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    interact_with_user()
