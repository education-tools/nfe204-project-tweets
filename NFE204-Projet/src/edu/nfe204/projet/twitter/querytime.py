# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
import logging


class QueryTime:

    def __init__(self, backMinutes):
        self.logger = logging.getLogger(__name__)
        self.backMinutes = backMinutes
        self.queryMinute=-1
        self.queryHour=-1

    description = "Construction de la requete"

    def getQuery(self):
        #Recuperer l'heure courante
        current_time = datetime.time(datetime.utcnow() - timedelta(minutes=self.backMinutes))
        self.queryMinute = current_time.minute
        self.queryHour = current_time.hour
        # Faire HEURE:MINUTE en tenant compte des minutes inférieures à 10
        minute = '0' + str(current_time.minute)
        minute = minute[-2:]
        time_query = str(current_time.hour) + ":" + minute
        q = '"it\'s ' + time_query + '" OR "its '
        q = q + time_query + '" OR "it is '
        q = q + time_query + '" OR "il est ' + time_query + '"'
        self.logger.debug("La requete : %s", q)
        return q
    def getTimeOfDayMinute(self):
        return self.queryMinute
    
    def getTimeOfDayHour(self):
        return self.queryHour
        