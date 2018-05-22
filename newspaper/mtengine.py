'''

Methods to run MT engines
subclass to corpus

'''

import logging
import abc


class MTEngine:

    @abc.abstractmethod
    def train(self):
        """Run a training step with a prepared corpus"""
        return

    # prepare corpus for a training step


class SockeyeEngine(MTEngine):

   def train(self):
       logging.info("Training with Sockeye")
