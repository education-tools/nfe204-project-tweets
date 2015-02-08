# -*- coding: utf-8 -*-
import twitter
import logging
from edu.nfe204.projet.twitter.querytime import QueryTime
from urllib2 import URLError

RESULT_TYPE = 'recent'
BEFORE_MINUTES = 5


class TwitterManager:

    def __init__(self, consumerKey, consumerSecret, oauthToken, oauthTokenSecret):
        self.logger = logging.getLogger(__name__)
        self.consumerKey = consumerKey
        self.consumerSecret = consumerSecret
        self.oauthToken = oauthToken
        self.oauthTokenSecret = oauthTokenSecret
        auth = twitter.oauth.OAuth(self.oauthToken, self.oauthTokenSecret,
             self.consumerKey, self.consumerSecret)
        self.twitter_api = twitter.Twitter(auth=auth)

    def getTweets(self, maxCount, maxRange):
        query = QueryTime(BEFORE_MINUTES)
        try:
            self.search_results = self.twitter_api.search.tweets(q=query.getQuery(),
                count=maxCount, result_type=RESULT_TYPE)
        except URLError, e:
            self.logger.critical("Erreur lors de la connection a twitter. Message %s",e, exc_info=True)
            raise e
        self.statuses = self.search_results['statuses']
        self.__iterateThroughResult(maxRange)
        self.logger.debug("Trouve %s tweets", len(self.statuses))
        for tweet in self.statuses:
            tweet['timeofday'] = {'minute': query.getTimeOfDayMinute(),
                                       'hour': query.getTimeOfDayHour()}
        return self.statuses

    def __iterateThroughResult(self, maxRange):

        # Iterer sur maxRange de resultats en utilisant le cursor
        for _ in range(maxRange):
            try:
                next_results = self.search_results['search_metadata']['next_results']
                # Creer un dictionary a partir de next_results, qui a la forme suivante:
                # ?max_id=313519052523986943&q=NCAA&include_entities=1
                kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])
                self.search_results = self.twitter_api.search.tweets(**kwargs)
                self.statuses += self.search_results['statuses']

            except KeyError:  # Plus d'autres résultats'
                break
       

        