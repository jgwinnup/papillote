'''

Methods to run MT engines
subclass to corpus

'''

import logging
import abc
import sys


class MTEngine:

    @abc.abstractmethod
    def train(self):
        """Run a training step with a prepared corpus"""
        return

    # prepare corpus for a training step


class SockeyeEngine(MTEngine):

    # This assumes you're already in a venv with sockeye available
    def train(self, step, work_dir, train_epochs):
        logging.info("Sockeye: Training Step {0} for {1} epochs in {2}".format(step, train_epochs, work_dir))


