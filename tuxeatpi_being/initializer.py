"""Module customizing initialization for the Brain component"""
import time

from tuxeatpi_common.initializer import Initializer


class BeingInitializer(Initializer):
    """Custom initializer for the Brain component"""

    def __init__(self, component, skip_dialogs=False, skip_intents=False, skip_settings=False):
        Initializer.__init__(self, component, skip_dialogs, skip_intents, skip_settings)

    def _check_birthdate(self):
        """Read config file and save it in Etcd"""
        while self.component.birthdate_ is None:
            self.component.birthdate_ = self.component.memory.read('birthdate')
            if self.component.birthdate_ is None:
                self.logger.critical("Can not get birthdate in memory, retrying")

        if not self.component.birthdate_:
            self.logger.warning("TuxEatPi Birth detected !!!")
            self.component.birthdate_ = time.time()
            self.component.memory.save('birthdate', self.component.birthdate_)
        # TODO create a birthdate scenario ??!!

    def run(self):
        """Run method overriding the standard one"""
        # Read config file
        self._check_birthdate()
        # Standard start
        Initializer.run(self)
