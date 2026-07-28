import os
import sys
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from src.user_interface import user_main

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestUserInterface(unittest.TestCase):

    @patch("src.aircraft.Aircraft.state_converting")
    @patch("src.aircraft_sourse.AircraftSourse")
    @patch("src.geocoder.Geocoder")
    @patch("builtins.input")
    def test_successful_execution(self, mock_input, mock_geocoder, mock_aircraft_source, mock_state_converting):
        mock_input.side_effect = ["Ireland", "нет", "5"]

        mock_geocoder_instance = MagicMock()
        mock_geocoder_instance.get_bounding_box.return_value = [1, 2, 3, 4]
        mock_geocoder_instance.name_country = "Ireland"
        mock_geocoder.return_value = mock_geocoder_instance

        mock_aircraft_instance = MagicMock()
        mock_aircraft_instance.get_aeroplanes.return_value = [["callsign1", 1, 2, 3, 4, 5, 6, 7, "Country1"]]
        mock_aircraft_source.return_value = mock_aircraft_instance

        mock_aircraft = MagicMock()
        mock_aircraft.callsign = "callsign1"
        mock_aircraft.country = "Country1"
        mock_aircraft.velocity = 5
        mock_aircraft.height = 6
        mock_state_converting.return_value = mock_aircraft

        user_main()

    @patch("src.aircraft.Aircraft.state_converting")
    @patch("src.aircraft_sourse.AircraftSourse")
    @patch("src.geocoder.Geocoder")
    @patch("builtins.input")
    def test_empty_country(self, mock_input, mock_geocoder, mock_aircraft_source, mock_state_converting):
        mock_input.side_effect = ["", "Ireland", "нет", "5"]

        mock_geocoder_instance = MagicMock()
        mock_geocoder_instance.get_bounding_box.return_value = [1, 2, 3, 4]
        mock_geocoder_instance.name_country = "Ireland"
        mock_geocoder.return_value = mock_geocoder_instance

        mock_aircraft_instance = MagicMock()
        mock_aircraft_instance.get_aeroplanes.return_value = [["callsign1", 1, 2, 3, 4, 5, 6, 7, "Country1"]]
        mock_aircraft_source.return_value = mock_aircraft_instance

        mock_aircraft = MagicMock()
        mock_aircraft.callsign = "callsign1"
        mock_aircraft.country = "Country1"
        mock_aircraft.velocity = 5
        mock_aircraft.height = 6
        mock_state_converting.return_value = mock_aircraft

        user_main()

    @patch("src.aircraft_sourse.AircraftSourse")
    @patch("src.geocoder.Geocoder")
    @patch("builtins.input")
    def test_no_bounding_box(self, mock_input, mock_geocoder, mock_aircraft_source):
        mock_input.side_effect = ["Ireland"]

        mock_geocoder_instance = MagicMock()
        mock_geocoder_instance.get_bounding_box.return_value = None
        mock_geocoder.return_value = mock_geocoder_instance

        user_main()

    @patch("src.aircraft_sourse.AircraftSourse")
    @patch("src.geocoder.Geocoder")
    @patch("builtins.input")
    def test_no_aircraft(self, mock_input, mock_geocoder, mock_aircraft_source):
        mock_input.side_effect = ["Ireland"]

        mock_geocoder_instance = MagicMock()
        mock_geocoder_instance.get_bounding_box.return_value = [1, 2, 3, 4]
        mock_geocoder_instance.name_country = "Ireland"
        mock_geocoder.return_value = mock_geocoder_instance

        mock_aircraft_instance = MagicMock()
        mock_aircraft_instance.get_aeroplanes.return_value = []
        mock_aircraft_source.return_value = mock_aircraft_instance

        user_main()

    @patch("src.aircraft_sourse.AircraftSourse")
    @patch("src.geocoder.Geocoder")
    @patch("builtins.input")
    def test_server_error(self, mock_input, mock_geocoder, mock_aircraft_source):
        mock_input.side_effect = ["Ireland"]

        mock_geocoder_instance = MagicMock()
        mock_geocoder_instance.get_bounding_box.return_value = [1, 2, 3, 4]
        mock_geocoder.return_value = mock_geocoder_instance

        mock_aircraft_instance = MagicMock()
        mock_aircraft_instance.get_aeroplanes.return_value = None
        mock_aircraft_source.return_value = mock_aircraft_instance

        user_main()

    @patch("builtins.input")
    def test_keyboard_interrupt(self, mock_input):
        mock_input.side_effect = KeyboardInterrupt()
        user_main()

    @patch("src.aircraft.Aircraft.get_sort")
    @patch("src.aircraft.Aircraft.state_converting")
    @patch("src.aircraft_sourse.AircraftSourse")
    @patch("src.geocoder.Geocoder")
    @patch("builtins.input")
    def test_top_aircraft(self, mock_input, mock_geocoder, mock_aircraft_source, mock_state_converting, mock_get_sort):
        mock_input.side_effect = ["Ireland", "нет", "1", "2", "5"]

        mock_geocoder_instance = MagicMock()
        mock_geocoder_instance.get_bounding_box.return_value = [1, 2, 3, 4]
        mock_geocoder_instance.name_country = "Ireland"
        mock_geocoder.return_value = mock_geocoder_instance

        mock_aircraft_instance = MagicMock()
        mock_aircraft_instance.get_aeroplanes.return_value = [
            ["callsign1", 1, 2, 3, 4, 5, 1000, 7, "Country1"],
            ["callsign2", 1, 2, 3, 4, 6, 2000, 7, "Country2"],
        ]
        mock_aircraft_source.return_value = mock_aircraft_instance

        mock_aircraft1 = MagicMock()
        mock_aircraft1.callsign = "callsign1"
        mock_aircraft1.country = "Country1"
        mock_aircraft1.velocity = 5
        mock_aircraft1.height = 1000

        mock_aircraft2 = MagicMock()
        mock_aircraft2.callsign = "callsign2"
        mock_aircraft2.country = "Country2"
        mock_aircraft2.velocity = 6
        mock_aircraft2.height = 2000

        mock_state_converting.side_effect = [mock_aircraft1, mock_aircraft2]
        mock_get_sort.return_value = [mock_aircraft1, mock_aircraft2]

        user_main()

    @patch("src.aircraft.Aircraft.state_converting")
    @patch("src.aircraft_sourse.AircraftSourse")
    @patch("src.geocoder.Geocoder")
    @patch("builtins.input")
    def test_top_aircraft_invalid_n(self, mock_input, mock_geocoder, mock_aircraft_source, mock_state_converting):
        mock_input.side_effect = ["Ireland", "нет", "1", "invalid", "5", "5"]

        mock_geocoder_instance = MagicMock()
        mock_geocoder_instance.get_bounding_box.return_value = [1, 2, 3, 4]
        mock_geocoder_instance.name_country = "Ireland"
        mock_geocoder.return_value = mock_geocoder_instance

        mock_aircraft_instance = MagicMock()
        mock_aircraft_instance.get_aeroplanes.return_value = [["callsign1", 1, 2, 3, 4, 5, 1000, 7, "Country1"]]
        mock_aircraft_source.return_value = mock_aircraft_instance

        mock_aircraft = MagicMock()
        mock_aircraft.callsign = "callsign1"
        mock_aircraft.country = "Country1"
        mock_aircraft.velocity = 5
        mock_aircraft.height = 1000
        mock_state_converting.return_value = mock_aircraft

        user_main()

    @patch("src.aircraft.Aircraft.state_converting")
    @patch("src.aircraft_sourse.AircraftSourse")
    @patch("src.geocoder.Geocoder")
    @patch("builtins.input")
    def test_filter_by_country(self, mock_input, mock_geocoder, mock_aircraft_source, mock_state_converting):
        mock_input.side_effect = ["Ireland", "нет", "2", "Country1", "5"]

        mock_geocoder_instance = MagicMock()
        mock_geocoder_instance.get_bounding_box.return_value = [1, 2, 3, 4]
        mock_geocoder_instance.name_country = "Ireland"
        mock_geocoder.return_value = mock_geocoder_instance

        mock_aircraft_instance = MagicMock()
        mock_aircraft_instance.get_aeroplanes.return_value = [
            ["callsign1", 1, 2, 3, 4, 5, 1000, 7, "Country1"],
            ["callsign2", 1, 2, 3, 4, 6, 2000, 7, "Country2"],
        ]
        mock_aircraft_source.return_value = mock_aircraft_instance

        mock_aircraft1 = MagicMock()
        mock_aircraft1.callsign = "callsign1"
        mock_aircraft1.country = "Country1"
        mock_aircraft1.velocity = 5
        mock_aircraft1.height = 1000

        mock_aircraft2 = MagicMock()
        mock_aircraft2.callsign = "callsign2"
        mock_aircraft2.country = "Country2"
        mock_aircraft2.velocity = 6
        mock_aircraft2.height = 2000

        mock_state_converting.side_effect = [mock_aircraft1, mock_aircraft2]

        user_main()

    @patch("src.aircraft.Aircraft.state_converting")
    @patch("src.aircraft_sourse.AircraftSourse")
    @patch("src.geocoder.Geocoder")
    @patch("builtins.input")
    def test_filter_by_country_empty(self, mock_input, mock_geocoder, mock_aircraft_source, mock_state_converting):
        mock_input.side_effect = ["Ireland", "нет", "2", "", "Country1", "5"]

        mock_geocoder_instance = MagicMock()
        mock_geocoder_instance.get_bounding_box.return_value = [1, 2, 3, 4]
        mock_geocoder_instance.name_country = "Ireland"
        mock_geocoder.return_value = mock_geocoder_instance

        mock_aircraft_instance = MagicMock()
        mock_aircraft_instance.get_aeroplanes.return_value = [["callsign1", 1, 2, 3, 4, 5, 1000, 7, "Country1"]]
        mock_aircraft_source.return_value = mock_aircraft_instance

        mock_aircraft = MagicMock()
        mock_aircraft.callsign = "callsign1"
        mock_aircraft.country = "Country1"
        mock_aircraft.velocity = 5
        mock_aircraft.height = 1000
        mock_state_converting.return_value = mock_aircraft

        user_main()

    @patch("src.aircraft.Aircraft.state_converting")
    @patch("src.aircraft_sourse.AircraftSourse")
    @patch("src.geocoder.Geocoder")
    @patch("builtins.input")
    def test_statistics(self, mock_input, mock_geocoder, mock_aircraft_source, mock_state_converting):
        mock_input.side_effect = ["Ireland", "нет", "3", "5"]

        mock_geocoder_instance = MagicMock()
        mock_geocoder_instance.get_bounding_box.return_value = [1, 2, 3, 4]
        mock_geocoder_instance.name_country = "Ireland"
        mock_geocoder.return_value = mock_geocoder_instance

        mock_aircraft_instance = MagicMock()
        mock_aircraft_instance.get_aeroplanes.return_value = [
            ["callsign1", 1, 2, 3, 4, 5, 1000, 7, "Country1"],
            ["callsign2", 1, 2, 3, 4, 6, 2000, 7, "Country2"],
        ]
        mock_aircraft_source.return_value = mock_aircraft_instance

        mock_aircraft1 = MagicMock()
        mock_aircraft1.callsign = "callsign1"
        mock_aircraft1.country = "Country1"
        mock_aircraft1.velocity = 5
        mock_aircraft1.height = 1000

        mock_aircraft2 = MagicMock()
        mock_aircraft2.callsign = "callsign2"
        mock_aircraft2.country = "Country2"
        mock_aircraft2.velocity = 6
        mock_aircraft2.height = 2000

        mock_state_converting.side_effect = [mock_aircraft1, mock_aircraft2]

        user_main()

    @patch("src.aircraft.Aircraft.state_converting")
    @patch("src.aircraft_storage.AircraftStorageJSON")
    @patch("src.aircraft_sourse.AircraftSourse")
    @patch("src.geocoder.Geocoder")
    @patch("builtins.input")
    def test_show_saved_file(
        self, mock_input, mock_geocoder, mock_aircraft_source, mock_storage, mock_state_converting
    ):
        mock_input.side_effect = ["Ireland", "нет", "4", "5"]

        mock_geocoder_instance = MagicMock()
        mock_geocoder_instance.get_bounding_box.return_value = [1, 2, 3, 4]
        mock_geocoder_instance.name_country = "Ireland"
        mock_geocoder.return_value = mock_geocoder_instance

        mock_aircraft_instance = MagicMock()
        mock_aircraft_instance.get_aeroplanes.return_value = [["callsign1", 1, 2, 3, 4, 5, 1000, 7, "Country1"]]
        mock_aircraft_source.return_value = mock_aircraft_instance

        mock_aircraft = MagicMock()
        mock_aircraft.callsign = "callsign1"
        mock_aircraft.country = "Country1"
        mock_aircraft.velocity = 5
        mock_aircraft.height = 1000
        mock_state_converting.return_value = mock_aircraft

        mock_storage_instance = MagicMock()
        mock_storage_instance.data = [{"callsign": "test"}]
        mock_storage.return_value = mock_storage_instance

        user_main()

    @patch("src.aircraft.Aircraft.state_converting")
    @patch("src.aircraft_sourse.AircraftSourse")
    @patch("src.geocoder.Geocoder")
    @patch("builtins.input")
    def test_invalid_menu_choice(self, mock_input, mock_geocoder, mock_aircraft_source, mock_state_converting):
        mock_input.side_effect = ["Ireland", "нет", "99", "5"]

        mock_geocoder_instance = MagicMock()
        mock_geocoder_instance.get_bounding_box.return_value = [1, 2, 3, 4]
        mock_geocoder_instance.name_country = "Ireland"
        mock_geocoder.return_value = mock_geocoder_instance

        mock_aircraft_instance = MagicMock()
        mock_aircraft_instance.get_aeroplanes.return_value = [["callsign1", 1, 2, 3, 4, 5, 1000, 7, "Country1"]]
        mock_aircraft_source.return_value = mock_aircraft_instance

        mock_aircraft = MagicMock()
        mock_aircraft.callsign = "callsign1"
        mock_aircraft.country = "Country1"
        mock_aircraft.velocity = 5
        mock_aircraft.height = 1000
        mock_state_converting.return_value = mock_aircraft

        user_main()

    @patch("src.aircraft_sourse.AircraftSourse")
    @patch("src.geocoder.Geocoder")
    @patch("builtins.input")
    def test_exception_handling(self, mock_input, mock_geocoder, mock_aircraft_source):
        mock_input.side_effect = ["Ireland"]

        mock_geocoder_instance = MagicMock()
        mock_geocoder_instance.get_bounding_box.side_effect = Exception("Test error")
        mock_geocoder.return_value = mock_geocoder_instance
