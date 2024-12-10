import unittest
from unittest.mock import patch
from io import StringIO
import json
import app
from datetime import datetime


class TestApp(unittest.TestCase):

    def test_collect_output_keys(self):
        data_model = {
            "temperature": "${temperature}",
            "humidity": "${humidity} ${unit}",
            "nested": {
                "pressure": "${pressure} ${altitude}",
                "info": "static_value"
            },
            "array": ["${wind_speed}", "constant"]
        }
        expected_keys = ["temperature", "humidity", "unit", "pressure", "altitude", "wind_speed"]
        result = app.collect_output_keys(data_model)
        self.assertCountEqual(result, expected_keys)

    def test_get_variable_value_local_scope(self):
        local_scope = {"temperature": 25, "humidity": 70}
        result = app.get_variable_value("temperature", local_scope)
        self.assertEqual(result, 25)

    # def test_get_variable_value_global_scope(self):
    #     with patch.dict("app.globals", {"pressure": 1013}):
    #         result = app.get_variable_value("pressure")
    #         self.assertEqual(result, 1013)

    def test_get_variable_value_not_found(self):
        result = app.get_variable_value("nonexistent")
        self.assertIsNone(result)

    def test_replace_placeholder_dict(self):
        data = {
            "temperature": "${temperature}",
            "humidity": "${humidity}"
        }
        result = app.replace_placeholder(data, "${temperature}", 25)
        expected = {
            "temperature": 25,
            "humidity": "${humidity}"
        }
        self.assertEqual(result, expected)

    def test_replace_placeholder_nested(self):
        data = {
            "nested": {
                "temperature": "${temperature}",
                "info": "constant"
            }
        }
        result = app.replace_placeholder(data, "${temperature}", 30)
        data["nested"]["temperature"] = 30
        expected = {
            "nested": {
                "temperature": 30,
                "info": "constant"
            }
        }
        self.assertEqual(result, expected)

    def test_run_function(self):
        config = {
            "params": {
                "TZ": "UTC",
                "T": 1,
                "MIN": -10,
                "MAX": 10
            },
            "data_model": {
                "ref": "${id}",
                "tz": "${current_time}",
                "temperature": "${temperature}"
            }
        }
        id = "jzp://edv.0001"
        with patch("time.sleep", return_value=None), patch("builtins.print") as mock_print:
            with patch("app.datetime") as mock_datetime:
                mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
                mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
                app.run(id, config)
                mock_print.assert_called()  # Ensure print was called

    def test_replace_placeholder_list(self):
        data = ["${temperature}", "constant"]
        result = app.replace_placeholder(data, "${temperature}", 25)
        expected = [25, "constant"]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
