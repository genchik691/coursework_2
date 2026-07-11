import json
import os
from typing import List, Optional

from src.aeroplane import Aeroplane
from src.aeroplanes_api import AeroplanesAPI
from src.json_storage import JSONStorage


def fetch_and_save_aeroplanes(country: str, storage: JSONStorage) -> List[Aeroplane]:
    """
    Получение данных о самолетах из API и сохранение в хранилище

    Args:
        country: Название страны
        storage: Экземпляр хранилища

    Returns:
        Список объектов Aeroplane
    """
    try:
        api = AeroplanesAPI()

        # Получаем данные из API
        data = api.get_aeroplanes(country)

        if not data:
            print(f"Не найдено данных о самолетах для страны '{country}'")
            return []

        # Преобразуем в объекты
        aeroplanes = Aeroplane.cast_to_object_list(data)

        if not aeroplanes:
            print("Нет корректных данных о самолетах")
            return []

        # Сохраняем в хранилище
        for aeroplane in aeroplanes:
            storage.add_aeroplane(aeroplane)

        return aeroplanes

    except ValueError as e:
        print(f"Ошибка получения данных: {e}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


def load_test_aeroplanes(storage: JSONStorage) -> List[Aeroplane]:
    """
    Загрузка тестовых данных о самолетах из файла

    Args:
        storage: Экземпляр хранилища

    Returns:
        Список объектов Aeroplane
    """
    test_file = "data/test_aeroplanes.json"

    if not os.path.exists(test_file):
        print(f"Тестовый файл {test_file} не найден")
        return []

    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Проверяем структуру данных
        if isinstance(data, dict) and 'states' in data:
            states = data.get('states', [])
        elif isinstance(data, list):
            states = data
        else:
            print("Неверный формат тестовых данных")
            return []

        aeroplanes_data = []
        for state in states:
            if state and len(state) >= 17:
                aeroplane = {
                    'icao24': state[0],
                    'callsign': state[1].strip() if state[1] else '',
                    'origin_country': state[2] if state[2] else 'Неизвестно',
                    'time_position': state[3],
                    'last_contact': state[4],
                    'longitude': state[5],
                    'latitude': state[6],
                    'baro_altitude': state[7],
                    'on_ground': state[8],
                    'velocity': state[9],
                    'true_track': state[10],
                    'vertical_rate': state[11],
                    'sensors': state[12],
                    'geo_altitude': state[13],
                    'squawk': state[14],
                    'spi': state[15],
                    'position_source': state[16]
                }
                aeroplanes_data.append(aeroplane)

        # Преобразуем в объекты и сохраняем
        aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_data)

        for aeroplane in aeroplanes:
            storage.add_aeroplane(aeroplane)

        print(f"Загружено {len(aeroplanes)} тестовых самолетов")
        return aeroplanes

    except Exception as e:
        print(f"Ошибка загрузки тестовых данных: {e}")
        return []


def filter_aeroplanes_by_country(aeroplanes: List[Aeroplane],
                                 country: str) -> List[Aeroplane]:
    """
    Фильтрация самолетов по стране регистрации

    Args:
        aeroplanes: Список самолетов
        country: Название страны для фильтрации

    Returns:
        Отфильтрованный список самолетов
    """
    if not country:
        return aeroplanes

    return [a for a in aeroplanes if country.lower() in a.origin_country.lower()]


def sort_aeroplanes_by_altitude(aeroplanes: List[Aeroplane],
                                descending: bool = True) -> List[Aeroplane]:
    """
    Сортировка самолетов по высоте

    Args:
        aeroplanes: Список самолетов
        descending: По убыванию (True) или по возрастанию (False)

    Returns:
        Отсортированный список самолетов
    """
    valid = [a for a in aeroplanes if a.altitude is not None]
    invalid = [a for a in aeroplanes if a.altitude is None]

    sorted_valid = sorted(valid, key=lambda x: x.altitude, reverse=descending)

    return sorted_valid + invalid


def sort_aeroplanes_by_velocity(aeroplanes: List[Aeroplane],
                                descending: bool = True) -> List[Aeroplane]:
    """
    Сортировка самолетов по скорости

    Args:
        aeroplanes: Список самолетов
        descending: По убыванию (True) или по возрастанию (False)

    Returns:
        Отсортированный список самолетов
    """
    valid = [a for a in aeroplanes if a.velocity is not None]
    invalid = [a for a in aeroplanes if a.velocity is None]

    sorted_valid = sorted(valid, key=lambda x: x.velocity, reverse=descending)

    return sorted_valid + invalid


def get_top_aeroplanes(aeroplanes: List[Aeroplane], n: int) -> List[Aeroplane]:
    """
    Получение топ N самолетов по высоте

    Args:
        aeroplanes: Список самолетов
        n: Количество самолетов в топе

    Returns:
        Топ N самолетов по высоте
    """
    if n <= 0:
        return []

    sorted_aeroplanes = sort_aeroplanes_by_altitude(aeroplanes, descending=True)
    return sorted_aeroplanes[:n]


def get_aeroplanes_by_altitude_range(aeroplanes: List[Aeroplane],
                                     min_alt: Optional[float] = None,
                                     max_alt: Optional[float] = None) -> List[Aeroplane]:
    """
    Получение самолетов в диапазоне высот

    Args:
        aeroplanes: Список самолетов
        min_alt: Минимальная высота
        max_alt: Максимальная высота

    Returns:
        Список самолетов в указанном диапазоне
    """
    result = aeroplanes

    if min_alt is not None:
        result = [a for a in result if a.altitude is not None and a.altitude >= min_alt]

    if max_alt is not None:
        result = [a for a in result if a.altitude is not None and a.altitude <= max_alt]

    return result


def print_aeroplanes(aeroplanes: List[Aeroplane]) -> None:
    """
    Вывод информации о самолетах в консоль

    Args:
        aeroplanes: Список самолетов
    """
    if not aeroplanes:
        print("\nНет самолетов для отображения")
        return

    print(f"\n{'=' * 80}")
    print(f"Найдено самолетов: {len(aeroplanes)}")
    print('=' * 80)

    for i, aeroplane in enumerate(aeroplanes, 1):
        status = "на земле" if aeroplane.on_ground else "в воздухе"
        print(f"{i}. {aeroplane.callsign} ({aeroplane.origin_country}) - {status}")
        print(f"   Скорость: {aeroplane.velocity if aeroplane.velocity is not None else 'Н/Д'} м/с")
        print(f"   Высота: {aeroplane.altitude if aeroplane.altitude is not None else 'Н/Д'} м")
        if aeroplane.latitude and aeroplane.longitude:
            print(f"   Координаты: {aeroplane.latitude:.4f}, {aeroplane.longitude:.4f}")
        print("-" * 80)

    print('=' * 80)


def get_aeroplanes_by_country_from_storage(storage: JSONStorage, country: str) -> List[Aeroplane]:
    """
    Получение самолетов из хранилища по стране регистрации

    Args:
        storage: Экземпляр хранилища
        country: Название страны

    Returns:
        Список самолетов
    """
    all_aeroplanes = storage.get_all_aeroplanes()
    return filter_aeroplanes_by_country(all_aeroplanes, country)
