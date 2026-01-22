import os
from rich import print
from rich.console import Console
from rich.table import Table
from rich.text import Text
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
    console = Console(width=800, record=True)
    console.print(banner())
    svg = console.export_svg()
    return svg


def generate_stats_svg(stats):
    console = Console(width=800, record=True)
    
    table = Table(title="[bold green]Saucegeo's Stats[/bold green]", show_header=True, header_style="bold magenta")
    table.add_column("Stat", style="cyan", no_wrap=True)
    table.add_column("Count", style="yellow")
    
    for k, v in stats.items():
        table.add_row(k, str(v))
    
    console.print(table)
    svg = console.export_svg()
    return svg


if __name__ == "__main__":
    print(banner())
    
    user = "saucegeo"
    repo = "saucegeo"
    token = os.getenv("GHT")
    stats = github_stats(user, repo, token=token)

    console = Console()
    
    table = Table(title="[bold green]Saucegeo's Stats[/bold green]", show_header=True, header_style="bold magenta")
    table.add_column("Stat", style="cyan", no_wrap=True)
    table.add_column("Count", style="yellow")
    
    for k, v in stats.items():
        table.add_row(k, str(v))
    
    console.print(table)
    
    banner_svg = generate_banner_svg()
    stats_svg = generate_stats_svg(stats)
    
    os.makedirs("assets", exist_ok=True)
    
    with open("assets/banner.svg", "w") as f:
        f.write(banner_svg)
    
    with open("assets/stats.svg", "w") as f:
        f.write(stats_svg)
    
    print("\n✅ Generated assets/banner.svg")
    print("✅ Generated assets/stats.svg")
