import unittest
from unittest import mock

import utils

class TestGetConfig(unittest.TestCase):

    @mock.patch("utils.open")
    def test_default_paths_called(self, mock_open):
        """
        Tests
        1. When both default paths are not found, utils.get_config will throw an IOError
        2. That both expected default paths are checked
        """
        mock_open.side_effect = FileNotFoundError
        self.assertRaises(IOError, utils.get_config)
        expected_calls = [mock.call("../config.json"), mock.call("./config.json")]
        self.assertEqual(mock_open.call_args_list, expected_calls)

    @mock.patch("utils.open")
    def test_custom_path_called(self, mock_open):
        """
        Tests
        1. When both default paths are not found, utils.get_config will throw an IOError
        2. That both expected default paths are checked
        """
        mock_open.side_effect = FileNotFoundError
        self.assertRaises(IOError, utils.get_config, "./my_path")
        expected_calls = [mock.call("./my_path")]
        self.assertEqual(mock_open.call_args_list, expected_calls)

    @mock.patch("utils.open", create=True)
    def test_file_read_result(self, mock_open):
        test_file_pathname = "/random/path/here/doesnt/matter"
        # This is some completely random unrelated json
        test_json_string = '[{"index": 4, "guid": "3919a105-5368-40bc-8fdb-36e76fb98236", "isActive": true}, {"index": 5, "guid": "0f014356-b098-41d8-9e4e-86bc47d250b8", "isActive": true}]'
        test_parsed_json = [{'guid': '3919a105-5368-40bc-8fdb-36e76fb98236', 'index': 4, 'isActive': True}, {'guid': '0f014356-b098-41d8-9e4e-86bc47d250b8', 'index': 5, 'isActive': True}]
        mock_open.side_effect = mock.mock_open(read_data=test_json_string)
        self.assertEqual(test_parsed_json, utils.get_config(test_file_pathname))
        mock_open.assert_called_once_with(test_file_pathname)
