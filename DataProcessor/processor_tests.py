#!/usr/bin/env python

import unittest
import socket, time
import simplejson as json
from subprocess import Popen, PIPE

import DataProcessor, EventSender

class TestConvertingData(unittest.TestCase):
    pass

class TestSendingEvent(unittest.TestCase):
    def setUp(self):
        self.config = json.load(open('resources/config.json', 'r'))
        port = self.config['socket_port']
        self.server_process = Popen(['python', 'MockServer.py', 'resources/config.json'], stdout=PIPE)
        time.sleep(1)
        self.client = EventSender.EventSender(port)
    def test_send_event(self):
        event = '{"sound_bank": "synth_waves", "features": {"pitch": 587.3, "wave_type": "square"}}'
        event_json = json.loads(event)
        self.client.send_event(event_json)
        self.client.send_exit_event()
        out = self.server_process.stdout.read()
        self.assertEqual(json.loads(event), json.loads(out))
    def tearDown(self):
        self.server_process.terminate()

class TestSendingMultipleEvents(unittest.TestCase):
    def setUp(self):
        self.config = json.load(open('resources/config.json', 'r'))
        port = self.config['socket_port']
        self.server_process = Popen(['python', 'MockServer.py', 'resources/config.json'], stdout=PIPE)
        time.sleep(1)
        self.client = EventSender.EventSender(port)
    def test_send_event(self):
        events = ['{"sound_bank": "synth_waves", "features": {"pitch": 587.3, "wave_type": "square"}}',
                '{"sound_bank": "synth_waves", "features": {"pitch": 659.3, "wave_type": "square"}}',
                '{"sound_bank": "synth_waves", "features": {"pitch": 987.8, "wave_type": "sine"}}']
        for event in events:
            event_json = json.loads(event)
            self.client.send_event(event_json)
        self.client.send_exit_event()
        out = self.server_process.stdout.read().split('\n')
        for event, line in zip(events, out):
            self.assertEqual(json.loads(event), json.loads(line))
    def tearDown(self):
        self.server_process.terminate()

class TestReadingConfig(unittest.TestCase):
    def setUp(self):
        self.config = json.load(open('resources/config.json', 'r'))
        self.server_process = Popen(['python', 'MockServer.py', 'resources/config.json'], stdout=PIPE)
        time.sleep(1)
    def test_config_reading(self):
        ds = DataProcessor.DataProcessor('resources/config.json')
        this_config = json.load(open('resources/config.json', 'r'))
        self.assertEqual(ds.config['socket_port'], this_config['socket_port'])
        self.assertEqual(ds.config['sound_bank'], this_config['sound_bank'])
    def tearDown(self):
        self.server_process.terminate()

class TestRescalingData(unittest.TestCase):
    pass

if __name__=='__main__':
    unittest.main()
