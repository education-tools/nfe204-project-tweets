import unittest
import nfe204Projet
import logging
from edu.nfe204.projet.twitter.twittermanager import TwitterManager
import json


class Test(unittest.TestCase):


    def setUp(self):
        configFile = '../resources/config_secret.ini'
        self.config = nfe204Projet.loadConfig(configFile)
        nfe204Projet.initLogging(self.config)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Execution du script avec le fichier de configuration %s",configFile)


    def tearDown(self):
        pass


    def testGetTweets(self):
        twit = TwitterManager(
                          self.config.get(nfe204Projet.SECTION_TWITTER, nfe204Projet.OPT_CONSUMER_KEY),
                          self.config.get(nfe204Projet.SECTION_TWITTER, nfe204Projet.OPT_CONSUMER_SECRET),
                          self.config.get(nfe204Projet.SECTION_TWITTER, nfe204Projet.OPT_OAUTH_TOKEN),
                          self.config.get(nfe204Projet.SECTION_TWITTER, nfe204Projet.OPT_OAUTH_TOKEN_SECRET))

        tweets = twit.getTweets(self.config.getint(nfe204Projet.SECTION_QUERY, nfe204Projet.OPT_MAX_COUNT),
                            self.config.getint(nfe204Projet.SECTION_QUERY, nfe204Projet.OPT_MAX_RANGE))
    
        self.logger.debug(json.dumps(tweets, indent=1))
        self.assertIsNotNone(tweets, 'Test en erreur')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()