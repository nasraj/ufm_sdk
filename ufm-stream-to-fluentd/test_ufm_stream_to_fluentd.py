import json
import os
from unittest import mock
from unittest.mock import patch, call
import unittest

import configparser
import requests

import ufm_stream_to_fluentd
from ufm_stream_to_fluentd import FluentdMessageMetadata


class MyTestCase(unittest.TestCase):
    ufm_stream_to_fluentd.args = mock.Mock()

    def setUp(self):
        ufm_stream_to_fluentd.enabled_streaming_systems = True
        ufm_stream_to_fluentd.enabled_streaming_ports = True
        ufm_stream_to_fluentd.enabled_streaming_links = True
        ufm_stream_to_fluentd.enabled_streaming_alarms = True

    def tearDown(self):
        return

    def test_send_request(self):
        with patch('ufm_stream_to_fluentd.requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.raise_for_status.side_effect = requests.exceptions.HTTPError
            # Test Remote Streaming case
            ufm_stream_to_fluentd.local_streaming = False
            ufm_stream_to_fluentd.ufm_protocol = "http"
            ufm_stream_to_fluentd.ufm_host = "ufm"
            ufm_stream_to_fluentd.ufm_username = "admin"
            ufm_stream_to_fluentd.ufm_password = "123456"
            mocked_get.raise_for_status.return_value = None
            mocked_get.return_value.status_code = 200
            ufm_stream_to_fluentd.send_ufm_request(ufm_stream_to_fluentd.UFM_API_VERSIONING)
            mocked_get.assert_called_with(f"http://ufm/ufmRest/{ufm_stream_to_fluentd.UFM_API_VERSIONING}",
                                          verify=False, headers={},
                                          auth=(ufm_stream_to_fluentd.ufm_username, ufm_stream_to_fluentd.ufm_password))

            # Test local streaming case
            ufm_stream_to_fluentd.local_streaming = True
            ufm_stream_to_fluentd.internal_ufm_server_port = "80"
            ufm_stream_to_fluentd.send_ufm_request(ufm_stream_to_fluentd.UFM_API_VERSIONING)
            mocked_get.assert_called_with(f"http://127.0.0.1:80/{ufm_stream_to_fluentd.UFM_API_VERSIONING}",
                                          verify=False, headers={'X-Remote-User': ufm_stream_to_fluentd.ufm_username})

            # Test non working API
            mocked_get.return_value.ok = False
            ufm_stream_to_fluentd.send_ufm_request(ufm_stream_to_fluentd.UFM_API_VERSIONING)
            self.assertRaises(expected_exception=Exception)

    def test_update_ufm_apis(self):
        with patch('ufm_stream_to_fluentd.write_json_to_file') as mocked_write:
            with patch('ufm_stream_to_fluentd.send_ufm_request') as mocked_send_request:
                ufm_stream_to_fluentd.stored_versioning_api = ""
                ufm_stream_to_fluentd.update_ufm_apis()
                self.assertEqual(mocked_send_request.call_count, 5)
                calls = [call.send_ufm_request(ufm_stream_to_fluentd.UFM_API_VERSIONING),
                         call.send_ufm_request(ufm_stream_to_fluentd.UFM_API_SYSTEMS),
                         call.send_ufm_request(ufm_stream_to_fluentd.UFM_API_PORTS),
                         call.send_ufm_request(ufm_stream_to_fluentd.UFM_API_LINKS)]
                mocked_send_request.assert_has_calls(calls, any_order=False)

    def test_write_to_json(self):
        json_object = {"name": "abc", "text": "sample"}
        path = "api_results/test"
        ufm_stream_to_fluentd.write_json_to_file(path, json_object)
        with open(path) as f:
            data = json.load(f)
            f.close()
            os.remove(path)
        self.assertDictEqual(json_object, data)
        raised = None
        try:
            ufm_stream_to_fluentd.write_json_to_file(path, json_object)
        except Exception as ex:
            raised = ex
        self.assertIsNone(raised, "Exception is not handled: " + raised if raised else "")

    def test_read_from_json(self):
        json_object = {"name": "abc", "text": "sample"}
        path = "api_results/test"
        f = open(path, "w")
        f.write(json.dumps(json_object))
        f.close()
        data = ufm_stream_to_fluentd.read_json_from_file(path)
        self.assertDictEqual(json_object, data)

    @patch('ufm_stream_to_fluentd.time.time', return_value=0)
    def test_stream_to_fluentd(self, mocked_time):
        ufm_stream_to_fluentd.fluentd_host = "host"
        ufm_stream_to_fluentd.fluentd_port = "123"
        ufm_stream_to_fluentd.ufm_server_name = ""
        ufm_stream_to_fluentd.fluentd_metadata = FluentdMessageMetadata(1)
        attrs = ['enabled_streaming_systems', 'enabled_streaming_ports', 'enabled_streaming_links'
            , 'enabled_streaming_alarms']
        attrs_dict = {
            'enabled_streaming_systems': 'systems',
            'enabled_streaming_ports': 'ports',
            'enabled_streaming_links': 'links',
            'enabled_streaming_alarms': 'alarms'
        }
        for attr in attrs:
            setattr(ufm_stream_to_fluentd, attr, False)

        with patch('ufm_stream_to_fluentd.FluentSender') as fluent:
            for attr in attrs:
                setattr(ufm_stream_to_fluentd, attr, True)
                ufm_stream_to_fluentd.stream_to_fluentd()
                self.assertTrue(attrs_dict[attr] in fluent.return_value.send.call_args.args[0], 'Property ' + attr
                                + ' doesn\'t Exists in response')

    def test_load_memory_with_jsons(self):
        if os.path.isfile(ufm_stream_to_fluentd.UFM_API_VERSIONING_RESULT):
            os.remove(ufm_stream_to_fluentd.UFM_API_VERSIONING_RESULT)
        if os.path.isfile(ufm_stream_to_fluentd.UFM_API_SYSTEMS_RESULT):
            os.remove(ufm_stream_to_fluentd.UFM_API_SYSTEMS_RESULT)
        if os.path.isfile(ufm_stream_to_fluentd.UFM_API_LINKS_RESULT):
            os.remove(ufm_stream_to_fluentd.UFM_API_LINKS_RESULT)
        if os.path.isfile(ufm_stream_to_fluentd.UFM_API_PORTS_RESULT):
            os.remove(ufm_stream_to_fluentd.UFM_API_PORTS_RESULT)
        if os.path.isfile(ufm_stream_to_fluentd.UFM_API_ALARMS_RESULT):
            os.remove(ufm_stream_to_fluentd.UFM_API_ALARMS_RESULT)

        # Test case when no json file exists
        with patch('ufm_stream_to_fluentd.read_json_from_file') as mocked_read:
            mocked_read.return_value = {}
            ufm_stream_to_fluentd.load_memory_with_jsons()
            self.assertEqual(mocked_read.call_count, 0)

        # Test case when json files exist
        with patch('ufm_stream_to_fluentd.read_json_from_file') as mocked_read:
            with patch('ufm_stream_to_fluentd.send_ufm_request') as mocked_send_request:
                mocked_read.return_value = {}
                mocked_send_request.return_value = {}
                ufm_stream_to_fluentd.update_ufm_apis()
                ufm_stream_to_fluentd.load_memory_with_jsons()
                self.assertEqual(mocked_read.call_count, 5)

    def test_get_config_value(self):
        config_file = 'test_ufm_stream_to_fluentd.cfg'
        ufm_stream_to_fluentd.CONFIG = configparser.RawConfigParser()
        ufm_stream_to_fluentd.CONFIG.read(config_file)
        args = {
            'param1': 'ok'
        }
        self.assertTrue(ufm_stream_to_fluentd.get_config_value(args.get('param1'), 'params-section', 'param1') == 'ok',
                        'Test Fails for value in arg')
        self.assertTrue(ufm_stream_to_fluentd.get_config_value(args.get('param2'), 'params-section', 'param2') == '80',
                        'Test Fails for value in config file')
        self.assertTrue(ufm_stream_to_fluentd.get_config_value(args.get('param3'), 'params-section', 'param3', 'defaultValue') == 'defaultValue',
                        'Test Fails for default value')
        with self.assertRaises(ValueError):
            ufm_stream_to_fluentd.get_config_value(args.get('param4'), 'params-section', 'param4')




if __name__ == '__main__':
    unittest.main()
