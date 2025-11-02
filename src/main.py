import os
import json
import requests
import argparse

class GitHubActivity():
    def __init__(self, filename="default"):
        self.filename = str(filename).lower() + ".json"
        self.github_url = "https://github.com/"
        self.base_url = "https://api.github.com/users/"

    def get_specific_data(self, username, sort, route=None):
        if route is None or route=="":
            url = f"{self.base_url}{username}"
        else:
            url = f"{self.base_url}{username}/{route}"
        querry_params = {"sort": "updated", "per_page": sort}
        print(url)
        user_data = requests.get(url=url, params=querry_params) # 'user_data' is the response and it is already a python dictionary.
        self.to_json(user_data.json(), self.filename)
        print(user_data.status_code)
        
    def load_credentials(self, pat_path):
        if os.path.exists(pat_path):
            with open(pat_path, mode="r") as read_file:
                self.pat = read_file.read()
                print(self.pat)
        else:
            print(f"The specified path {pat_path} doesn't exist")
        
    def get_activity(self, username, n_recent):
        url = f"{self.base_url}{username}/events"
        querry_params = {"sort": "updated", "per_page":n_recent}
        event = requests.get(url=url, params=querry_params).json()
        action, createdAt, public = event[0]["type"], event[0]["created_at"], event[0]["public"]
        repo_name = str(event[0]["repo"]["name"]).split("/")[1]
        repo_url =  f"{self.github_url}{username}/{repo_name}"
        event_data = [action, createdAt, repo_name, repo_url, public]
        self.format_output(event_data)
        return event_data
    
    def format_output(self, list):
        action, createdAt, repo_name, repo_url, public = list
        print("----- User Activity -----")
        print(f"action: {action}")
        print(f"performaed at: {createdAt}")
        print(f"repo name: {repo_name}")
        print(f"repo url: {repo_url}")
        print(f"visibility: {"public" if public else "private"}")
        print("-------------------------")
        # print(action, createdAt, repo_name, repo_url, public)
    
    def process_cli(self):
        parser = argparse.ArgumentParser(description="GitHub activity Tracker")
        parser.add_argument("username", type=str, help="username of the git user")
        parser.add_argument("arg1", nargs=1, type=int, help="last 'n' activities of the user")
        args = parser.parse_args()
        self.get_activity(args.username, args.arg1)

    def to_json(self, data, filename):
        with open(filename, mode="w", encoding="utf-8") as writefile:
            json.dump(data, writefile, indent=2)

if __name__ == "__main__":
    ga = GitHubActivity(filename="user_data")
    username = "SIDDHARTH-S-001"
    route = "events"
    sort = 1
    pat_path = "/home/kinisi/Documents/personal/pat2.txt"
    # ga.get_specific_data(username=username, sort=sort, route=route)
    # ga.load_credentials(pat_path=pat_path)
    ga.process_cli()


