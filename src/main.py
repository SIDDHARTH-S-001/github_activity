#!/usr/bin/python3
import os
import json
import requests
import argparse

class GitHubActivity():
    def __init__(self, filename="default"):
        self.filename = str(filename).lower() + ".json"
        self.github_url = "https://github.com/"
        self.base_url = "https://api.github.com/users/"
       
    def get_activity(self, username, n_recent):
        url = f"{self.base_url}{username}/events"
        querry_params = {"sort": "updated", "per_page":n_recent}
        event = requests.get(url=url, params=querry_params).json()
        print("----- Recent User Activity -----")
        for i in range(len(event)):
            event_id, action, createdAt, repo_name, public = event[i]["id"], event[i]["type"], event[i]["created_at"], \
                                                             event[i]["repo"]["name"], event[i]["public"]
            event_data = [event_id, action, createdAt, repo_name, public]
            self.format_output(event_data)
    
    def format_output(self, list):
        event_id, action, createdAt, repo_name, public = list
        repo_name = str(repo_name).split("/")[1]
        repo_url =  f"{self.github_url}{self.username}/{repo_name}"
        time , date = createdAt[12:-1], createdAt[:10]
        print(f"action: {action}")
        print(f"event id: {event_id}")
        print(f"performed at: {time} on {date}")
        print(f"repo name: {repo_name}")
        print(f"repo url: {repo_url}")
        print(f"visibility: {"public" if public else "private"}")
        print("--------------------------------")
    
    def process_cli(self):
        parser = argparse.ArgumentParser(description="GitHub activity Tracker")
        parser.add_argument("username", type=str, help="username of the git user")
        parser.add_argument("arg1", nargs=1, type=int, help="last 'n' activities of the user")
        args = parser.parse_args()
        self.username = args.username
        self.get_activity(args.username, args.arg1)

    def to_json(self, data, filename):
        with open(filename, mode="w", encoding="utf-8") as writefile:
            json.dump(data, writefile, indent=2)

if __name__ == "__main__":
    ga = GitHubActivity(filename="user_data")
    ga.process_cli()


