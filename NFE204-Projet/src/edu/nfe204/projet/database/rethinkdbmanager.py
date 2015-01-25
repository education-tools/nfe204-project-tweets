# -*- coding: utf-8 -*-
import rethinkdb as r
import logging


class RethinkdbManager:

    def __init__(self, rdbHost, rdbPort, rdbDB, rdbPwd, rdbTimeout):
        self.logger = logging.getLogger(__name__)
        self.conn = r.connect(host=rdbHost, port=rdbPort, db=rdbDB, auth_key=rdbPwd, timeout=rdbTimeout).repl()

    def insertTweets(self, tweets, tableName):        
        if (len(tweets) > 0):
            self.logger.debug("Insertion de %s tweets dans '%s'.", len(tweets), tableName)
            try:
                resultInsert = r.table(tableName).insert(tweets, return_changes=False, conflict="replace").run()
                self.logger.info("Resultat de l'insertion dans '%s': inserted=%s, replaced=%s, unchanged=%s, error=%s",
                            tableName,
                            resultInsert.get('inserted'),
                            resultInsert.get('replaced'),
                            resultInsert.get('unchanged'),
                            resultInsert.get('error'))
            except r.RqlRuntimeError, e:
                self.logger.critical("Erreur lors de l'insertion. Message %s", e, exc_info=True)
                raise e
        else:
            self.logger.info("Aucun tweet a inserer.")
            
    def disconnect(self):
        self.conn.close(noreply_wait=False)