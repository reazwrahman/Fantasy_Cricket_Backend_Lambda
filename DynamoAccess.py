from typing import List, Dict
import os,sys 
import boto3  
import json 
from decimal import Decimal


from FantasyPointsCalculator_API.FantasyPointsCalculator.SquadGenerator.ListOfAllPlayers import AllPlayers
''' 
Responsible for handling all dynamo related calls  
'''

class DynamoAccess(object): 
    def __init__(self): 
        self.dynamodb = boto3.resource('dynamodb')   
        self.table_name = 'all_match_info'
        self.table = self.dynamodb.Table(self.table_name) 

    '''-------------------------- read calls --------------------------'''    

    def GetSquad(self, match_id:str) -> List[Dict] : 
        #TODO 

        '''  
        reads the match details from dynamo 
        and returns the squad for a given match
        ''' 
        '''
        # use the existing squad reader for now 
        # format 
        { 1: playername: kane williamson batter, 2: ... }

        } 
        placeholder code below
        '''  
        url: str = 'https://www.espncricinfo.com/series/australia-in-india-2022-23-1348637/india-vs-australia-2nd-test-1348653/match-squads'
        squad_generator: AllPlayers = AllPlayers(url)  
        raw_squad = squad_generator.GetFullSquad()

        full_squad: Dict = {} 
        i=1 
        for each in raw_squad: 
            full_squad[i] = each
            i+=1 
        
        return full_squad  
    


    def GetGameDetails(self, match_id): 
        ''' 
            reads dynamo and returns game_details 
        ''' 
        game_details:Dict = {'match_id': '1234', 
        'game_title': 'nz v pakistan', 
        'score_card_url': 'https://www.espncricinfo.com/series/australia-in-india-2022-23-1348637/india-vs-australia-2nd-test-1348653/full-scorecard', 
        'points_per_run': 1, 
        'points_per_wicket':20 
        }

        return game_details

    def GetSelectedSquads(self, match_id): 
        ''' 
            return a list of all users with their squads 
            [{user_id:1, user_name:maxwell, selected_squad:[1,15,16,19...]}]
        '''  
        user1 = {'user_id':5, 'user_name':'maxwell', 'squad':[1,15,6,9,3,20,5,9],'captain':20, 'vice_captain':9 } 
        user2 = {'user_id':1, 'user_name':'warner', 'squad':[19,17,7,8,9,4,3,27],'captain':19, 'vice_captain': 3} 
        user3 = {'user_id':4, 'user_name':'renshaw', 'squad':[15,14,13,11,19,23,2],'captain': 15, 'vice_captain':2}
        info = [user1, user2, user3]
        return info

    
    '''-------------------------- write calls -------------------------- '''

    def UpdateAllPoints(self, records):    
        item = {'match_id': records['match_id'],   
                'fantasy_ranks': records['fantasy_ranks'],
                'batting_points': records['batting_points'], 
                'bowling_points': records['bowling_points'], 
                'fielding_points': records['fielding_points'], 
                'summary_points' : records['summary_points']          
                } 
        item = json.loads(json.dumps(item), parse_float=Decimal)  
        response = self.table.put_item(Item = item) 
        print(f'DynamoAccess::UpdateAllPoints response = {response}') 


if __name__ == "__main__":
    x=DynamoAccess() 
    print (x.GetSquad('123'))