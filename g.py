import os
import subprocess
import random
import string
from datetime import datetime

filename = "random_commit_file.txt"

# Configuration: specify the exact date here
year = 2024
month = 6
day = 15

# Number of commits to make on that date (random between min and max)
min_commits = 1
max_commits = 5

def random_string(length=10):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def run_git_command(cmd, env=None):
    result = subprocess.run(cmd, shell=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(result.stderr.decode())
    return result

def main():
    # Initialize git repo if not already initialized
    if not os.path.exists(".git"):
        print("Initializing new git repository...")
        run_git_command("git init")

    commit_date = datetime(year, month, day, 12, 0, 0)  # Noon time to avoid timezone issues
    date_str = commit_date.strftime("%Y-%m-%d %H:%M:%S")

    commits_to_make = random.randint(min_commits, max_commits)
    print(f"Making {commits_to_make} commits on {date_str}")

    for commit_num in range(commits_to_make):
        # Append random content to the file
        with open(filename, "a") as f:
            f.write(f"{random_string(20)}\n")

        run_git_command(f"git add {filename}")

        # Set commit date environment variables
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = date_str
        env["GIT_COMMITTER_DATE"] = date_str

        commit_message = f"Random commit on {date_str} #{commit_num} - {random_string(8)}"
        run_git_command(f'git commit -m "{commit_message}"', env=env)

    print("Done making commits. Push to GitHub to update contribution graph.")

if __name__ == "__main__":
    main()
