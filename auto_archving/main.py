import os
import json
from typing import List

from github import Github
import requests

from config import Config



g = Github(os.environ['GITHUB_TOKEN'])
repo = g.get_repo(os.environ['GITHUB_REPOSITORY']) 
commit = repo.get_commit(os.environ['GITHUB_SHA'])
token = os.environ['MY_TOKEN']
allClosedIssueNumber = os.environ['CLOSED_ISSUE_NUMBER']
allReopenIssueNumber = os.environ['REOPEN_ISSUE_NUMBER']
repositoryName = repo.name   
commitTitle = commit.commit.message
repositoryOwner = repo.owner.login 

config = Config(repositoryName,repositoryOwner,token)

print(f"Repository name: {repositoryName}")  
print(f"Commit title: {commitTitle}")
print(f'issue need to closed : {allClosedIssueNumber}')
# print(os.environ['GITHUB_TOKEN'])

class Issue():
    state = ""
    issueNumber = 0
    allIssues = []
    
    def __init__(
            self,issueNumber:int,
            state:str = "closed"
            ) -> None:
        self.state = state
        self.issueNumber = issueNumber
        self.isPreviouslyClosed = False
        self.notFound = False
        Issue.allIssues.append(self)
        
    def SetPreviouslyClosed(self) -> None:
        self.isPreviouslyClosed = True
        
    def SetNotFound(self) -> None:
        self.notFound = True
        Statistics.notFoundIssues.append(self.issueNumber)

class Statistics():
    previouslyClosedIssues = []
    newlyClosedIssues = []
    faildToClosedIssues = []
    notFoundIssues = []
    def FormatIssues(issueNumbers:List[int]) -> List[str]:
        def AddSharp(issueNumber:int) -> str:
            return f'#{issueNumber}'
        result = []
        for issueNumber in issueNumbers:
            result.append(AddSharp(issueNumber))
        return result
    
    def PrintStatistics():
        print(f'Statistics : ')
        print(f'{len(Statistics.previouslyClosedIssues)} issues already closed : {Statistics.FormatIssues(Statistics.previouslyClosedIssues)}')
        print(f'{len(Statistics.newlyClosedIssues)} issues closed successfully: {Statistics.FormatIssues(Statistics.newlyClosedIssues)}')
        print(f'{len(Statistics.faildToClosedIssues)} issues faild to closed : {Statistics.FormatIssues(Statistics.faildToClosedIssues)}')
        print(f'{len(Statistics.notFoundIssues)} issues not found : {Statistics.FormatIssues(Statistics.notFoundIssues)}')
        
        
def SplitIssueNumber(allClosedIssueNumber:str) -> list:
    return allClosedIssueNumber.split(",")
        
def ToJsonString(dict:dict) -> str:
    return json.dumps(dict)

def SetPatchBody(issue:Issue) -> str:
    body = {
        "state":issue.state
    }
    return ToJsonString(body)

def SetIssueAPIUrl(issue:Issue) -> str:
    url = f'{config.githubAPIUrl}/repos/' 
    url += f'{config.repositoryOwner}/'
    url += f'{config.repositoryName}/' 
    url += f'issues/{issue.issueNumber}'
    return url

def PrintFatchFaliedMessage(response:object,issue:Issue) -> None:
        separator = "-" * 30
        print(f'fetch issue#{issue.issueNumber} failed !!!')
        print(f'error message : \n{separator}')
        print(f'issue api url:{response.url}')
        print(f'issue http url:{ToissueHtmlUrl(response.url)}')
        print(f'http code:{response.status_code}')
        print(f'response content:{response.text}')
        print(f'{separator}\n\n')
        
def ToissueHtmlUrl(issueAPIUrl:str) -> str:
        issueHtmlUrl = issueAPIUrl.replace("api.","") 
        issueHtmlUrl = issueHtmlUrl.replace("/repos","") 
        return issueHtmlUrl
    
def IsClosedIssue(response:object,issue:Issue) -> bool:
        try:
            return response.json()["state"] == "closed"
        except KeyError:
            PrintFatchFaliedMessage(response,issue)
            return False

def CloseIssues(issue:Issue) -> None:
    def Patch(issueAPIUrl:str,header:dict,body:str) -> None:
        response = requests.patch(issueAPIUrl,headers=header,data=body)
        if IsClosedIssue(response,issue):
            # print(f'issue API url : {response.url}')
            print(f'issue HTML url : {ToissueHtmlUrl(response.url)}')
            print(f'close issue#{issue.issueNumber} successfully\n')
            Statistics.newlyClosedIssues.append(issue.issueNumber)
        else:
            Statistics.faildToClosedIssues.append(issue.issueNumber)
        
    if issue.isPreviouslyClosed or issue.notFound:
        return
    issueAPIUrl = SetIssueAPIUrl(issue)
    header = config.header
    body = SetPatchBody(issue)
    Patch(issueAPIUrl,header,body)
    
def GetIssue(issue:Issue) -> None:
    def Get(issueAPIUrl:str,header:dict):
        response = requests.get(issueAPIUrl,headers=header)
        if response.status_code == 404:
            print(f'issue#{issue.issueNumber} not found !\n')
            issue.SetNotFound()
            return
        
        if IsClosedIssue(response,issue):
            print(f'issue HTML url : {ToissueHtmlUrl(response.url)}')
            print(f'issue#{issue.issueNumber} is already closed\n')
            Statistics.previouslyClosedIssues.append(issue.issueNumber)
            issue.SetPreviouslyClosed()
    
    issueAPIUrl = SetIssueAPIUrl(issue)
    header = config.header
    Get(issueAPIUrl,header)
    

if __name__ == "__main__":
    allClosedIssueNumber = SplitIssueNumber(allClosedIssueNumber)
    print()
    for issueNumber in allClosedIssueNumber:
        issue = Issue(issueNumber)
        GetIssue(issue)
        CloseIssues(issue)
    Statistics.PrintStatistics()

    
    
    


    
    
    
        
        
        
        

    
    
    