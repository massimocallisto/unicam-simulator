import unittest
from unittest.mock import patch, MagicMock
import time
import json
from app import App
from functions import collect_output_keys, get_variable_value, replace_placeholder


class TestFunctions(unittest.TestCase):
    def test_collect_output_keys(self):
        data_model = {
            "simple_message": "${random_text}",
            "nested": {
                "iteration": "${iteration}",
                "info": "constant_value"
            },
            "array": ["${id}", "${another_key}"]
        }
        expected_keys = ["random_text", "iteration", "id", "another_key"]
        self.assertCountEqual(collect_output_keys(data_model), expected_keys)

    def test_get_variable_value_local_scope(self):
        local_scope = {"temperature": 25, "humidity": 70}
        self.assertEqual(get_variable_value("temperature", local_scope), 25)
        self.assertEqual(get_variable_value("humidity", local_scope), 70)

    def test_get_variable_value_additional_map(self):
        additional_map = {"iteration": 5, "id": "test-id"}
        self.assertEqual(get_variable_value("iteration", None, additional_map), 5)
        self.assertEqual(get_variable_value("id", None, additional_map), "test-id")

    def test_get_variable_value_not_found(self):
        self.assertIsNone(get_variable_value("nonexistent"))

    def test_replace_placeholder(self):
        data = {
            "simple_message": "${random_text}",
            "nested": {"iteration": "${iteration}"}
        }
        replaced_data = replace_placeholder(data, "${random_text}", "HelloWorld")
        expected = {
            "simple_message": "HelloWorld",
            "nested": {"iteration": "${iteration}"}
        }
        self.assertEqual(replaced_data, expected)


class TestApp(unittest.TestCase):
    def setUp(self):
        self.config = {
            "id": "test-id",
            "params": {
                "T": 1,
                "max_iterations": 2
            },
            "data_model": {
                "simple_message": "${random_text}",
                "iteration": "${iteration}",
                "ref": "${id}"
            }
        }
        self.app = App(self.config)

    def test_configure(self):
        self.app.configure()
        self.assertEqual(self.app.params["T"], 1)
        self.assertEqual(self.app.params["max_iterations"], 2)
        self.assertEqual(self.app.id, "test-id")
        alist = ["random_text", "iteration", "id"]
        alist.sort()
        self.assertListEqual(self.app.output_keys, alist)

    @patch("time.sleep", return_value=None)
    @patch("builtins.print")
    def test_execute(self, mock_print, _):
        self.app.configure()
        self.app.execute()
        self.assertEqual(mock_print.call_count, 2)  # max_iterations = 2

    def test_run(self):
        self.app.configure()
        with patch("builtins.print") as mock_print:
            self.app.run()
            output = json.loads(mock_print.call_args[0][0])  # Parse the printed JSON
            self.assertIn("simple_message", output)
            self.assertIn("iteration", output)
            self.assertIn("ref", output)

    def test_set_output(self):
        self.app.configure()
        local_vars = {"random_text": "abc123", "iteration": 1}
        output = self.app.set_output(local_vars)
        self.assertEqual(output["simple_message"], "abc123")
        self.assertEqual(output["iteration"], 1)
        self.assertEqual(output["ref"], "test-id")

    def test_get_param(self):
        self.assertEqual(self.app.get_param("T"), 1)
        self.assertEqual(self.app.get_param("max_iterations"), 2)

    def test_get_config(self):
        self.assertEqual(self.app.get_config("id"), "test-id")
        self.assertIsNone(self.app.get_config("nonexistent_param"))


if __name__ == "__main__":
    unittest.main()
