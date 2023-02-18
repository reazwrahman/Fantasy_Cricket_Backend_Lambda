from typing import List, Dict
import os,sys 
import boto3  
import simplejson as json
from decimal import Decimal 
from boto3.dynamodb.conditions import Key


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
        response = self.table.query( 
                KeyConditionExpression=Key('match_id').eq(match_id),  
                ProjectionExpression = 'game_details')   
        
        json_list = json.loads(json.dumps(response["Items"], use_decimal=True))
        self.game_details = json_list[0]['game_details']
        print (self.game_details)
        return self.game_details

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
        match_id = records['match_id']   
        update_expression=  "set fantasy_ranks=:fantasy_ranks, batting_points=:batting_points, bowling_points=:bowling_points, fielding_points=:fielding_points, summary_points=:summary_points"

        try:
            response = self.table.update_item( 
                Key={'match_id': match_id}, 
                UpdateExpression= update_expression, 
                ExpressionAttributeValues={
                    ':fantasy_ranks': json.loads(json.dumps(records['fantasy_ranks']), parse_float=Decimal),
                    ':batting_points': json.loads(json.dumps(records['batting_points']), parse_float=Decimal),
                    ':bowling_points': json.loads(json.dumps(records['bowling_points']), parse_float=Decimal), 
                    ':fielding_points': json.loads(json.dumps(records['fielding_points']), parse_float=Decimal), 
                    ':summary_points': json.loads(json.dumps(records['summary_points']), parse_float=Decimal),   
                },
                ReturnValues="UPDATED_NEW"
            )   
            print (f'DynamoAccess::UpdateAllPoints successfully updated')
        except: 
            print (f'DynamoAccess::UpdateAllPoints FAILED to update items')


if __name__ == "__main__":
    x=DynamoAccess() 
    print (x.GetSquad('123'))