import nfe204Projet
import sys
import logging.config
import rethinkdb as r


def usage():
    print("Usage : queryData.py configfile")

def initLogging(config):
    configFile = config.get(nfe204Projet.SECTION_LOGGING,nfe204Projet.OPT_CONFIGFILE)
    logging.config.fileConfig(configFile)
    
def main():
    if ( len(sys.argv) < 2 ):
        usage()
        exit(1)
    config = nfe204Projet.loadConfig(sys.argv[1])
    nfe204Projet.initLogging(config)
    
    logger = logging.getLogger(__name__)
    logger.info("Execution du script avec le fichier de configuration %s",sys.argv[1])
    
    conn = r.connect(host=config.get(nfe204Projet.SECTION_RETHINKDB, nfe204Projet.OPT_HOST),
                     port=config.getint(nfe204Projet.SECTION_RETHINKDB, nfe204Projet.OPT_PORT),
                     db=config.get(nfe204Projet.SECTION_RETHINKDB, nfe204Projet.OPT_DB),
                     auth_key=config.get(nfe204Projet.SECTION_RETHINKDB, nfe204Projet.OPT_PWD),
                     timeout=config.getint(nfe204Projet.SECTION_RETHINKDB, nfe204Projet.OPT_TIMEOUT),
                     ).repl()
    query(logger)
    conn.close(noreply_wait=False)

def query(logger):
    try:
        cursor = r.table("timeofday").get_all(False, index='retweeted').limit(4).run()
        #cursor = r.table("timeofday").filter(lambda doc:       doc['text'].match("18:")).pluck('id','text').count().run()
        docs = list(cursor)
        for doc in docs:
            logger.debug(doc)
        
    except r.RqlRuntimeError, e:
        logger.critical("Erreur lors de l'insertion. Message %s", e, exc_info=True)
        raise e

if __name__ == '__main__':
    main()