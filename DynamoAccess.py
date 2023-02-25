from typing import List, Dict
import os,sys 
import boto3  
import simplejson as json
from decimal import Decimal 
from boto3.dynamodb.conditions import Key, Attr


from FantasyPointsCalculator_API.FantasyPointsCalculator.SquadGenerator.ListOfAllPlayers import AllPlayers
''' 
Responsible for handling all dynamo related calls  
'''

class DynamoAccess(object): 
    def __init__(self): 
        self.dynamodb = boto3.resource('dynamodb')   
        self.match_table_name = 'all_match_info'
        self.match_table = self.dynamodb.Table(self.match_table_name)   

        self.squad_table_name = 'selected_squads' 
        self.squad_table = self.dynamodb.Table(self.squad_table_name)

        ## frequently read values: 
        self.scorecard_details = None

    '''-------------------------- read calls --------------------------'''    

    def GetMatchSquad(self, match_id:str): 
        response = self.match_table.query( 
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
        response = self.match_table.query( 
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
        response = self.squad_table.scan(
                    FilterExpression=Attr("match_id").eq(match_id)
                    ) 
        json_list = json.loads(json.dumps(response["Items"], use_decimal=True))
        all_info = [] 
        for i in range(len(json_list)): 
            squad_selection = json_list[i]['squad_selection']
            user_name = json_list[i]['user_name'] 
            user_id = json_list[i]['user_id']
            user_info = {'user_id':user_id, 'user_name':user_name, 
                         'squad': squad_selection['selected_squad'], 
                         'captain': squad_selection['captain'],
                         'vice_captain': squad_selection['vice_captain']} 
            
            all_info.append(user_info) 
        
        return all_info

    
    '''-------------------------- write calls -------------------------- '''

    def UpdateAllPoints(self, records):   
        match_id = records['match_id']   
        update_expression=  "set fantasy_ranks=:fantasy_ranks, batting_points=:batting_points, bowling_points=:bowling_points, fielding_points=:fielding_points, summary_points=:summary_points, last_updated=:last_updated"

        try:
            response = self.match_table.update_item( 
                Key={'match_id': match_id}, 
                UpdateExpression= update_expression, 
                ExpressionAttributeValues={
                    ':fantasy_ranks': json.loads(json.dumps(records['fantasy_ranks']), parse_float=Decimal),
                    ':batting_points': json.loads(json.dumps(records['batting_points']), parse_float=Decimal),
                    ':bowling_points': json.loads(json.dumps(records['bowling_points']), parse_float=Decimal), 
                    ':fielding_points': json.loads(json.dumps(records['fielding_points']), parse_float=Decimal), 
                    ':summary_points': json.loads(json.dumps(records['summary_points']), parse_float=Decimal),  
                    ':last_updated': json.loads(json.dumps(records['last_updated']), parse_float=Decimal), 

                },
                ReturnValues="UPDATED_NEW"
            )   
            print (f'DynamoAccess::UpdateAllPoints successfully updated')
        except: 
            print (f'DynamoAccess::UpdateAllPoints FAILED to update items') 
        


if __name__ == "__main__":
    x=DynamoAccess() 
    print (x.GetMatchSquad('123'))