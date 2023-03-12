import requests
from bs4 import BeautifulSoup

class MatchResultFinder(object): 
    def __init__(self, scorecard_link, team1, team2): 
        self.scorecard_link = scorecard_link  
        self.team1 = team1 
        self.team2 = team2
    
    def __ExtractPage__(self): 
        # send an HTTP GET request to the URL and get the page content
        page = requests.get(self.scorecard_link)
        html_content = page.content

        # create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(html_content, "lxml")
        
        # find the match result element
        won_by = list(soup.find_all(lambda tag: tag.name == 'span' and ('won by' in tag.text)))    
        drawn = list(soup.find_all(lambda tag: tag.name == 'span' and ('Match drawn' in tag.text))) 
        tied = list(soup.find_all(lambda tag: tag.name == 'span' and ('Match tied' in tag.text)))

        match_results = won_by + drawn + tied
        return match_results 
    
    def FindMatchResult(self):
        match_results = self.__ExtractPage__()

        if len(match_results) == 0: 
            return None 
        
        last_result = str(match_results[-1])
        ''' check if match is drawn (most likely that's the last result found on that page) 
            this may change in the future ''' 
        
        if 'drawn' in last_result or 'tied' in last_result: 
            return 'draw'  
        elif self.team1.lower() in last_result.lower(): 
            return 'team1' 
        elif self.team2.lower() in last_result.lower(): 
            return 'team2'  
        else: 
            return 'unknown'

