'''
Corpus methods
'''
import logging
import os

from newspaper.database import query_corpus


def prep(step, workdir, db, bound_lower, bound_upper):

    stepdir = "{0}/step{1}".format(workdir, step)

    logging.info("Preparing corpus for step {0} in {1}".format(step , stepdir))

    # make working directory
    if not os.path.exists(stepdir):
        os.makedirs(stepdir)
        logging.info("Creating work dir %s" % stepdir)
    else:
        logging.warning("Work dir %s already exists!" % stepdir)

    corpus = query_corpus(db, bound_lower, bound_upper)

    # 0 - orig row id
    # 1 - source sent
    # 2 - target sent
    # 3 - score

    max_score = 0.0
    min_score = 1.0
    avg_score = 0.0
    mean_score = 0.0

    ctr = 0
    sourcefile = "{0}/source".format(stepdir)
    targetfile = "{0}/target".format(stepdir)
    scorefile  = "{0}/scores".format(stepdir)
    try:
        with open(sourcefile, 'w') as source, open(targetfile, 'w') as target, open(scorefile, 'w') as scores:
            for row in corpus:
                #print("id %s: score: %s" % (row[0], row[3]))

                #writes
                source.writelines(row[1])
                target.writelines(row[2])
                scoreline = "{0} {1}".format(row[0], row[3])
                scores.writelines(scoreline)

                #maths
                score = row[3]
                avg_score += score
                if score < min_score:
                    min_score = score
                elif score > max_score:
                    max_score = score


                ctr += 1

        avg_score = avg_score / ctr

        logging.info("Wrote {0} lines with min score {1}, max score {2}, avg score {3}".format(ctr, min_score, max_score, avg_score))
        source.close()
        target.close()
        scores.close()

    except IOError as e:
        logging.warning("IOError: %s", e.strerror)