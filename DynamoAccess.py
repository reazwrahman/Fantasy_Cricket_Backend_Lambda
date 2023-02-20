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

        ## frequently read values: 
        self.scorecard_details = None

    '''-------------------------- read calls --------------------------'''    

    def GetMatchSquad(self, match_id:str) -> List[Dict] : 
        response = self.table.query( 
                KeyConditionExpression=Key('match_id').eq(match_id),  
                ProjectionExpression = 'match_squad')   
        
        json_list = json.loads(json.dumps(response["Items"], use_decimal=True))

        if len(json_list) < 1: 
            raise ValueError("NO ITEM FOUND FOR THE GIVEN MATCH ID, CHECK THE ID OR CHECK DATABASE")
        else:  
            return json_list[0]['match_squad']
    

    def ReadScorecardInfo(self, match_id): 
        ''' 
            reads dynamo and returns game_details 
        ''' 
        response = self.table.query( 
                KeyConditionExpression=Key('match_id').eq(match_id),  
                ProjectionExpression = 'scorecard_details')   
        
        json_list = json.loads(json.dumps(response["Items"], use_decimal=True))

        if len(json_list) < 1: 
            raise ValueError("NO ITEM FOUND FOR THE GIVEN MATCH ID, CHECK THE ID OR CHECK DATABASE")
        else:  
            self.scorecard_details = json_list[0]['scorecard_details']


    def GetScorecardInfo(self, match_id): 
        if not self.scorecard_details: 
            self.ReadScorecardInfo(match_id) 
        
        return self.scorecard_details

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
    print (x.GetMatchSquad('123'))