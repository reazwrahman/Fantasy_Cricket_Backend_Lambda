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
        #print(self.summary_points) 
        print('\n') 
        print ('\n')
        #print(self.player_ranks) 
        
        records = { 'match_id': self.match_id,   
                    'fantasy_ranks': self.player_ranks,
                    'batting_points': self.batting_points, 
                    'bowling_points': self.bowling_points, 
                    'fielding_points': self.fielding_points, 
                    'summary_points' : self.summary_points,           
                  } 
        self.dynamo_access.UpdateAllPoints(records)
             
        

def CheckLambdaPreConditions(match_id):  
    result = False
    dynamo_access = DynamoAccess() 
    game_details = dynamo_access.GetGameDetails(match_id) 
    scorecard_link = game_details['scorecard_link']  

    if len(scorecard_link) > 5: 
        result = True 
    
    return result

def handle(event, context):  
    ''' 
        get match id 
        use that to update points in dynamo 
        update ranking in dynamo 
        die peacefully
    '''   
    match_id = event['match_id']  
    print(f'got match id {match_id}') 
    if CheckLambdaPreConditions(match_id):
        db_updater = DbUpdater(match_id) 
        db_updater.UpdateDataInDynamo()
        return 'dynamo updated'
    
    return 'scorecard not available yet'


if __name__ == "__main__": 
    handle({'match_id':'4321'},{})


#TODO 
''' 
[DONE] setup git repo!! first, would hate to lose my work!!!!
[DONE] try do an initial deployment in aws lambda, so we have a benchmark
[DONE] tomorrow: setup proper dynamo access 
[DONE] so we can make the calls from the interface 
[DONE] implement the write calls first 
if time allows do the read calls too
'''