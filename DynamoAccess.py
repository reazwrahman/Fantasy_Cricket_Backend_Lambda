from typing import List, Dict
import os,sys 


from FantasyPointsCalculator_API.FantasyPointsCalculator.SquadGenerator.ListOfAllPlayers import AllPlayers
''' 
Responsible for handling all dynamo related calls  
'''

class DynamoAccess(object): 
    def __init__(self): 
        #TODO 
        pass 

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
        url: str = 'https://www.espncricinfo.com/series/england-tour-of-new-zealand-2022-23-1322349/new-zealand-vs-england-1st-test-1322355/match-squads'
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
        'score_card_url': 'https://www.espncricinfo.com/series/england-tour-of-new-zealand-2022-23-1322349/new-zealand-vs-england-1st-test-1322355/full-scorecard', 
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

    def UpdateBattingPoints(self, records:Dict): 
        ''' update dynamo with batting points'''
        pass 

    def UpdateBowlingPoints(self, records:Dict): 
        ''' update dynamo with bowling points'''
        pass 

    def UpdateFieldingPoints(self, records:Dict): 
        ''' update dynamo with fielding points'''
        pass  

    def UpdateSummaryPoints(self, records:Dict): 
        ''' update dynamo with summary points'''
        pass 

    def UpdateUserRanking(self, ranks:List[List]): 
        ''' 
            update player ranking in dynamo
        '''
        pass


if __name__ == "__main__":
    x=DynamoAccess() 
    print (x.GetSquad('123'))