from DynamoAccess import DynamoAccess 
from FantasyPointsCalculator_API.MatchResultFinder import MatchResultFinder

class Ranker(object): 
    def __init__(self, match_id, summary_points:dict, match_result:str):
        self.match_id = match_id  
        self.summary_points = summary_points  
        self.match_result = match_result

        self.dynamo_access = DynamoAccess()  


    def CalculatePointsForEachUser(self, user_info):
        selected_squad = user_info['squad']   
        captain = user_info['captain'] 
        vice_captain = user_info['vice_captain'] 
        result_prediction = user_info['result_prediction']

        total_points = 0 
        
        for each_player in selected_squad:  
            if str(each_player) in self.summary_points:   
                total_points += self.summary_points[str(each_player)]['Total'] 
        
        ## apply cap_vc points 
        if captain in self.summary_points: 
            total_points += self.summary_points[captain]['Total']  # 2x boost
        if vice_captain in self.summary_points: 
            total_points += (self.summary_points[vice_captain]['Total']/2) # 1.5x boost  
        
        ## apply match_prediction_points 
        if self.match_result != None and self.match_result != 'unknown': 
            if result_prediction == self.match_result:
                total_points += 100

        return [total_points, user_info['user_name'], total_points, user_info['user_id']] 
     
        
    def RankUsers(self): 
        all_users = self.dynamo_access.GetSelectedSquads(self.match_id)
        ranking = [] 
        for each_user_data in all_users: 
            points = self.CalculatePointsForEachUser(each_user_data) 
            ranking.append(points) 

        ranking.sort(reverse=True) 
        for i in range (len(ranking)):  
            # get rid of total points from the front
            ranking[i][0] = i+1
        
        return ranking 

if __name__ == "__main__":  
    from PlayerStatsTracker import PlayerStatsTracker 
    stat = PlayerStatsTracker('1234') 
    summary = stat.GetSummaryPoints()
    x = Ranker('1234', summary) 
    print(x.RankUsers())

        

