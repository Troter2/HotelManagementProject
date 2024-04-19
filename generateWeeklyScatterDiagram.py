from datetime import datetime, timezone, timedelta

import matplotlib.pyplot as plt
from github import Github

from generateScatterDiagram import token, repo_name

# This code generates a scatter diagram with all the issues
# closed on this week, showing the creation data and the days for
# closing. It runs automatically every Sunday on 23:59 using the
# "scatterWeeklyGenerator.yml" workflow.

g = Github(token)
repo = g.get_repo(repo_name)

days_to_close = []
issue_created_dates = []


def main() -> None:
    get_data()
    generate_diagram()


def get_date_range_of_current_week() -> tuple:
    """Gets the date range of the current week from Monday to Sunday as datetime objects, making them timezone aware."""
    current_date = datetime.now(timezone.utc)
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    start_of_week = datetime.combine(start_of_week.date(), datetime.min.time(), tzinfo=timezone.utc)
    end_of_week = datetime.combine(end_of_week.date(), datetime.max.time(), tzinfo=timezone.utc)
    return start_of_week, end_of_week


def get_data() -> None:
    """Gets all the closed issues with their open date and time to close"""
    start_of_week, end_of_week = get_date_range_of_current_week()
    issues = repo.get_issues(state='closed')

    for issue in issues:
        closed_at = issue.closed_at

        if closed_at is not None and start_of_week <= closed_at:
            created_at = issue.created_at
            time_to_close = (closed_at - created_at).days
            days_to_close.append(time_to_close)
            issue_created_dates.append(created_at)


def generate_diagram() -> None:
    """Generates and saves the scatter diagram with all the data"""
    plt.figure(figsize=(10, 6))

    plt.scatter(days_to_close, issue_created_dates, color='blue', alpha=0.7)

    plt.xlabel('Days for closing the issue')
    plt.ylabel('Date of creation of the issue')
    plt.title(f'Scatter Diagram of closed issues - {get_date()}')
    plt.grid(True)

    plt.savefig("scatter_diagram_issues_weekly.png")


def get_date() -> str:
    """The format is: MX-WY-Report -> where X is the month number and Y is the week number"""
    now = datetime.now()
    month = now.strftime("%m")
    week_of_year = int(now.strftime("%U"))
    first_day_of_month = now.replace(day=1)
    week_of_first_day = int(first_day_of_month.strftime("%U"))
    week_of_month = week_of_year - week_of_first_day + 1
    return f"M{month}-W{week_of_month}-Report"


if __name__ == '__main__':
    main()
