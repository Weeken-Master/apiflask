from datetime import datetime


class market_analytics:
    def __init__(self, market_id=0, match_id='',selling ='',newest ='',popular ='',timeupdate=datetime ):
        self.market_id= market_id
        self.match_id = match_id 
        self.selling  = selling
        self.newest = newest
        self.popular  = popular
        self.timeupdate = timeupdate

    def serialize(self):
        return {
            'market_id': self.market_id,
            'match_id': self.match_id,
            'selling': self.selling,
            'newest' : self.newest,
            'popular': self.popular,
            'timeupdate':self.timeupdate,
        }