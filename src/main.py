import os
import json
import requests

class GitHubActivity():
    def __init__(self, filename="default"):
        self.filename = str(filename).lower() + ".json"

    def get_user_data(self, username, route=None):
        base_url = "https://api.github.com/users/"
        if route is None or route=="":
            url = f"{base_url}{username}"
        else:
            url = f"{base_url}{username}/{route}"
        user_data = requests.get(url=url) # 'user_data' is the response and it is already a python dictionary.
        print(url)
        self.to_json(user_data.json(), self.filename)
        print(user_data.status_code)

    def to_json(self, data, filename):
        with open(filename, mode="w", encoding="utf-8") as writefile:
            json.dump(data, writefile, indent=2)

if __name__ == "__main__":
    ga = GitHubActivity(filename="user_data")
    username = "SIDDHARTH-S-001"
    route=""
    ga.get_user_data(username=username, route=route)

