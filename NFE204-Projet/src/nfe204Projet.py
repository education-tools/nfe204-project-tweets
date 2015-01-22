#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging.config
import json
import ConfigParser
import io
import sys

from edu.nfe204.projet.database.rethinkdbmanager import RethinkdbManager
from edu.nfe204.projet.twitter.twittermanager import TwitterManager


SECTION_LOGGING = 'logging'
OPT_CONFIGFILE = 'config.file'

SECTION_TWITTER = 'twitter'
OPT_CONSUMER_KEY = 'consumer.key'
OPT_CONSUMER_SECRET = 'consumer.secret'
OPT_OAUTH_TOKEN = 'oauth.token'
OPT_OAUTH_TOKEN_SECRET = 'oauth.token.secret'

SECTION_RETHINKDB = 'rethinkdb'
OPT_HOST = 'host'
OPT_PORT = 'port'
OPT_DB = 'db'
OPT_PWD = 'password'
OPT_TIMEOUT = 'timeout'

SECTION_QUERY = 'query'
OPT_MAX_COUNT = 'max.count'
OPT_MAX_RANGE = 'max.range'

def loadConfig(configFile):
    # Charger le fichier de configuration
    with open(configFile) as f:
        sample_config = f.read()
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(sample_config))

    # List all contents
    if (False):
        print("Parametrage du fichier de configuration :"+configFile)
        for section in config.sections():
            print("[%s]" % section)
            for options in config.options(section):
                print("\t%s = %s" % (options,
                                  config.get(section, options)))
    return config

def initLogging(config):
    configFile = config.get(SECTION_LOGGING,OPT_CONFIGFILE)
    logging.config.fileConfig(configFile)
    
def usage():
    print("Usage : nfe204Projet.py configfile")
    
def main():
    if ( len(sys.argv) < 2 ):
        usage()
        exit(1)
        
    config = loadConfig(sys.argv[1])
    initLogging(config)
    logger = logging.getLogger(__name__)
    logger.info("Execution du script avec le fichier de configuration %s",sys.argv[1])
    
    twit = TwitterManager(
                          config.get(SECTION_TWITTER, OPT_CONSUMER_KEY),
                          config.get(SECTION_TWITTER, OPT_CONSUMER_SECRET),
                          config.get(SECTION_TWITTER, OPT_OAUTH_TOKEN),
                          config.get(SECTION_TWITTER, OPT_OAUTH_TOKEN_SECRET))

    tweets = twit.getTweets(config.getint(SECTION_QUERY, OPT_MAX_COUNT),
                            config.getint(SECTION_QUERY, OPT_MAX_RANGE))
    
    logger.debug(json.dumps(tweets, indent=1))
    rdb = RethinkdbManager(config.get(SECTION_RETHINKDB, OPT_HOST),
                           config.getint(SECTION_RETHINKDB, OPT_PORT),
                           config.get(SECTION_RETHINKDB, OPT_DB),
                           config.get(SECTION_RETHINKDB, OPT_PWD),
                           config.getint(SECTION_RETHINKDB, OPT_TIMEOUT))
    #rdb.insertTweets(tweets)
    rdb.disconnect()

    logger.info("Fin du script.")


if __name__ == '__main__':
    main()


