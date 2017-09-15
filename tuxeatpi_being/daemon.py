"""Module defining Get time/day component daemon"""
import logging
import time
import locale
import datetime

import agecalc
from tuxeatpi_common.message import Message, is_mqtt_topic
from tuxeatpi_common.daemon import TepBaseDaemon
from tuxeatpi_common.error import TuxEatPiError

from tuxeatpi_being.initializer import BeingInitializer


class Being(TepBaseDaemon):
    """Component giving time and day"""

    def __init__(self, name, workdir, intent_folder, dialog_folder, logging_level=logging.INFO):
        TepBaseDaemon.__init__(self, name, workdir, intent_folder, dialog_folder, logging_level)
        self.name_ = None
        self.birthdate_ = None
        # Skip witing for config
        self._initializer = BeingInitializer(self)

    def main_loop(self):
        time.sleep(1)

    def set_config(self, config):
        """Save the configuration and reload the daemon"""
        self.name_ = config.get("name")
        return True

    @is_mqtt_topic("help")
    def help_(self):
        """Help for time component"""
        pass

    @is_mqtt_topic("name")
    def name__(self):
        """Get name"""
        self.logger.info("being/name called")
        # Get dialog
        dialog = self.get_dialog("name", name=self.name_)
        # Prepare message
        data = {"arguments": {"text": dialog}}
        topic = "speech/say"
        message = Message(topic=topic, data=data)
        # Send message
        self.publish(message)

    @is_mqtt_topic("birthdate")
    def birthdate(self):
        """Return birth"""
        self.logger.info("being/birthdate called")
        # Get time format
        day_format = locale.nl_langinfo(locale.D_FMT)
        birthdate_datetime = datetime.datetime.fromtimestamp(self.birthdate_)
        birth_fmt = birthdate_datetime.strftime(day_format)
        # Get dialog
        dialog = self.get_dialog("birthdate", birth=birth_fmt,
                                 year=birthdate_datetime.year,
                                 month=birthdate_datetime.month,
                                 day=birthdate_datetime.day)
        # Prepare message
        data = {"arguments": {"text": dialog}}
        topic = "speech/say"
        message = Message(topic=topic, data=data)
        # Send message
        self.publish(message)

    @is_mqtt_topic("birthday")
    def birthday(self):
        """Return birthday"""
        self.logger.info("being/birthday called")
        # Get time format
        day_format = locale.nl_langinfo(locale.D_FMT)
        birthdate_datetime = datetime.datetime.fromtimestamp(self.birthdate_)
        birth_fmt = birthdate_datetime.strftime(day_format)
        month = birthdate_datetime.strftime("%B")
        # Get dialog
        dialog = self.get_dialog("birthdate", birthday=birth_fmt,
                                 month=month,
                                 day=birthdate_datetime.day)
        # Prepare message
        data = {"arguments": {"text": dialog}}
        topic = "speech/say"
        message = Message(topic=topic, data=data)
        # Send message
        self.publish(message)

    @is_mqtt_topic("age")
    def age(self):
        """Get age"""
        self.logger.info("being/age called")
        birth_date = datetime.datetime.fromtimestamp(self.birthdate_)
        age_ = agecalc.AgeCalc(birth_date.day, birth_date.month, birth_date.year)
        dialog = self.get_dialog("age",
                                 days=age_.age_days,
                                 weeks=age_.age_weeks,
                                 months=age_.age_months,
                                 years=age_.age_years_months.get('years', 0),
                                 )
        # Prepare message
        data = {"arguments": {"text": dialog}}
        topic = "speech/say"
        message = Message(topic=topic, data=data)
        # Send message
        self.publish(message)


class BeingError(TuxEatPiError):
    """Base class for brain exceptions"""
    pass
