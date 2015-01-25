# -*- coding: utf-8 -*-
import rethinkdb as r
import logging


class RethinkdbManager:

    def __init__(self, rdbHost, rdbPort, rdbDB, rdbPwd, rdbTimeout):
        self.logger = logging.getLogger(__name__)
        self.table = 'test_tweet3'
        self.conn = r.connect(host=rdbHost, port=rdbPort, db=rdbDB, auth_key=rdbPwd, timeout=rdbTimeout).repl()

    def insertTweets(self, tweets):
        self.logger.info("Insertion de %s tweets.", len(tweets))
        try:
            r.table(self.table).insert(tweets).run()
        except r.RqlRuntimeError, e:
            self.logger.critical("Erreur lors de l'insertion. Message %s", e, exc_info=True)
            raise e

    def disconnect(self):
        self.conn.close(noreply_wait=False)