from unittest.mock import Mock, patch

import pytest

from src.aeroplanes_api import AeroplanesAPI


class TestAeroplanesAPI:
    """Тесты для класса AeroplanesAPI"""

    @patch('src.aeroplanes_api.requests.Session.get')
    def test_get_country_coordinates_success(self, mock_get):
        """Тест успешного получения координат страны"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {'boundingbox': ['50.0', '60.0', '-10.0', '0.0']}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api = AeroplanesAPI()
        coords = api.get_country_coordinates('Spain')

        assert coords['min_lat'] == 50.0
        assert coords['max_lat'] == 60.0
        assert coords['min_lon'] == -10.0
        assert coords['max_lon'] == 0.0

    @patch('src.aeroplanes_api.requests.Session.get')
    def test_get_country_coordinates_not_found(self, mock_get):
        """Тест поиска несуществующей страны"""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api = AeroplanesAPI()

        with pytest.raises(ValueError, match="Страна 'UnknownCountry' не найдена"):
            api.get_country_coordinates('UnknownCountry')

    @patch('src.aeroplanes_api.AeroplanesAPI.get_country_coordinates')
    @patch('src.aeroplanes_api.requests.Session.get')
    def test_get_aeroplanes_success(self, mock_get, mock_coords):
        """Тест успешного получения данных о самолетах"""
        mock_coords.return_value = {
            'min_lat': 50.0, 'max_lat': 60.0,
            'min_lon': -10.0, 'max_lon': 0.0
        }

        mock_response = Mock()
        mock_response.json.return_value = {
            'states': [
                ['abc123', 'UAL1621', 'United States', 123, 456, 0.0, 0.0,
                 10203.18, False, 268.79, 0.0, 0.0, [], 10203.18, '1234', False, 0]
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        api = AeroplanesAPI()
        result = api.get_aeroplanes('Spain')

        assert len(result) == 1
        assert result[0]['callsign'] == 'UAL1621'
        assert result[0]['origin_country'] == 'United States'
