import pytest

from src.aeroplane import Aeroplane


class TestAeroplane:
    """Тесты для класса Aeroplane"""

    def test_aeroplane_creation(self):
        """Тест создания самолета"""
        aeroplane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
        assert aeroplane.callsign == "UAL1621"
        assert aeroplane.origin_country == "United States"
        assert aeroplane.velocity == 268.79
        assert aeroplane.altitude == 10203.18

    def test_aeroplane_with_optional_fields(self):
        """Тест создания с опциональными полями"""
        aeroplane = Aeroplane("UAL1621", "United States", 268.79, 10203.18,
                              "abc123", 37.6173, 55.7558, False)
        assert aeroplane.icao24 == "abc123"
        assert aeroplane.longitude == 37.6173
        assert aeroplane.latitude == 55.7558
        assert aeroplane.on_ground is False

    def test_aeroplane_velocity_validation(self):
        """Тест валидации скорости"""
        aeroplane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)

        with pytest.raises(ValueError, match="Скорость не может быть отрицательной"):
            aeroplane.velocity = -100

    def test_aeroplane_altitude_validation(self):
        """Тест валидации высоты"""
        aeroplane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)

        with pytest.raises(ValueError, match="Высота не может быть отрицательной"):
            aeroplane.altitude = -500

    def test_aeroplane_comparison_by_velocity(self):
        """Тест сравнения самолетов по скорости"""
        a1 = Aeroplane("A1", "US", 100.0, 1000)
        a2 = Aeroplane("A2", "UK", 200.0, 2000)

        assert a1 < a2
        assert a2 > a1
        assert not a1 > a2

    def test_aeroplane_comparison_by_altitude(self):
        """Тест сравнения самолетов по высоте"""
        a1 = Aeroplane("A1", "US", 100.0, 1000)
        a2 = Aeroplane("A2", "UK", 100.0, 2000)

        assert a1 < a2  # 1000 < 2000
        assert a2 > a1  # 2000 > 1000
        assert not a1 > a2

    def test_aeroplane_comparison_mixed(self):
        """Тест сравнения когда у одного нет высоты"""
        a1 = Aeroplane("A1", "US", 100.0, None)  # Нет высоты
        a2 = Aeroplane("A2", "UK", 200.0, 2000)

        # Сравниваем по скорости, т.к. у a1 нет высоты
        assert a1 < a2  # 100 < 200

        a3 = Aeroplane("A3", "FR", 300.0, None)
        assert a2 < a3  # 200 < 300

    def test_aeroplane_comparison_both_no_altitude(self):
        """Тест сравнения когда у обоих нет высоты"""
        a1 = Aeroplane("A1", "US", 100.0, None)
        a2 = Aeroplane("A2", "UK", 100.0, None)

        # Оба без высоты и с одинаковой скоростью
        assert not a1 < a2
        assert not a1 > a2

    def test_aeroplane_equality(self):
        """Тест равенства самолетов"""
        a1 = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
        a2 = Aeroplane("UAL1621", "United States", 300.0, 11000.0)
        a3 = Aeroplane("BAW123", "UK", 300.0, 11000.0)

        assert a1 == a2
        assert a1 != a3

    def test_cast_to_object_list(self):
        """Тест преобразования списка словарей в объекты"""
        data = [
            {'callsign': 'A1', 'origin_country': 'US', 'velocity': 100.0, 'altitude': 1000},
            {'callsign': 'A2', 'origin_country': 'UK', 'velocity': 200.0, 'altitude': 2000}
        ]

        aeroplanes = Aeroplane.cast_to_object_list(data)
        assert len(aeroplanes) == 2
        assert isinstance(aeroplanes[0], Aeroplane)
        assert aeroplanes[0].callsign == 'A1'

    def test_cast_to_object_list_with_invalid_data(self):
        """Тест преобразования с некорректными данными"""
        data = [
            {'callsign': 'A1', 'origin_country': 'US', 'velocity': 100.0, 'altitude': 1000},
            {'invalid': 'data'},  # Некорректные данные - должен быть пропущен
            {'callsign': 'A2', 'origin_country': 'UK', 'velocity': 200.0, 'altitude': 2000}
        ]

        aeroplanes = Aeroplane.cast_to_object_list(data)
        # Должны быть только корректные записи (A1 и A2)
        assert len(aeroplanes) == 2
        assert aeroplanes[0].callsign == 'A1'
        assert aeroplanes[1].callsign == 'A2'

    def test_cast_to_object_list_with_missing_fields(self):
        """Тест преобразования с отсутствующими полями"""
        data = [
            {'callsign': 'A1', 'origin_country': 'US', 'velocity': 100.0},  # Нет altitude
            {'callsign': 'A2', 'origin_country': 'UK', 'altitude': 2000},  # Нет velocity
            {'callsign': 'A3', 'origin_country': 'FR'},  # Нет velocity и altitude
            {'origin_country': 'DE'}  # Нет callsign
        ]

        aeroplanes = Aeroplane.cast_to_object_list(data)
        # Должны быть только A1 и A2 (у них есть хотя бы один параметр)
        assert len(aeroplanes) == 2
        assert aeroplanes[0].callsign == 'A1'
        assert aeroplanes[1].callsign == 'A2'

    def test_cast_to_object_list_empty(self):
        """Тест преобразования пустого списка"""
        aeroplanes = Aeroplane.cast_to_object_list([])
        assert aeroplanes == []

    def test_aeroplane_string_representation(self):
        """Тест строкового представления"""
        aeroplane = Aeroplane("UAL1621", "United States", 268.79, 10203.18, on_ground=False)
        str_repr = str(aeroplane)
        assert "UAL1621" in str_repr
        assert "United States" in str_repr
        assert "268.79" in str_repr
        assert "10203.18" in str_repr
        assert "в воздухе" in str_repr

    def test_aeroplane_string_representation_on_ground(self):
        """Тест строкового представления для самолета на земле"""
        aeroplane = Aeroplane("UAL1621", "United States", 0.0, 0.0, on_ground=True)
        assert "на земле" in str(aeroplane)

    def test_aeroplane_repr(self):
        """Тест repr представления"""
        aeroplane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
        repr_str = repr(aeroplane)
        assert "Aeroplane" in repr_str
        assert "UAL1621" in repr_str
        assert "United States" in repr_str
