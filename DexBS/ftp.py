


def del_git_file(path):
    import requests
    # Set up authentication and repository details
    USERNAME = 'TheHackerClown'
    REPO_NAME = 'DexBS_Asset_Library'
    ACCESS_TOKEN = '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'
    FILE_GITHUB_PATH = (path.split('/'))[-1]  # GitHub API path of the file

    # Prepare headers with authentication token
    headers = {
        'Authorization': f'token {ACCESS_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Make GET request to get information about the file
    response = requests.get(
        f'https://api.github.com/repos/{USERNAME}/{REPO_NAME}/contents/{FILE_GITHUB_PATH}',
        headers=headers
    )

    # Check if the file exists
    if response.status_code == 200:
        # Extract the SHA hash of the file
        file_sha = response.json()['sha']

        # Prepare request payload
        payload = {
            'message': f'Delete {FILE_GITHUB_PATH}',
            'sha': file_sha,
        }

        # Make DELETE request to delete file
        response = requests.delete(
            f'https://api.github.com/repos/{USERNAME}/{REPO_NAME}/contents/{FILE_GITHUB_PATH}',
            headers=headers,
            json=payload
        )

        # Check if the deletion was successful
        if response.status_code == 200:
            return "Done"
        else:
            return 'Not Done'
    else:
        return 'Not Done'
    
print(del_git_file('https://raw.githubusercontent.com/TheHackerClown/DexBS_Asset_Library/main/favicon.png'))