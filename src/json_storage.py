import json
import os
from typing import Any, Dict, List

from src.abstract_storage import AbstractStorage
from src.aeroplane import Aeroplane


class JSONStorage(AbstractStorage):
    """Класс для сохранения информации о самолетах в JSON файл"""

    def __init__(self, file_path: str = "data/aeroplanes.json"):
        """
        Инициализация JSON хранилища

        Args:
            file_path: Путь к JSON файлу
        """
        self.file_path = file_path
        self._ensure_directory_exists()
        self._ensure_file_exists()

    def _ensure_directory_exists(self) -> None:
        """Создание директории для файла, если её нет"""
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def _ensure_file_exists(self) -> None:
        """Создание файла, если его нет"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _read_file(self) -> List[Dict[str, Any]]:
        """Чтение данных из файла"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_file(self, data: List[Dict[str, Any]]) -> None:
        """Запись данных в файл"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """
        Добавление информации о самолете в файл
        """
        data = self._read_file()

        # Проверяем, есть ли уже такой самолет
        for item in data:
            if item.get('callsign') == aeroplane.callsign:
                return

        # Добавляем новый самолет
        aeroplane_dict = {
            'callsign': aeroplane.callsign,
            'origin_country': aeroplane.origin_country,
            'velocity': aeroplane.velocity,
            'altitude': aeroplane.altitude,
            'icao24': aeroplane.icao24,
            'longitude': aeroplane.longitude,
            'latitude': aeroplane.latitude,
            'on_ground': aeroplane.on_ground
        }
        data.append(aeroplane_dict)
        self._write_file(data)

    def get_aeroplanes(self, **filters) -> List[Aeroplane]:
        """
        Получение информации о самолетах по критериям
        """
        data = self._read_file()
        aeroplanes = []

        for item in data:
            # Проверяем соответствие фильтрам
            match = True
            for key, value in filters.items():
                if key in item and item[key] != value:
                    match = False
                    break

            if match:
                try:
                    aeroplane = Aeroplane(
                        callsign=item.get('callsign', ''),
                        origin_country=item.get('origin_country', 'Неизвестно'),
                        velocity=item.get('velocity'),
                        altitude=item.get('altitude'),
                        icao24=item.get('icao24', ''),
                        longitude=item.get('longitude', 0.0),
                        latitude=item.get('latitude', 0.0),
                        on_ground=item.get('on_ground', False)
                    )
                    aeroplanes.append(aeroplane)
                except (ValueError, TypeError):
                    continue

        return aeroplanes

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """
        Удаление информации о самолете
        """
        data = self._read_file()
        data = [item for item in data if item.get('callsign') != aeroplane.callsign]
        self._write_file(data)

    def get_all_aeroplanes(self) -> List[Aeroplane]:
        """
        Получение всех самолетов из файла
        """
        return self.get_aeroplanes()

    def clear(self) -> None:
        """Очистка файла"""
        self._write_file([])
