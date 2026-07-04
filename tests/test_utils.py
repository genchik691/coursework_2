from src.aeroplane import Aeroplane
from src.json_storage import JSONStorage
from src.utils import (filter_aeroplanes_by_country,
                       get_aeroplanes_by_altitude_range,
                       get_aeroplanes_by_country_from_storage,
                       get_top_aeroplanes, print_aeroplanes,
                       sort_aeroplanes_by_altitude,
                       sort_aeroplanes_by_velocity)


class TestUtils:
    """Тесты для утилитных функций"""

    def test_filter_aeroplanes_by_country(self):
        """Тест фильтрации по стране"""
        a1 = Aeroplane("A1", "United States", 100.0, 1000)
        a2 = Aeroplane("A2", "United Kingdom", 200.0, 2000)
        a3 = Aeroplane("A3", "United States", 300.0, 3000)

        result = filter_aeroplanes_by_country([a1, a2, a3], "United States")
        assert len(result) == 2
        assert result[0].callsign == "A1"
        assert result[1].callsign == "A3"

    def test_filter_aeroplanes_by_country_empty(self):
        """Тест фильтрации с пустым списком"""
        result = filter_aeroplanes_by_country([], "United States")
        assert result == []

    def test_filter_aeroplanes_by_country_no_match(self):
        """Тест фильтрации без совпадений"""
        a1 = Aeroplane("A1", "United States", 100.0, 1000)
        result = filter_aeroplanes_by_country([a1], "Russia")
        assert result == []

    def test_sort_aeroplanes_by_altitude(self):
        """Тест сортировки по высоте"""
        a1 = Aeroplane("A1", "US", 100.0, 1000)
        a2 = Aeroplane("A2", "UK", 200.0, 2000)
        a3 = Aeroplane("A3", "FR", 300.0, 3000)

        result = sort_aeroplanes_by_altitude([a1, a2, a3], descending=True)
        assert result[0].altitude == 3000
        assert result[1].altitude == 2000
        assert result[2].altitude == 1000

    def test_sort_aeroplanes_by_altitude_ascending(self):
        """Тест сортировки по высоте по возрастанию"""
        a1 = Aeroplane("A1", "US", 100.0, 3000)
        a2 = Aeroplane("A2", "UK", 200.0, 1000)
        a3 = Aeroplane("A3", "FR", 300.0, 2000)

        result = sort_aeroplanes_by_altitude([a1, a2, a3], descending=False)
        assert result[0].altitude == 1000
        assert result[1].altitude == 2000
        assert result[2].altitude == 3000

    def test_sort_aeroplanes_by_altitude_with_none(self):
        """Тест сортировки с None значениями"""
        a1 = Aeroplane("A1", "US", 100.0, 1000)
        a2 = Aeroplane("A2", "UK", 200.0, None)
        a3 = Aeroplane("A3", "FR", 300.0, 2000)

        result = sort_aeroplanes_by_altitude([a1, a2, a3], descending=True)
        assert result[0].altitude == 2000
        assert result[1].altitude == 1000
        assert result[2].altitude is None

    def test_sort_aeroplanes_by_velocity(self):
        """Тест сортировки по скорости"""
        a1 = Aeroplane("A1", "US", 100.0, 1000)
        a2 = Aeroplane("A2", "UK", 300.0, 2000)
        a3 = Aeroplane("A3", "FR", 200.0, 3000)

        result = sort_aeroplanes_by_velocity([a1, a2, a3], descending=True)
        assert result[0].velocity == 300.0
        assert result[1].velocity == 200.0
        assert result[2].velocity == 100.0

    def test_sort_aeroplanes_by_velocity_ascending(self):
        """Тест сортировки по скорости по возрастанию"""
        a1 = Aeroplane("A1", "US", 100.0, 1000)
        a2 = Aeroplane("A2", "UK", 300.0, 2000)
        a3 = Aeroplane("A3", "FR", 200.0, 3000)

        result = sort_aeroplanes_by_velocity([a1, a2, a3], descending=False)
        assert result[0].velocity == 100.0
        assert result[1].velocity == 200.0
        assert result[2].velocity == 300.0

    def test_get_top_aeroplanes(self):
        """Тест получения топ N самолетов"""
        a1 = Aeroplane("A1", "US", 100.0, 1000)
        a2 = Aeroplane("A2", "UK", 200.0, 2000)
        a3 = Aeroplane("A3", "FR", 300.0, 3000)

        result = get_top_aeroplanes([a1, a2, a3], 2)
        assert len(result) == 2
        assert result[0].altitude == 3000
        assert result[1].altitude == 2000

    def test_get_top_aeroplanes_zero(self):
        """Тест получения 0 самолетов"""
        a1 = Aeroplane("A1", "US", 100.0, 1000)
        result = get_top_aeroplanes([a1], 0)
        assert result == []

    def test_get_top_aeroplanes_more_than_available(self):
        """Тест получения больше самолетов чем есть"""
        a1 = Aeroplane("A1", "US", 100.0, 1000)
        a2 = Aeroplane("A2", "UK", 200.0, 2000)

        result = get_top_aeroplanes([a1, a2], 5)
        assert len(result) == 2

    def test_get_aeroplanes_by_altitude_range(self):
        """Тест фильтрации по диапазону высот"""
        a1 = Aeroplane("A1", "US", 100.0, 1000)
        a2 = Aeroplane("A2", "UK", 200.0, 2000)
        a3 = Aeroplane("A3", "FR", 300.0, 3000)
        a4 = Aeroplane("A4", "DE", 400.0, None)

        result = get_aeroplanes_by_altitude_range([a1, a2, a3, a4], 1500, 2500)
        assert len(result) == 1
        assert result[0].altitude == 2000

    def test_get_aeroplanes_by_altitude_range_min_only(self):
        """Тест фильтрации только по минимальной высоте"""
        a1 = Aeroplane("A1", "US", 100.0, 1000)
        a2 = Aeroplane("A2", "UK", 200.0, 2000)
        a3 = Aeroplane("A3", "FR", 300.0, 3000)

        result = get_aeroplanes_by_altitude_range([a1, a2, a3], min_alt=2000)
        assert len(result) == 2
        assert all(a.altitude >= 2000 for a in result)

    def test_get_aeroplanes_by_altitude_range_max_only(self):
        """Тест фильтрации только по максимальной высоте"""
        a1 = Aeroplane("A1", "US", 100.0, 1000)
        a2 = Aeroplane("A2", "UK", 200.0, 2000)
        a3 = Aeroplane("A3", "FR", 300.0, 3000)

        result = get_aeroplanes_by_altitude_range([a1, a2, a3], max_alt=2000)
        assert len(result) == 2
        assert all(a.altitude <= 2000 for a in result)

    def test_print_aeroplanes(self, capsys):
        """Тест вывода самолетов"""
        a1 = Aeroplane("A1", "US", 100.0, 1000)
        a2 = Aeroplane("A2", "UK", 200.0, 2000)

        print_aeroplanes([a1, a2])
        captured = capsys.readouterr()
        assert "Найдено самолетов: 2" in captured.out
        assert "A1" in captured.out
        assert "A2" in captured.out

    def test_print_aeroplanes_empty(self, capsys):
        """Тест вывода пустого списка"""
        print_aeroplanes([])
        captured = capsys.readouterr()
        assert "Нет самолетов для отображения" in captured.out

    def test_get_aeroplanes_by_country_from_storage(self, tmp_path):
        """Тест получения самолетов из хранилища по стране"""
        storage = JSONStorage(str(tmp_path / "test.json"))

        a1 = Aeroplane("A1", "United States", 100.0, 1000)
        a2 = Aeroplane("A2", "United Kingdom", 200.0, 2000)
        a3 = Aeroplane("A3", "United States", 300.0, 3000)

        storage.add_aeroplane(a1)
        storage.add_aeroplane(a2)
        storage.add_aeroplane(a3)

        result = get_aeroplanes_by_country_from_storage(storage, "United States")
        assert len(result) == 2
        assert result[0].callsign == "A1"
        assert result[1].callsign == "A3"
