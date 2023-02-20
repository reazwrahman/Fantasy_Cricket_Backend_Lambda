from typing import Dict, List

from DynamoAccess import DynamoAccess 
from FantasyPointsCalculator_API.FantasyPointsCalculatorIF import FantasyPointsForFullSquad

''' 
creates a dictionary for all the players 
with all the necessary fantasy points
'''

class PlayerStatsTracker(object): 
    def __init__(self, match_id): 

        self.match_id = match_id
        self.dynamo_access = DynamoAccess() 
        self.__CallFantasyApi__()

        self.batting_points = self.__MapBattingPoints__()  
        self.bowling_points = self.__MapBowlingPoints__()  
        self.fielding_points = self.__MapFieldingPoints__()  
        self.summary_points = self.__MapSummaryPoints__()  
  

    def __CallFantasyApi__(self):   
        self.scorecard_details = self.dynamo_access.GetScorecardInfo(self.match_id)
        self.game_squad = self.dynamo_access.GetMatchSquad(self.match_id) 
        self.game_squad_reversed = {}
        player_names = []

        for each in self.game_squad:   
            player_id = each
            player_name = self.game_squad[each]['Name']
            self.game_squad_reversed[player_name] = player_id
            player_names.append(player_name)

        game_info = {'score_card_url': self.scorecard_details['scorecard_link'],  
                    'squad': player_names,
                    'points_per_run': 1, 
                    'points_per_wicket': 20
                    } 
        self.fantasy_api = FantasyPointsForFullSquad(game_info)


    def __MapIdToRecord__(self, records: List[Dict]) -> Dict:      
        mapped_records= {}

        ## insert player id into each record   
        for i in range (len(records)):  
            each_record = records[i]
            player_name = each_record['Name'] 

            if player_name in self.game_squad_reversed:
                player_id = self.game_squad_reversed[player_name] 
                mapped_records[player_id] = each_record

        return mapped_records 

    def __MapBattingPoints__(self) -> List[Dict]: 
        ''' maps player id to batting points''' 
        batting_points = self.fantasy_api.GetBattingDf() 
        batting_points = batting_points.to_dict('records') 

        return self.__MapIdToRecord__(batting_points) 

    
    def __MapBowlingPoints__(self) -> List[Dict]: 
        '''maps player id to bowling point'''  
        bowling_points = self.fantasy_api.GetBowlingDf()    
        bowling_points = bowling_points.to_dict('records') 
        
        return self.__MapIdToRecord__(bowling_points) 


    def __MapFieldingPoints__(self) -> List[Dict]: 
        '''maps player id to fielding point'''  
        fielding_points = self.fantasy_api.GetFieldingDf()    
        fielding_points = fielding_points.to_dict('records') 
        
        return self.__MapIdToRecord__(fielding_points)  

    def __MapSummaryPoints__(self) -> List[Dict]: 
        '''maps player id to summary points'''   
        summary_points = self.fantasy_api.GetFullSquadDf()   
        summary_points = summary_points.to_dict('records') 

        return self.__MapIdToRecord__(summary_points)   
   

    def GetBattingPoints(self): 
        return self.batting_points 

    def GetBowlingPoints(self): 
        return self.bowling_points  
    
    def GetFieldingPoints(self): 
        return self.fielding_points  
    
    def GetSummaryPoints(self): 
        return self.summary_points  
    


if __name__ == "__main__": 
    x = PlayerStatsTracker('1234')   
    #print(x.game_squad)
    #print (x.game_squad_reversed) 
    #print(x.GetBattingPoints()) 
    #print(x.GetBowlingPoints()) 
    #print(x.GetFieldingPoints()) 
    print(x.GetSummaryPoints())
    
    