import sqlite3
import pymysql
from ..models import market_analytics_model
class market_analytics_action:
    def __init__(self, db_connection) -> None:
        self.db_connection = db_connection
    def add(self, market_analytics: market_analytics_model.market_analytics):
        conn = self.db_connection
        cursor = conn.cursor()

        print(" này là action ", market_analytics.match_id)
        sql = """
                INSERT INTO market_analytics(match_id,selling,newest, popular, timeupdate) VALUES(%s, %s, %s, %s, %s)
                """
        cursor.execute(sql, (market_analytics.match_id,market_analytics.selling,market_analytics.newest,market_analytics.popular,market_analytics.timeupdate))
        conn.commit()
        return "Insert:Success!",200


    def get_by_match_id(self, match_id):
        conn = self.db_connection
        cursor = conn.cursor()
        sql = """
            SELECT *
            FROM market_analytics
            WHERE  timeupdate = (
                SELECT MAX(timeupdate) 
                FROM market_analytics
                WHERE  match_id = %s)
        """
        #dạng toppge truyền tham số
        #(a,b,c)
        cursor.execute(sql, (match_id, ))
        #id duy nhất fetchone
        row = cursor.fetchone();
        result = []
        print(row)
        if row == None:
            # ko có id truyền vào = vs id  bảng chart1
            return  "error",404
        
        Market_analytics_model = market_analytics_model.market_analytics(
            market_id= row[0],
            match_id=row[1],
            selling=row[2], 
            newest= row[3],
            popular= row[4],
            timeupdate= row[5],          
            )
       
        result.append( Market_analytics_model.serialize())
        return result,200
