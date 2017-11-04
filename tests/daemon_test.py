import os
import json
import time
import threading

import pytest
from wampy.peers import Client

from tuxeatpi_common.cli import main_cli, set_daemon_class
from tuxeatpi_being.daemon import Being
from tuxeatpi_common.message import Message


from click.testing import CliRunner

class TestTime(object):

    @classmethod
    def setup_method(self):
        workdir = "tests/workdir"
        intents = "intents"
        dialogs = "dialogs"
        self.being_daemon = Being('being_test', workdir, intents, dialogs)
        self.being_daemon.settings.language = "en_US"
        self.message = None

        def speech_say(text):
            self.message = text

        self.wamp_client = Client(realm="tuxeatpi")
        self.wamp_client.start()

        self.wamp_client.session._register_procedure("speech.say")
        setattr(self.wamp_client, "speech.say", speech_say)

    @classmethod
    def teardown_method(self):
        self.message = None
        self.being_daemon.settings.delete("/config/global")
        self.being_daemon.settings.delete("/config/being_test")
        self.being_daemon.settings.delete()
        self.being_daemon.registry.clear()
        self.being_daemon.memory.delete("birthdate")
        try:  # CircleCI specific
            self.being_daemon.shutdown()
        except (AttributeError, RuntimeError):
            pass
        time.sleep(1)

    @pytest.mark.order1
    def test_name(self, capsys):
        t = threading.Thread(target=self.being_daemon.start)
        t = t.start()

        global_config = {"language": "en_US",
                         "nlu_engine": "fake_nlu",
                         }
        self.being_daemon.settings.save(global_config, "global")
        config = {}
        self.being_daemon.settings.save(config)
        self.being_daemon.set_config(config)

        time.sleep(1)

        assert self.message is None
        self.being_daemon.name__()
        time.sleep(1)
        assert self.message is not None

    @pytest.mark.order2
    def test_birthday(self, capsys):
        t = threading.Thread(target=self.being_daemon.start)
        t = t.start()
        time.sleep(1)

        assert self.being_daemon.birthdate_ is not None

        global_config = {"language": "en_US",
                         "nlu_engine": "fake_nlu",
                         }
        self.being_daemon.settings.save(global_config, "global")
        config = {}
        self.being_daemon.settings.save(config)
        self.being_daemon.set_config(config)

        assert self.message is None
        self.being_daemon.birthday()
        time.sleep(1)
        assert self.message is not None

    @pytest.mark.order3
    def test_birthdate(self, capsys):
        t = threading.Thread(target=self.being_daemon.start)
        t = t.start()
        time.sleep(1)

        assert self.being_daemon.birthdate_ is not None

        global_config = {"language": "en_US",
                         "nlu_engine": "fake_nlu",
                         }
        self.being_daemon.settings.save(global_config, "global")
        config = {}
        self.being_daemon.settings.save(config)
        self.being_daemon.set_config(config)

        assert self.message is None
        self.being_daemon.birthdate()
        time.sleep(1)
        assert self.message is not None

    @pytest.mark.order4
    def test_age(self, capsys):
        t = threading.Thread(target=self.being_daemon.start)
        t = t.start()
        time.sleep(1)

        assert self.being_daemon.birthdate_ is not None

        global_config = {"language": "en_US",
                         "nlu_engine": "fake_nlu",
                         }
        self.being_daemon.settings.save(global_config, "global")
        config = {}
        self.being_daemon.settings.save(config)
        self.being_daemon.set_config(config)

        assert self.message is None
        self.being_daemon.age()
        time.sleep(1)
        assert self.message is not None
