'''

Methods to run MT engines
subclass to corpus

'''

import logging
import abc
import subprocess
import os

# helper class
# https://stackoverflow.com/questions/431684
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

class MTEngine:

    @abc.abstractmethod
    def train(self):
        """Run a training step with a prepared corpus"""
        return

    # prepare corpus for a training step


class SockeyeEngine(MTEngine):

    # This assumes you're already in a venv with sockeye available
    def train(self, step, work_dir, train_epochs, rel_valid_source, rel_valid_target):
        logging.info("Sockeye: Training Step {0} for {1} epochs in {2}".format(step, train_epochs, work_dir))

        # get current working directory so we don't hose paths when switching to work dir
        cwd = os.getcwd()

        step_dir = '{0}/step{1}'.format(work_dir, step)
        valid_source = '{0}/{1}'.format(cwd, rel_valid_source)
        valid_target = '{0}/{1}'.format(cwd, rel_valid_target)

        # build executable string
        # why does python need a command as an array of strings?
        cmd = ["python", "-m",  "sockeye.train",
               "--source", "source",
               "--target", "target",
               "--validation-source", valid_source,
               "--validation-target", valid_target,
               "--output", "model",
               "--max-num-epochs", train_epochs]

        print(" ".join(cmd))

        # change to working dir
        with cd(step_dir):
            print("cwd now: {0}".format(os.getcwd()))
            subprocess.call(cmd)

        logging.info("Sockeye: Finished train for step {0}".format(step))


class MarianEngine(MTEngine):

    # This assumes you're already in a venv with sockeye available
    def train(self, step, work_dir, train_epochs, rel_valid_source, rel_valid_target):
        logging.info("Marian: Training Step {0} for {1} epochs in {2}".format(step, train_epochs, work_dir))