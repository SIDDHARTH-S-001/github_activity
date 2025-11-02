#!/usr/bin/python3
import os
import json
import requests
import argparse
import datetime

class GitHubActivity():
    def __init__(self, filename="default"):
        self.filename = str(filename).lower() + ".json"
        self.github_url = "https://github.com/"
        self.base_url = "https://api.github.com/users/"
        self.current_data = []
       
    def get_activity(self, username, n_recent, log=False):
        self.memory()
        url = f"{self.base_url}{username}/events"
        querry_params = {"sort": "updated", "per_page":n_recent}
        event = requests.get(url=url, params=querry_params).json()
        current_date_time = self.process_datetime()
        data = []
        print("----- Recent User Activity -----")
        for i in range(len(event)):
            event_id, action, createdAt, repo_name, public = event[i]["id"], event[i]["type"], event[i]["created_at"], event[i]["repo"]["name"], event[i]["public"]
            owner, repo_name = str(repo_name).split("/")
            repo_url =  f"{self.github_url}{owner}/{repo_name}"
            time , date = createdAt[12:-1], createdAt[:10]
            create_time_date = str(time) + "/" + str(date) 
            event_data = {"event_id": event_id, "action": action, "create_at": create_time_date, "repo_name": repo_name, "repo_url": repo_url, "visibility": public}
            data.append(event_data)
            self.format_output(event_data)
        self.current_data.append([current_date_time, data])
        self.to_json(self.current_data, self.filename); print("logging") if log else None
    
    def format_output(self, event_data):       
        print(f"action: {event_data["action"]}")
        print(f"event id: {event_data["event_id"]}")
        print(f"performed at: {event_data["create_at"]}")
        print(f"repo name: {event_data["repo_name"]}")
        print(f"repo url: {event_data["repo_url"]}")
        print(f"visibility: {"public" if event_data["visibility"] else "private"}")
        print("--------------------------------")

    def memory(self):
        if os.path.exists(self.filename):
            with open(self.filename, mode="r", encoding="utf-8") as read_file:
                self.current_data = json.load(read_file)      
                return self.current_data
        else:
            self.to_json(self.filename)
            self.memory()

    def process_datetime(self):
        date_time = datetime.datetime.now()
        date = date_time.strftime("%x")
        time = date_time.strftime("%X")
        date_time = str(time) + " - "+ str(date)
        return date_time
    
    def process_cli(self):
        parser = argparse.ArgumentParser(description="GitHub activity Tracker")
        parser.add_argument("username", type=str, help="username of the git user")
        parser.add_argument("n_recent", type=int, help="last 'n' activities of the user")
        parser.add_argument("-l", "--log", action="store_true", help="Logs output into json file if set to 'True'")
        args = parser.parse_args()
        self.username = args.username
        self.get_activity(args.username, args.n_recent, args.log)

    def to_json(self, data, filename):
        with open(filename, mode="w", encoding="utf-8") as writefile:
            json.dump(data, writefile, indent=2)

if __name__ == "__main__":
    ga = GitHubActivity(filename="user_data")
    ga.process_cli()


