from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def get_country_coordinates(self, country_name: str) -> Dict[str, Any]:
        """
        Получение географических координат страны

        Args:
            country_name: Название страны

        Returns:
            Словарь с координатами (boundingbox)
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, country_name: str) -> List[Dict[str, Any]]:
        """
        Получение информации о самолетах в воздушном пространстве страны

        Args:
            country_name: Название страны

        Returns:
            Список словарей с данными о самолетах
        """
        pass
