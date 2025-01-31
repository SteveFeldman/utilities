import requests
import concurrent.futures
import re
import os
from datetime import datetime

# GitHub Personal Access Token (Replace with your token)
GITHUB_TOKEN = "Enter Your Token Here"
# List of PR URLs
PR_URLS = [
"https://github.com/XYZ/pull/1",
"https://github.com/XYZ/Pull/2"
]

# :white_check_mark: GitHub API Headers
HEADERS = {
  "Authorization": f"token {GITHUB_TOKEN}",
  "Accept": "application/vnd.github.v3+json"
}
def extract_repo_details(pr_url):
  """Extracts owner, repo, and PR number from a GitHub PR URL."""
  match = re.match(r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)", pr_url)
  if match:
    return {"owner": match.group(1), "repo": match.group(2), "pr": match.group(3)}
  return None
def seconds_to_hours(seconds):
  """Converts seconds to hours, rounded to 2 decimal places."""
  return round(seconds / 3600, 2) if seconds is not None else None
def fetch_pr_details(pr_url):
  """Fetch PR details, reviews, and commits."""
  pr_data = extract_repo_details(pr_url)
  if not pr_data:
    return {"url": pr_url, "error": "Invalid PR URL format"}
  owner, repo, pr_number = pr_data["owner"], pr_data["repo"], pr_data["pr"]
  # :white_check_mark: Step 1: Fetch PR metadata
  pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
  response = requests.get(pr_url, headers=HEADERS)
  if response.status_code != 200:
    return {"url": pr_url, "error": response.status_code}
  pr_info = response.json()
  # :white_check_mark: Step 2: Fetch Reviews
  reviews_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
  reviews_response = requests.get(reviews_url, headers=HEADERS)
  reviews = reviews_response.json() if reviews_response.status_code == 200 else []
  approvals = sum(1 for r in reviews if r["state"] == "APPROVED")
  reviewers = list(set(r["user"]["login"] for r in reviews if r.get("user")))
  # :white_check_mark: Step 3: Fetch Commits
  commits_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/commits"
  commits_response = requests.get(commits_url, headers=HEADERS)
  commits = commits_response.json() if commits_response.status_code == 200 else []
  commit_authors = list(set(c["commit"]["author"]["name"] for c in commits if c.get("commit")))
  num_commits = len(commits)
  # :white_check_mark: Calculate time-based metrics
  created_at = datetime.strptime(pr_info["created_at"], "%Y-%m-%dT%H:%M:%SZ")
  merged_at = datetime.strptime(pr_info["merged_at"], "%Y-%m-%dT%H:%M:%SZ") if pr_info["merged_at"] else None
  closed_at = datetime.strptime(pr_info["closed_at"], "%Y-%m-%dT%H:%M:%SZ") if pr_info["closed_at"] else None
  first_commit_timestamp = datetime.strptime(commits[0]["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ") if commits else None
  first_review_timestamp = datetime.strptime(reviews[0]["submitted_at"], "%Y-%m-%dT%H:%M:%SZ") if reviews else None
  time_to_open_pr = seconds_to_hours((created_at - first_commit_timestamp).total_seconds()) if first_commit_timestamp else None
  time_to_first_review = seconds_to_hours((first_review_timestamp - created_at).total_seconds()) if first_review_timestamp else None
  time_to_merge = seconds_to_hours((merged_at - created_at).total_seconds()) if merged_at else None
  time_pr_open_before_close = seconds_to_hours((closed_at - created_at).total_seconds()) if closed_at else None
  # :white_check_mark: Return the collected metrics
  return {
    "url": pr_url,
    "id": pr_info["id"],
    "pr_number": pr_info["number"],
    "title": pr_info["title"],
    "created_at": pr_info["created_at"],
    "updated_at": pr_info["updated_at"],
    "closed_at": pr_info["closed_at"],
    "merged_at": pr_info["merged_at"],
    "author": pr_info["user"]["login"],
    "files_changed": pr_info["changed_files"],
    "lines_added": pr_info["additions"],
    "lines_removed": pr_info["deletions"],
    "diff_size": pr_info["additions"] + pr_info["deletions"],
    "requested_reviewers": [r["login"] for r in pr_info.get("requested_reviewers", [])],
    "reviewers": reviewers,
    "approvals": approvals,
    "review_comments": pr_info["review_comments"],
    "general_comments": pr_info["comments"],
    "num_commits": num_commits,
    "commit_authors": commit_authors,
    "time_to_open_pr (hours)": time_to_open_pr,
    "time_to_first_review (hours)": time_to_first_review,
    "time_to_merge (hours)": time_to_merge,
    "time_pr_open_before_close (hours)": time_pr_open_before_close
  }
# :white_check_mark: Fetch multiple PRs in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
  results = list(executor.map(fetch_pr_details, PR_URLS))
# :white_check_mark: Print results
for pr in results:
  if "error" in pr:
    print(f":x: Failed to fetch PR from {pr['url']} (Error: {pr['error']})")
  else:
    print(f":white_check_mark: PR #{pr['pr_number']} ({pr['title']}) - {pr['author']} - {pr['created_at']}")
    print(f"  Files Changed: {pr['files_changed']}, Lines Added: {pr['lines_added']}, Lines Removed: {pr['lines_removed']}, Total Diff: {pr['diff_size']}")
    print(f"  Approvals: {pr['approvals']}, Review Comments: {pr['review_comments']}, General Comments: {pr['general_comments']}")
    print(f"  Commits: {pr['num_commits']}, Authors: {', '.join(pr['commit_authors'])}")
    print(f"  Time to Open PR: {pr['time_to_open_pr (hours)']} hours")
    print(f"  Time to First Review: {pr['time_to_first_review (hours)']} hours")
    print(f"  Time to Merge: {pr['time_to_merge (hours)']} hours")
    print(f"  Time PR Open Before Close: {pr['time_pr_open_before_close (hours)']} hours")
    print("------------------------------------------------------------------")
