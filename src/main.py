import os
import json
import requests

class GitHubActivity():
    def __init__(self, filename="default"):
        self.filename = str(filename).lower() + ".json"

    def get_specific_data(self, username, sort, route=None):
        base_url = "https://api.github.com/users/"
        if route is None or route=="":
            url = f"{base_url}{username}"
        else:
            url = f"{base_url}{username}/{route}"
        querry_params = {
            "sort": "updated",
            "per_page": sort
        }
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
            
    def to_json(self, data, filename):
        with open(filename, mode="w", encoding="utf-8") as writefile:
            json.dump(data, writefile, indent=2)

if __name__ == "__main__":
    ga = GitHubActivity(filename="user_data")
    username = "SIDDHARTH-S-001"
    route = "repos"
    sort = 1
    pat_path = "/home/kinisi/Documents/personal/pat2.txt"
    # ga.get_specific_data(username=username, sort=sort, route=route)
    ga.load_credentials(pat_path=pat_path)


