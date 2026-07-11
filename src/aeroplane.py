from typing import Any, Dict, List, Optional


class Aeroplane:
    """Класс для представления самолета"""

    def __init__(self, callsign: str, origin_country: str,
                 velocity: Optional[float], altitude: Optional[float],
                 icao24: str = "", longitude: float = 0.0,
                 latitude: float = 0.0, on_ground: bool = False):
        """
        Инициализация самолета

        Args:
            callsign: Позывной самолета
            origin_country: Страна регистрации
            velocity: Скорость (м/с)
            altitude: Высота (м)
            icao24: ICAO код
            longitude: Долгота
            latitude: Широта
            on_ground: На земле или в воздухе
        """
        self.callsign = callsign
        self.origin_country = origin_country
        self.icao24 = icao24
        self.longitude = longitude
        self.latitude = latitude
        self._velocity = velocity
        self._altitude = altitude
        self.on_ground = on_ground

    @property
    def velocity(self) -> Optional[float]:
        """Геттер для скорости"""
        return self._velocity

    @velocity.setter
    def velocity(self, value: Optional[float]) -> None:
        """Сеттер для скорости с валидацией"""
        if value is not None and value < 0:
            raise ValueError("Скорость не может быть отрицательной")
        self._velocity = value

    @property
    def altitude(self) -> Optional[float]:
        """Геттер для высоты"""
        return self._altitude

    @altitude.setter
    def altitude(self, value: Optional[float]) -> None:
        """Сеттер для высоты с валидацией"""
        if value is not None and value < 0:
            raise ValueError("Высота не может быть отрицательной")
        self._altitude = value

    def __str__(self) -> str:
        """Строковое представление самолета"""
        status = "на земле" if self.on_ground else "в воздухе"
        return (f"{self.callsign} ({self.origin_country}) - {status}, "
                f"скорость: {self.velocity if self.velocity is not None else 'Н/Д'} м/с, "
                f"высота: {self.altitude if self.altitude is not None else 'Н/Д'} м")

    def __repr__(self) -> str:
        return (f"Aeroplane('{self.callsign}', '{self.origin_country}', "
                f"{self.velocity}, {self.altitude})")

    def __lt__(self, other: 'Aeroplane') -> bool:
        """Сравнение по высоте (для сортировки)"""
        if not isinstance(other, Aeroplane):
            return NotImplemented

        # Сначала сравниваем по высоте
        if self.altitude is not None and other.altitude is not None:
            return self.altitude < other.altitude
        # Если высота отсутствует, сравниваем по скорости
        elif self.velocity is not None and other.velocity is not None:
            return self.velocity < other.velocity
        else:
            return False

    def __gt__(self, other: 'Aeroplane') -> bool:
        """Сравнение по высоте"""
        if not isinstance(other, Aeroplane):
            return NotImplemented

        if self.altitude is not None and other.altitude is not None:
            return self.altitude > other.altitude
        elif self.velocity is not None and other.velocity is not None:
            return self.velocity > other.velocity
        else:
            return False

    def __eq__(self, other: 'Aeroplane') -> bool:
        """Сравнение на равенство"""
        if not isinstance(other, Aeroplane):
            return NotImplemented

        return (self.callsign == other.callsign and
                self.origin_country == other.origin_country)

    @classmethod
    def cast_to_object_list(cls, data_list: List[Dict[str, Any]]) -> List['Aeroplane']:
        """
        Преобразование списка словарей в список объектов Aeroplane

        Args:
            data_list: Список словарей с данными о самолетах

        Returns:
            Список объектов Aeroplane
        """
        aeroplanes = []
        for data in data_list:
            try:
                # Проверяем наличие обязательных полей
                callsign = data.get('callsign', '')
                origin_country = data.get('origin_country', 'Неизвестно')

                # Пропускаем записи без позывного и без страны
                if not callsign and origin_country == 'Неизвестно':
                    continue

                # Если нет callsign, но есть origin_country - используем origin_country как callsign
                if not callsign:
                    callsign = origin_country[:5].upper() if origin_country else 'UNKNOWN'

                # Получаем высоту (приоритет: geo_altitude > baro_altitude > altitude)
                altitude = data.get('geo_altitude') or data.get('baro_altitude') or data.get('altitude')

                # Получаем скорость
                velocity = data.get('velocity')

                # Пропускаем записи без скорости и высоты (неинформативные)
                if velocity is None and altitude is None:
                    continue

                aeroplane = cls(
                    callsign=callsign,
                    origin_country=origin_country,
                    velocity=velocity,
                    altitude=altitude,
                    icao24=data.get('icao24', ''),
                    longitude=data.get('longitude', 0.0),
                    latitude=data.get('latitude', 0.0),
                    on_ground=data.get('on_ground', False)
                )
                aeroplanes.append(aeroplane)
            except (ValueError, TypeError, AttributeError):
                # Пропускаем некорректные записи
                continue
        return aeroplanes
