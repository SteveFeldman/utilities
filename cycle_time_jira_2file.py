from collections import defaultdict
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth

# JIRA Cloud instance URL and endpoint
JIRA_URL = "https://somesite.atlassian.net"
SEARCH_ENDPOINT = "/rest/api/3/search"

# Your JIRA API credentials
EMAIL = "email@site.com"
API_TOKEN = "Enter your API token here"
# JQL to filter issues
JQL_QUERY = (
    "issueKey in (XXX-1234)"
)
# File to save the output
OUTPUT_FILE = "transitions.txt"
REPORT_FILE = "report.txt"

# Transitions to analyze
ANALYZED_TRANSITIONS = [
    "From: Open To: In Development",
    "From: In Development To: Code Review",
    "From: Code Review To: Ready for Test",
    "From: Ready for Test To: Test",
    "From: Test To: PO Approval",
    "From: PO Approval To: QA Branch",
    "From: QA Branch To: Done"
]


def fetch_all_jira_data():
    headers = {"Accept": "application/json"}
    auth = HTTPBasicAuth(EMAIL, API_TOKEN)

    response = requests.get(
        JIRA_URL + SEARCH_ENDPOINT,
        headers=headers,
        params={
            "jql": JQL_QUERY,
            "fields": "summary,customfield_11503,resolutiondate",
            "expand": "changelog",
        },
        auth=auth,
    )

    if response.status_code == 200:
        return response.json().get("issues", [])
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []


def calculate_duration(start_time, end_time):
    start = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%f%z")
    end = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%f%z")
    duration = end - start
    hours = duration.total_seconds() / 3600
    days = duration.days + (duration.seconds / 86400)
    return round(hours, 2), round(days, 2)


def parse_issues(issues):
    parsed_data = []
    for issue in issues:
        ticket_id = issue["key"]
        story_points = issue["fields"].get("customfield_11503", None)
        changelog = issue["changelog"]["histories"]

        transitions = []
        for history in sorted(changelog, key=lambda x: x["created"]):
            for item in history["items"]:
                if item["field"] == "status":
                    transitions.append({
                        "from": item["fromString"],
                        "to": item["toString"],
                        "start_time": history["created"]
                    })

        for i in range(len(transitions) - 1):
            transitions[i]["end_time"] = transitions[i + 1]["start_time"]
            hours, days = calculate_duration(
                transitions[i]["start_time"], transitions[i]["end_time"]
            )
            transitions[i]["duration_hours"] = hours
            transitions[i]["duration_days"] = days

        if transitions:
            transitions[-1]["end_time"] = "Ongoing"
            transitions[-1]["duration_hours"] = None
            transitions[-1]["duration_days"] = None

        parsed_data.append({
            "ticket_id": ticket_id,
            "story_points": story_points,
            "transitions": transitions,
        })

    return parsed_data


def analyze_transitions(parsed_data):
    story_point_summary = defaultdict(int)
    transition_analysis = defaultdict(lambda: defaultdict(list))

    for issue in parsed_data:
        story_points = issue["story_points"]
        if story_points is None:
            continue

        story_point_summary[story_points] += 1

        for transition in issue["transitions"]:
            transition_name = f"From: {transition['from']} To: {transition['to']}"
            if (
                transition_name in ANALYZED_TRANSITIONS
                and transition["duration_hours"] is not None
            ):
                transition_analysis[transition_name][story_points].append(
                    transition["duration_hours"]
                )

    report = "Summary Stories by Points\n"
    for story_point, count in sorted(story_point_summary.items()):
        report += f"Story Points: {story_point} -> {count} tickets\n"
    report += "\n"

    for transition, story_point_data in transition_analysis.items():
        report += f"{transition}:\n"
        for story_point, durations in sorted(story_point_data.items()):
            avg_hours = round(sum(durations) / len(durations), 2)
            avg_days = round(avg_hours / 24, 2)
            count = len(durations)
            report += (
                f"  Story Points: {story_point} -> "
                f"Avg Duration: {avg_hours} hours ({avg_days} days) -> {count} tickets\n"
            )
        report += "\n"

    return report


def save_output_to_file(output, file_path):
    with open(file_path, "w") as file:
        file.write(output)


def main():
    print("Fetching JIRA data...")
    issues = fetch_all_jira_data()

    if issues:
        parsed_data = parse_issues(issues)
        detailed_output = f"Total Issues: {len(parsed_data)}\n"
        save_output_to_file(detailed_output, OUTPUT_FILE)
        print(f"Detailed output saved to {OUTPUT_FILE}")

        report = analyze_transitions(parsed_data)
        save_output_to_file(report, REPORT_FILE)
        print(f"Report saved to {REPORT_FILE}")
    else:
        print("No issues found.")


if __name__ == "__main__":
    main()
