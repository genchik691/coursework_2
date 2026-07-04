from abc import ABC, abstractmethod
from typing import List

from src.aeroplane import Aeroplane


class AbstractStorage(ABC):
    """Абстрактный класс для работы с хранилищем"""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """
        Добавление информации о самолете в хранилище

        Args:
            aeroplane: Объект самолета
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, **filters) -> List[Aeroplane]:
        """
        Получение информации о самолетах по критериям

        Args:
            **filters: Критерии фильтрации

        Returns:
            Список объектов самолетов
        """
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        """
        Удаление информации о самолете

        Args:
            aeroplane: Объект самолета для удаления
        """
        pass

    @abstractmethod
    def get_all_aeroplanes(self) -> List[Aeroplane]:
        """
        Получение всех самолетов из хранилища

        Returns:
            Список всех объектов самолетов
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Очистка хранилища"""
        pass
