from src import JSONStorage
from src.utils import (
    fetch_and_save_aeroplanes,
    filter_aeroplanes_by_country,
    get_top_aeroplanes,
    get_aeroplanes_by_altitude_range,
    print_aeroplanes,
    load_test_aeroplanes
)


def user_interaction():
    """
    Функция для взаимодействия с пользователем
    """
    print("=" * 60)
    print("Добро пожаловать в систему мониторинга самолетов!")
    print("=" * 60)

    storage = JSONStorage()

    # Проверяем наличие тестовых данных
    test_data = load_test_aeroplanes(storage)
    if test_data:
        print(f"Загружено {len(test_data)} тестовых самолетов")

    while True:
        print("\nВыберите действие:")
        print("1. Получить информацию о самолетах в стране (из API)")
        print("2. Показать топ N самолетов по высоте")
        print("3. Фильтровать самолеты по стране регистрации")
        print("4. Фильтровать самолеты по диапазону высот")
        print("5. Показать все сохраненные самолеты")
        print("6. Очистить сохраненные данные")
        print("7. Загрузить тестовые данные")
        print("0. Выход")

        choice = input("\nВведите номер действия: ").strip()

        if choice == '0':
            print("До свидания!")
            break

        elif choice == '1':
            try:
                country = input("Введите название страны (на английском): ").strip()
                if not country:
                    print("Название страны не может быть пустым")
                    continue

                print(f"\nПолучение данных о самолетах в {country}...")
                print("Пожалуйста, подождите...")

                aeroplanes = fetch_and_save_aeroplanes(country, storage)

                if aeroplanes:
                    print(f"Найдено и сохранено самолетов: {len(aeroplanes)}")
                    print_aeroplanes(aeroplanes)
                else:
                    print("Самолеты не найдены или данные отсутствуют")
                    print("Возможные причины:")
                    print("  - В указанной стране нет самолетов в воздушном пространстве")
                    print("  - Ошибка подключения к API")
                    print("  - Неверное название страны (используйте английское название)")
                    print("\nСовет: попробуйте выбрать действие 7 для загрузки тестовых данных")

            except ValueError as e:
                print(f"Ошибка: {e}")
            except Exception as e:
                print(f"Произошла ошибка: {e}")

        elif choice == '2':
            try:
                n = input("Введите количество самолетов для топа: ").strip()
                if not n:
                    print("Количество не может быть пустым")
                    continue

                n = int(n)
                if n <= 0:
                    print("Количество должно быть положительным")
                    continue

                aeroplanes = storage.get_all_aeroplanes()
                if not aeroplanes:
                    print("Нет сохраненных данных. Сначала получите данные о самолетах.")
                    print("Совет: выберите действие 1 или 7")
                    continue

                top = get_top_aeroplanes(aeroplanes, n)
                print(f"\nТоп {n} самолетов по высоте полета:")
                print_aeroplanes(top)

            except ValueError:
                print("Ошибка: введите корректное число")
            except Exception as e:
                print(f"Произошла ошибка: {e}")

        elif choice == '3':
            try:
                country = input("Введите страну регистрации для фильтрации: ").strip()
                if not country:
                    print("Название страны не может быть пустым")
                    continue

                aeroplanes = storage.get_all_aeroplanes()
                if not aeroplanes:
                    print("Нет сохраненных данных. Сначала получите данные о самолетах.")
                    continue

                filtered = filter_aeroplanes_by_country(aeroplanes, country)
                print(f"\nСамолеты, зарегистрированные в стране '{country}':")
                print_aeroplanes(filtered)

            except Exception as e:
                print(f"Произошла ошибка: {e}")

        elif choice == '4':
            try:
                min_alt = input("Введите минимальную высоту (м): ").strip()
                max_alt = input("Введите максимальную высоту (м): ").strip()

                min_alt = float(min_alt) if min_alt else None
                max_alt = float(max_alt) if max_alt else None

                if min_alt is None and max_alt is None:
                    print("Не указан диапазон высот")
                    continue

                if min_alt is not None and max_alt is not None and min_alt > max_alt:
                    print("Минимальная высота не может быть больше максимальной")
                    continue

                aeroplanes = storage.get_all_aeroplanes()
                if not aeroplanes:
                    print("Нет сохраненных данных. Сначала получите данные о самолетах.")
                    continue

                filtered = get_aeroplanes_by_altitude_range(aeroplanes, min_alt, max_alt)

                range_str = []
                if min_alt is not None:
                    range_str.append(f"от {min_alt} м")
                if max_alt is not None:
                    range_str.append(f"до {max_alt} м")

                print(f"\nСамолеты в диапазоне высот {' '.join(range_str)}:")
                print_aeroplanes(filtered)

            except ValueError:
                print("Ошибка: введите корректные числа")
            except Exception as e:
                print(f"Произошла ошибка: {e}")

        elif choice == '5':
            try:
                aeroplanes = storage.get_all_aeroplanes()
                if not aeroplanes:
                    print("Нет сохраненных данных")
                else:
                    print(f"\nВсе сохраненные самолеты ({len(aeroplanes)}):")
                    print_aeroplanes(aeroplanes)
            except Exception as e:
                print(f"Произошла ошибка: {e}")

        elif choice == '6':
            try:
                storage.clear()
                print("Данные успешно очищены")
            except Exception as e:
                print(f"Ошибка при очистке данных: {e}")

        elif choice == '7':
            try:
                test_aeroplanes = load_test_aeroplanes(storage)
                if test_aeroplanes:
                    print(f"Загружено {len(test_aeroplanes)} тестовых самолетов")
                    print_aeroplanes(test_aeroplanes)
                else:
                    print("Не удалось загрузить тестовые данные")
                    print("Убедитесь, что файл data/test_aeroplanes.json существует")
            except Exception as e:
                print(f"Ошибка загрузки тестовых данных: {e}")

        else:
            print("Неверный выбор. Пожалуйста, выберите действие из списка.")


if __name__ == "__main__":
    user_interaction()
