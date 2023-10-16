import json
import time

import requests
import ruamel.yaml as yaml
from github import Github


def open_yaml(file_url):
    try:
        if file_url.startswith("http"):
            # It is a URL
            pointer = requests.get(file_url)
            return yaml.safe_load(pointer.content.decode('utf-8'))
    except:
        return "Exception"
    else:
        # It is a file
        try:
            file = open(file_url, "r")
            return yaml.safe_load(file.read())
        except:
            return "Wrong file path"
        

def github_rate(user, token, security_margin=2):
    """
    Check the remaining GitHub API calls for the authenticated user and wait if necessary.
    """
    try:
        # Get the current rate limit status
        response = requests.get('https://api.github.com/rate_limit', auth=(user, token))
        resonse_text = response.text
        response.raise_for_status()  # Raise an exception if the request fails
        rate_limit_data = response.json()

        # Extract rate limit information
        resources = rate_limit_data["resources"]["core"]
        remaining = resources["remaining"]  # Remaining API calls for the current window
        reset_time = resources["reset"]  # Timestamp when the rate limit resets
        used_calls = resources["used"]  # Number of API calls made in the current window

        # Calculate the time until the rate limit resets
        time_until_reset = reset_time - time.time()

        # Check if we're close to the rate limit
        if remaining < security_margin:
            # Calculate the pause time to wait until the rate limit resets
            pause_time = max(0, time_until_reset + 1)  # Add 1 second as a buffer
            print(f"Waiting for {pause_time:.2f} seconds until rate limit resets...")
            time.sleep(pause_time)

        # Print rate limit information
        print(f"Remaining API calls: {remaining}")
        print(f"Time until rate limit reset: {time_until_reset:.2f} seconds")
        print(f"Total API calls made in this window: {used_calls}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def get_credentials(credentials_file):
    """
    Read and load credentials from a JSON file.
    """
    try:
        with open(credentials_file, "r") as cred_file:
            credentials_dict = json.load(cred_file)
            return credentials_dict
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return None


def open_json(fileUrl):
    import json

    import requests
    if fileUrl[0:4] == "http":
        # es URL
        try:
            pointer = requests.get(fileUrl)
            return json.loads(pointer.content.decode('utf-8'))
        except:
            return None

    else:
        # es file
        try:
            file = open(fileUrl, "r")
            return json.loads(file.read())
        except:
            return None


def github_push_from_variable(contentVariable, repoName, fileTargetPath, message, globalUser, token):
    """
    Push content to a GitHub repository.
    """
    g = Github(token)
    repo = g.get_organization(globalUser).get_repo(repoName)
    try:
        file = repo.get_contents("/" + fileTargetPath)
        update = True
    except:
        update = False
    if update:
        repo.update_file(fileTargetPath, message, contentVariable, file.sha)
    else:
        repo.create_file(fileTargetPath, message, contentVariable, "master")
