import time
from typing import Any, Dict, List, Optional

import requests

from src.abstract_api import AbstractAPI


class AeroplanesAPI(AbstractAPI):
    """Класс для работы с API самолетов"""

    # Константы с URL API
    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_URL = "https://opensky-network.org/api/states/all"

    def __init__(self, user_agent: Optional[str] = None):
        """
        Инициализация API

        Args:
            user_agent: User-Agent для запросов (рекомендуется указывать email)
        """
        self.session = requests.Session()

        # Устанавливаем User-Agent (обязательно для Nominatim)
        if user_agent is None:
            user_agent = "AircraftMonitoringSystem/1.0 (genchik691@gmail.com)"

        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'application/json'
        })

    def get_country_coordinates(self, country_name: str) -> Dict[str, float]:
        """
        Получение географических координат страны через Nominatim API

        Args:
            country_name: Название страны

        Returns:
            Словарь с координатами

        Raises:
            ValueError: Если страна не найдена
            requests.RequestException: При ошибке запроса
        """
        try:
            # Параметры запроса к Nominatim
            params = {
                'q': country_name,
                'format': 'json',
                'limit': 1
            }

            # Добавляем задержку для соблюдения политики использования
            time.sleep(1)

            # Отправляем GET-запрос
            response = self.session.get(self.NOMINATIM_URL, params=params)
            response.raise_for_status()

            data = response.json()

            if not data:
                raise ValueError(f"Страна '{country_name}' не найдена")

            # Получаем boundingbox из ответа
            boundingbox = data[0].get('boundingbox', [])

            if len(boundingbox) < 4:
                raise ValueError(f"Не удалось получить координаты для страны '{country_name}'")

            return {
                'min_lat': float(boundingbox[0]),
                'max_lat': float(boundingbox[1]),
                'min_lon': float(boundingbox[2]),
                'max_lon': float(boundingbox[3])
            }

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                raise ValueError(
                    "Ошибка доступа к Nominatim API. Убедитесь, что указан корректный User-Agent.\n"
                    "Попробуйте: установить переменную окружения или использовать другой email."
                )
            raise requests.RequestException(f"Ошибка при запросе к Nominatim API: {e}")
        except requests.RequestException as e:
            raise requests.RequestException(f"Ошибка при запросе к Nominatim API: {e}")
        except (ValueError, IndexError, KeyError) as e:
            raise ValueError(f"Ошибка при обработке данных: {e}")

    def get_aeroplanes_by_bounding_box(self, min_lat: float, max_lat: float,
                                       min_lon: float, max_lon: float) -> List[Dict[str, Any]]:
        """
        Получение информации о самолетах по географической области через OpenSky API
        """
        try:
            # Параметры запроса к OpenSky API
            params = {
                'lamin': min_lat,
                'lamax': max_lat,
                'lomin': min_lon,
                'lomax': max_lon
            }

            # Добавляем задержку
            time.sleep(0.5)

            # Отправляем GET-запрос
            response = self.session.get(self.OPENSKY_URL, params=params)
            response.raise_for_status()

            data = response.json()
            states = data.get('states', [])

            # Преобразуем данные в список словарей
            aeroplanes = []
            for state in states:
                if state and len(state) >= 17:
                    aeroplane_data = {
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
                    # Добавляем только если есть данные
                    if aeroplane_data['callsign'] or aeroplane_data['origin_country'] != 'Неизвестно':
                        aeroplanes.append(aeroplane_data)

            return aeroplanes

        except requests.RequestException as e:
            raise requests.RequestException(f"Ошибка при запросе к OpenSky API: {e}")
        except (ValueError, IndexError, KeyError) as e:
            raise ValueError(f"Ошибка при обработке данных: {e}")

    def get_aeroplanes(self, country_name: str) -> List[Dict[str, Any]]:
        """
        Получение информации о самолетах в воздушном пространстве страны
        """
        try:
            # Получаем координаты страны
            coords = self.get_country_coordinates(country_name)

            # Получаем самолеты по координатам
            return self.get_aeroplanes_by_bounding_box(
                coords['min_lat'],
                coords['max_lat'],
                coords['min_lon'],
                coords['max_lon']
            )

        except (ValueError, requests.RequestException) as e:
            raise ValueError(f"Ошибка при получении данных о самолетах: {e}")
