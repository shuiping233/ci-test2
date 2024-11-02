

class Config():
    repositoryName = ""
    repositoryOwner = ""
    token = ""
    githubAPIUrl = "https://api.github.com"
    header = {
        "accept":"application/vnd.github+json",
        "Content-Type":"application/json"
    }
    
    def __init__(self,repositoryName:str,repositoryOwner:str,token:str) -> None:
        self.repositoryName = repositoryName
        self.repositoryOwner = repositoryOwner
        self.token = token 
        self.header["Authorization"] = f"token {self.token}"
    

    
            
    
        
        
