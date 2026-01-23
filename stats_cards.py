import os
from rich import print
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.align import Align # used to center elements
import requests

def banner():
    txt = Text()
    txt.append("""
██╗   ██╗ █████╗  ██████╗██╗███╗   ██╗███████╗
╚██╗ ██╔╝██╔══██╗██╔════╝██║████╗  ██║██╔════╝
 ╚████╔╝ ███████║██║     ██║██╔██╗ ██║█████╗  
  ╚██╔╝  ██╔══██║██║     ██║██║╚██╗██║██╔══╝  
   ██║   ██║  ██║╚██████╗██║██║ ╚████║███████╗
   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝╚═╝  ╚═══╝╚══════╝  
""", style="bold bright_magenta")
    return txt


def github_stats(user, repo, token=None):
    headers = {"Authorization": f"token {token}"} if token else {}
    
    repo_data = requests.get(f"https://api.github.com/repos/{user}/{repo}", headers=headers).json()
    stars = repo_data.get("stargazers_count", 0)
    issues = repo_data.get("open_issues_count", 0)
    pulls = requests.get(f"https://api.github.com/repos/{user}/{repo}/pulls?state=open", headers=headers).json()
    
    commits_url = f"https://api.github.com/repos/{user}/{repo}/commits"
    total_commits = 0
    page = 1
    per_page = 100
    
    while True:
        response = requests.get(f"{commits_url}?per_page={per_page}&page={page}", headers=headers)
        if response.status_code != 200:
            break
        commits = response.json()
        if not commits:
            break
        total_commits += len(commits)
        page += 1
        if len(commits) < per_page:
            break
    
    return {
        "Stars": stars,
        "Total Commits": total_commits,
        "Open Issues": issues,
        "Open PRs": len(pulls),
    }


def generate_banner_svg():
    console = Console(width=60, record=True, force_terminal=True, legacy_windows=False)
    console.print("\n")
    centered_banner = Align.center(banner(), vertical="middle")
    console.print(centered_banner)
    console.print("\n")
    svg = console.export_svg()
    
    svg = svg.replace('<svg ', '<svg style="width:100%; max-width:450px; height: auto;" ')
    return svg


def generate_stats_svg(stats):
    console = Console(width=50, record=True, force_terminal=True, legacy_windows=False)
    
    console.print("\n")
    table = Table(title="[bold green]Saucegeo's Stats[/bold green]", show_header=True, header_style="bold magenta", expand=False)
    table.add_column("Stat", style="cyan", no_wrap=True, justify="left", width=15)
    table.add_column("Count", style="yellow", justify="right", width=10)
    
    for k, v in stats.items():
        table.add_row(k, str(v))
    
    centered_table = Align.center(table, vertical="middle")
    console.print(centered_table)
    console.print("\n")
    svg = console.export_svg()
    
    svg = svg.replace('<svg ', '<svg style="width:100%; max-width:350px; height: auto;" ')
    return svg


if __name__ == "__main__":
    user = "saucegeo"
    repo = "saucegeo"
    token = os.getenv("GHT")
    stats = github_stats(user, repo, token=token)

    banner_svg = generate_banner_svg()
    stats_svg = generate_stats_svg(stats)
    
    os.makedirs("assets", exist_ok=True)
    
    with open("assets/banner.svg", "w") as f:
        f.write(banner_svg)
    
    with open("assets/stats.svg", "w") as f:
        f.write(stats_svg)
    
    print("\n✅ Generated assets/banner.svg")
    print("✅ Generated assets/stats.svg")
