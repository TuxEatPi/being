import os
import json
import time

import daemonocle
import pytest

from tuxeatpi_common.cli import main_cli, set_daemon_class
from tuxeatpi_time.daemon import Time
from tuxeatpi_common.message import Message, MqttClient
import paho.mqtt.client as paho


from click.testing import CliRunner

class TestMQTT(object):

    @classmethod
    def setup_class(self):
        intent_folder = os.path.join(os.getcwd(), 'intents')
        dialog_folder = os.path.join(os.getcwd(), 'dialogs')
        if not os.path.exists(intent_folder):
           os.makedirs(intent_folder)
        if not os.path.exists(dialog_folder):
           os.makedirs(dialog_folder)
        daemon = daemonocle.Daemon()
        self.time_daemon = Time(daemon, 'timedaemon', intent_folder, dialog_folder)
        self.time_daemon.dialog_handler.load()
        self.time_daemon._mqtt_client.run()
        self.time_daemon.language = "en_US"
        self.message = None

        def get_message(mqttc, obj, msg):
            payload = json.loads(msg.payload.decode())
            self.message = payload.get("data", {}).get("arguments", {})
        self.mqtt_client = paho.Client()
        self.mqtt_client.connect("127.0.0.1", 1883, 60)
        self.mqtt_client.on_message = get_message
        self.mqtt_client.subscribe("speak/say", 0)
        self.mqtt_client.loop_start()

    @classmethod
    def teardown_class(self):
       self.message = None
       self.mqtt_client.loop_stop()

    @pytest.mark.order1
    def test_time(self, capsys):
        self.time_daemon.time_()
        time.sleep(3)
        assert self.message.get("text") is not None

    @pytest.mark.order2
    def test_day(self, capsys):
        self.time_daemon.day()
        time.sleep(3)
        assert self.message.get("text") is not None
