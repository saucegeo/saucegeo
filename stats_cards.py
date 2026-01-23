import os
from rich import print
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.align import Align
import requests


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


def generate_terminal_svg(stats):
    console = Console(width=70, record=True, force_terminal=True, legacy_windows=False)

    console.print("\n")

    # Terminal header with user@hostname
    console.print("[bold green]saucegeo@github-profile ~ $ [/bold green]", end="")

    # Greeting command
    console.print(" echo 'Hi, my name is'")
    console.print("[bold cyan]Hi, my name is[/bold cyan]\n")

    # ASCII art command
    console.print("[bold green]saucegeo@github-profile ~ $ [/bold green]", end="")
    console.print(" ascii-art saucegeo")

    console.print("[bold bright_magenta]██╗   ██╗ █████╗  ██████╗██╗███╗   ██╗███████╗[/bold bright_magenta]")
    console.print("[bold bright_magenta]╚██╗ ██╔╝██╔══██╗██╔════╝██║████╗  ██║██╔════╝[/bold bright_magenta]")
    console.print("[bold bright_magenta] ╚████╔╝ ███████║██║     ██║██╔██╗ ██║█████╗  [/bold bright_magenta]")
    console.print("[bold bright_magenta]  ╚██╔╝  ██╔══██║██║     ██║██║╚██╗██║██╔══╝  [/bold bright_magenta]")
    console.print("[bold bright_magenta]   ██║   ██║  ██║╚██████╗██║██║ ╚████║███████╗[/bold bright_magenta]")
    console.print("[bold bright_magenta]   ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝╚═╝  ╚═══╝╚══════╝[/bold bright_magenta]\n")

    # Stats command
    console.print("[bold green]saucegeo@github-profile ~ $ [/bold green]", end="")
    console.print(" github-stats")

    table = Table(show_header=True, header_style="bold magenta", expand=False, box=None, padding=(0, 1))
    table.add_column("", style="cyan", no_wrap=True)
    table.add_column("", style="yellow", justify="right")

    table.add_row("Stars", f"{stats['Stars']}")
    table.add_row("Total Commits", f"{stats['Total Commits']}")
    table.add_row("Open Issues", f"{stats['Open Issues']}")
    table.add_row("Open PRs", f"{stats['Open PRs']}")

    console.print(table)
    console.print("")

    # Tech stack command
    console.print("[bold green]saucegeo@github-profile ~ $ [/bold green]", end="")
    console.print(" tech-stack --list\n")

    console.print("[bold cyan]╔═══════════════════════════════════════════════════╗[/bold cyan]")
    console.print("[bold cyan]║              TECHNOLOGIES & TOOLS                    ║[/bold cyan]")
    console.print("[bold cyan]╠═══════════════════════════════════════════════════╣[/bold cyan]")
    console.print("[bold cyan]║                                                       ║[/bold cyan]")
    console.print("[bold cyan]║  [bold yellow]Languages:[/bold yellow]                                        ║[/bold cyan]")
    console.print("[bold cyan]║  [bold green]Python       ████████████████░░░░░[/bold green]              [bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║  [bold blue]JavaScript   ██████████████░░░░░░░░[/bold blue]             [bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║  [bold magenta]TypeScript   ████████░░░░░░░░░░░░░░[/bold magenta]           [bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║  [bold cyan]Go           ██████████░░░░░░░░░░░  [/bold cyan]            [bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║                                                       ║[/bold cyan]")
    console.print("[bold cyan]║  [bold yellow]Frameworks & Tools:[/bold yellow]                             ║[/bold cyan]")
    console.print("[bold cyan]║  🐍 Django    📊 NumPy    🎨 Tailwind                ║[/bold cyan]")
    console.print("[bold cyan]║  ⚛️ React      🔥 Firebase  🐳 Docker                 ║[/bold cyan]")
    console.print("[bold cyan]║  📱 Next.js    🔵 GraphQL  🌐 Vercel                  ║[/bold cyan]")
    console.print("[bold cyan]║                                                       ║[/bold cyan]")
    console.print("[bold cyan]╚═══════════════════════════════════════════════════╝[/bold cyan]")
    console.print("")

    svg = console.export_svg()
    svg = svg.replace('<svg ', '<svg style="width:100%; max-width:600px; height: auto;" ')
    return svg


if __name__ == "__main__":
    user = "saucegeo"
    repo = "saucegeo"
    token = os.getenv("GHT")
    stats = github_stats(user, repo, token=token)

    terminal_svg = generate_terminal_svg(stats)

    os.makedirs("assets", exist_ok=True)

    with open("assets/terminal.svg", "w") as f:
        f.write(terminal_svg)

    print("\n✅ Generated assets/terminal.svg")
    print("✅ Single terminal SVG with all commands!")
