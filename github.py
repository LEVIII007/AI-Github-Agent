import os
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document



load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

def FETCH_GETHUB(owner, repo, endpoint):
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
    headers = {
    "Authorization": f"token {github_token}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data[0]
    else:
        print(f"Error: {response.status_code}")
        data = None
        return data

def load_issues(issues):
    docs = []
    for entry in issues:
        metadata = {
            "author": entry["user"]["login"],
            "comments": entry["comments"],
            "body": entry["body"],
            "created_at": entry["created_at"],
            "labels": entry["labels"]
        }
        data = entry["title"]
        if entry["body"]:
            data += entry["body"]
        doc = Document(page_content = data, metadata = metadata)
        docs.append(doc)

    return docs

def fetch_issues(owner, repo):
    endpoint = "issues"
    data = FETCH_GETHUB(owner, repo, endpoint)
    docs = load_issues(data)
    return docs

# owner = "techwithtim"
# repo = "Flask-Web-App-Tutorial"
# endpoint = "issues"
# data = FETCH_GETHUB(owner, repo, endpoint)
