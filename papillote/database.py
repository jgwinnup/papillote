import logging
import sqlite3


def create_database(dbname):

    logging.info("Creating db: %s" % dbname)
    db = sqlite3.connect(dbname)
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
    cursor.execute('''
      DROP TABLE IF EXISTS corpus
    ''')
    cursor.execute('''
      CREATE TABLE corpus(id INTEGER PRIMARY KEY, source TEXT,
                          target TEXT, score REAL)
    ''')
    db.commit()

    return db


def populate_db(db, sourcefile, targetfile, scorefile):

    ctr = 0

    source = open(sourcefile, encoding="utf-8")
    target = open(targetfile, encoding="utf-8")
    scores = open(scorefile, encoding="utf-8")

    try:
        with open(sourcefile, 'r') as source, open(targetfile, 'r') as target, open(scorefile, 'r') as scores:
            for (source_line, target_line, score_line) in zip(source, target, scores):

                cursor = db.cursor()
                sql = '''INSERT into corpus VALUES(?, ?, ?, ?)'''
                task = (ctr, source_line, target_line, score_line)
                cursor.execute(sql, task)

                ctr += 1
            # actually commit the data
            db.commit()

    except IOError as e:
        logging.warning("Danger! %s" % e.strerror)

    logging.info("Inserted %s sentence pairs" % ctr)


def query_corpus(db, bound_lower, bound_upper):

    try:
        cursor = db.cursor()
        # pre-random the result so that we don't get into an ordering fit
        sql = '''SELECT * from corpus WHERE score <= ? AND score >= ? ORDER BY RANDOM()'''
        task = (bound_upper, bound_lower)
        cursor.execute(sql, task)
        return cursor.fetchall()

    except IOError as e:
        logging.warning("Error: %s" % e.strerror)
        return None