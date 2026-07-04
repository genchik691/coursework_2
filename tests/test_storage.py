import os
import tempfile


from src.aeroplane import Aeroplane
from src.json_storage import JSONStorage


class TestJSONStorage:
    """Тесты для JSONStorage"""

    def test_add_aeroplane(self):
        """Тест добавления самолета"""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            storage = JSONStorage(temp_file)
            aeroplane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)

            storage.add_aeroplane(aeroplane)

            # Проверяем, что самолет добавлен
            result = storage.get_all_aeroplanes()
            assert len(result) == 1
            assert result[0].callsign == "UAL1621"

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_add_duplicate_aeroplane(self):
        """Тест добавления дубликата самолета"""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            storage = JSONStorage(temp_file)
            aeroplane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)

            storage.add_aeroplane(aeroplane)
            storage.add_aeroplane(aeroplane)  # Дубликат

            result = storage.get_all_aeroplanes()
            assert len(result) == 1  # Дубликат не должен добавиться

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_get_aeroplanes_with_filters(self):
        """Тест получения самолетов с фильтрацией"""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            storage = JSONStorage(temp_file)

            a1 = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
            a2 = Aeroplane("BAW123", "United Kingdom", 250.00, 9000.00)
            a3 = Aeroplane("AFR456", "France", 270.00, 11000.00)

            storage.add_aeroplane(a1)
            storage.add_aeroplane(a2)
            storage.add_aeroplane(a3)

            # Фильтрация по стране
            result = storage.get_aeroplanes(origin_country="United States")
            assert len(result) == 1
            assert result[0].callsign == "UAL1621"

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_delete_aeroplane(self):
        """Тест удаления самолета"""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            storage = JSONStorage(temp_file)
            aeroplane = Aeroplane("UAL1621", "United States", 268.79, 10203.18)

            storage.add_aeroplane(aeroplane)
            result = storage.get_all_aeroplanes()
            assert len(result) == 1

            storage.delete_aeroplane(aeroplane)
            result = storage.get_all_aeroplanes()
            assert len(result) == 0

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_clear(self):
        """Тест очистки хранилища"""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            storage = JSONStorage(temp_file)

            a1 = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
            a2 = Aeroplane("BAW123", "United Kingdom", 250.00, 9000.00)

            storage.add_aeroplane(a1)
            storage.add_aeroplane(a2)

            result = storage.get_all_aeroplanes()
            assert len(result) == 2

            storage.clear()
            result = storage.get_all_aeroplanes()
            assert len(result) == 0

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
