from datetime import datetime
from pytz import timezone

from PlayerStatsTracker import PlayerStatsTracker 
from DynamoAccess import DynamoAccess 
from Ranker import Ranker

class DbUpdater(object): 
    def __init__(self, match_id):  
        self.match_id = match_id
        self.dynamo_access = DynamoAccess()

        self.stats = PlayerStatsTracker(match_id)  
        self.batting_points = self.stats.GetBattingPoints() 
        self.bowling_points = self.stats.GetBowlingPoints() 
        self.fielding_points = self.stats.GetFieldingPoints() 
        self.summary_points = self.stats.GetSummaryPoints()  
        
        self.ranker = Ranker(self.match_id, self.summary_points) 
        self.player_ranks = self.ranker.RankUsers() 

    def UpdateDataInDynamo(self): 
        ''' 
            map batting/bowling/fielding/summary/total 
            upload each to dynamo 
        '''   
        records = { 'match_id': self.match_id,   
                    'fantasy_ranks': self.player_ranks,
                    'batting_points': self.batting_points, 
                    'bowling_points': self.bowling_points, 
                    'fielding_points': self.fielding_points, 
                    'summary_points' : self.summary_points, 
                    'last_updated' : self.GetCurrentTimeInEst()         
                  } 
        self.dynamo_access.UpdateAllPoints(records) 
    
    def GetCurrentTimeInEst(self):  
        # Get the current time in UTC
        now_utc = datetime.utcnow()

        # Format the time as a string and return it 
        time_str = now_utc.strftime('%Y-%m-%d %H:%M:%S UTC') 
        return time_str

             
        

def CheckLambdaPreConditions(match_id):  
    result = False
    dynamo_access = DynamoAccess() 
    scorecard_details = dynamo_access.GetScorecardInfo(match_id) 
    scorecard_link = scorecard_details['scorecard_link']  

    if len(scorecard_link) > 5: 
        result = True 
    
    return result

def handle(event, context):  
    match_id = event['match_id']  
    print(f'got match id {match_id}') 
    if CheckLambdaPreConditions(match_id):
        db_updater = DbUpdater(match_id) 
        db_updater.UpdateDataInDynamo()
        return 'dynamo updated'
    
    return 'scorecard not available yet'


if __name__ == "__main__": 
    handle({'match_id':'1348655'},{})
