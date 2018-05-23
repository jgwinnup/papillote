
"""
Start-stop training wrapper for Sockeye

"""

import argparse
import logging
import os
import subprocess

from newspaper.corpus import prep
from newspaper.database import create_database, populate_db
from newspaper.mtengine import SockeyeEngine


def main():

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    logging.info("Newspaper!")

    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="source corpus")
    parser.add_argument("--target", help="target corpus")
    parser.add_argument("--scores", help="corpus scores")
    parser.add_argument("--db", help="sqlite db name")
    parser.add_argument("--work-dir", help="working directory", default="work")
    parser.add_argument("--steps", help="number of training passes", default=5)
    parser.add_argument("--bound-lower", help="starting lower bound of score", default=0.8)
    parser.add_argument("--bound-upper", help="starting upper bound of score", default=1.0)
    parser.add_argument("--bound-step",  help="amount to move score per step", default=0.2)
    parser.add_argument("--train-epochs", help="number of epochs to train", default=10)
    args = parser.parse_args()

    # run info
    logging.info("All settings used:")

    for arg in vars(args):
        logging.info("{0}: {1}".format(arg, getattr(args, arg)))

    # create + populate database
    db = create_database(args.db)
    populate_db(db, args.source, args.target, args.scores)

    # create working dir if not exists
    directory = args.work_dir
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info("Creating work dir %s" % args.work_dir)
    else:
        logging.warning("Work dir %s already exists!" % args.work_dir)

    # convenience variables to iterate over
    bound_upper = args.bound_upper
    bound_lower = args.bound_lower
    bound_step = args.bound_step

    # one-based? zero-based?

    engine = SockeyeEngine()

    for step in range(1, args.steps):
        prep(step, args.work_dir, db, bound_lower, bound_upper)
        # adjust params for next step
        bound_upper -= bound_step
        bound_lower -= bound_step

        engine.train(step, args.work_dir, args.train_epochs)


if __name__ == "__main__":
    main()


