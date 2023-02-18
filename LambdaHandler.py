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

    def UpdatePointsInDynamo(self): 
        ''' 
            map batting/bowling/fielding/summary/total 
            upload each to dynamo 
        ''' 
        self.dynamo_access.UpdateSummaryPoints(self.summary_points)
        self.dynamo_access.UpdateBattingPoints(self.batting_points) 
        self.dynamo_access.UpdateBowlingPoints(self.bowling_points) 
        self.dynamo_access.UpdateFieldingPoints(self.fielding_points) 
             

    def UpdateRankingInDynamo(self): 
        ranker = Ranker(self.match_id, self.summary_points) 
        player_ranks = ranker.RankUsers() 
        self.dynamo_access.UpdateUserRanking(player_ranks)  
        print(self.summary_points) 
        print('\n') 
        print ('\n')
        print(player_ranks)
        

def CheckLambdaPreConditions(match_id):  
    result = False
    dynamo_access = DynamoAccess() 
    game_details = dynamo_access.GetGameDetails(match_id) 
    scorecard_link = game_details['score_card_url']  

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
    if CheckLambdaPreConditions(match_id):
        db_updater = DbUpdater(match_id)
        db_updater.UpdateRankingInDynamo() 
        db_updater.UpdatePointsInDynamo() 
        return 'dynamo updated'
    
    return 'scorecard not available yet'


if __name__ == "__main__": 
    handle({'match_id':'1234'},{}) 


#TODO 
''' 
setup git repo!! first, would hate to lose my work!!!!
tomorrow: setup proper dynamo access 
so we can make the calls from the interface 
implement the write calls first 
if time allows do the read calls too
'''