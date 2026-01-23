import os
from rich import print
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.align import Align
import requests

# color taken from https://rich.readthedocs.io/en/stable/appendix/colors.html

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

    console.print("[khaki1]saucegeo@github-profile ~ $ [/khaki1]", end="")
    console.print(" echo [indian_red1]'Hello there, my name is'[/indian_red1]\n")
    console.print("[pale_turquoise1]Hello there, my name is[/pale_turquoise1]\n")

    console.print("[khaki1]saucegeo@github-profile ~ $ [/khaki1]", end="")
    console.print(" ascii-name\n")

    console.print("[indian_red1]      ██╗   ██╗ █████╗  ██████╗██╗███╗   ██╗███████╗[/indian_red1]".center(70))
    console.print("[indian_red1]      ╚██╗ ██╔╝██╔══██╗██╔════╝██║████╗  ██║██╔════╝[/indian_red1]".center(70))
    console.print("[indian_red1]       ╚████╔╝ ███████║██║     ██║██╔██╗ ██║█████╗  [/indian_red1]".center(70))
    console.print("[indian_red1]        ╚██╔╝  ██╔══██║██║     ██║██║╚██╗██║██╔══╝  [/indian_red1]".center(70))
    console.print("[indian_red1]         ██║   ██║  ██║╚██████╗██║██║ ╚████║███████╗[/indian_red1]".center(70))
    console.print("[indian_red1]         ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝[/indian_red1]\n".center(70))
    console.print("[khaki1]saucegeo@github-profile ~ $ [/khaki1]", end="")
    console.print(" github-stats")

    table = Table(show_header=True, header_style="indian_red1", expand=False, box=None, padding=(0, 1))
    table.add_column("", style="pale_turquoise1", no_wrap=True)
    table.add_column("", style="indian_red1", justify="right")

    table.add_row("Stars", f"{stats['Stars']}")
    table.add_row("Total Commits", f"{stats['Total Commits']}")
    table.add_row("Open Issues", f"{stats['Open Issues']}")
    table.add_row("Open PRs", f"{stats['Open PRs']}")

    console.print(table)
    console.print("")

    console.print("[khaki1]saucegeo@github-profile ~ $ [/khaki1]", end="")
    console.print(" about-me\n")
    console.print(Align.center("[light_pink1]I'm a computer engineering student with a passion \n    for Robotics, Hardware, and Open Source.[/light_pink1]\n", vertical="middle"))

    console.print("[khaki1]saucegeo@github-profile ~ $ [/khaki1]", end="")
    console.print(" learning-roadmap\n")
    console.print("╔═════════════════════════════════════════╗")
    console.print("║            Currently Learning           ║")
    console.print("╠═════════════════════════════════════════╣")
    console.print("║                                         ║")
    console.print("║  [indian_red1]Embedded C & Robotics:[/indian_red1]                 ║")
    console.print("║  [pale_turquoise1]*** ROS2                               [/pale_turquoise1]║")
    console.print("║  [pale_turquoise1]*** Assembly Programming               [/pale_turquoise1]║")
    console.print("║                                         ║")
    console.print("║  [indian_red1]Web/UI:[/indian_red1]                                ║")
    console.print("║  [pale_turquoise1]*** Typescript                         [/pale_turquoise1]║")
    console.print("║  [pale_turquoise1]*** React + Vite                       [/pale_turquoise1]║")
    console.print("║                                         ║")
    console.print("║  [indian_red1]Tools:[/indian_red1]                                 ║")
    console.print("║  [pale_turquoise1]*** Linux/Bash                         [/pale_turquoise1]║")
    console.print("║  [pale_turquoise1]*** Git & GitHub                       [/pale_turquoise1]║")
    console.print("║                                         ║")
    console.print("╚═════════════════════════════════════════╝\n")

    console.print("[khaki1]saucegeo@github-profile ~ $ [/khaki1]", end="")
    console.print(" exit\n")
    console.print("[light_pink1]thank you for passing by ( ˘▽˘)っ♨ [/light_pink1]\n")

    import re
    svg = console.export_svg()

    # Remove width and height attributes from the <svg ...> tag
    svg = re.sub(r'(<svg[^>]*)\swidth="[^"]*"', r'\1', svg)
    svg = re.sub(r'(<svg[^>]*)\sheight="[^"]*"', r'\1', svg)

    # Inject JetBrains Mono font CSS into the first <style> block after <svg ...><defs><style ...>
    font_css = """
    @font-face {
        font-family: 'JetBrains Mono';
        font-style: normal;
        font-weight: 400;
        src: url('https://fonts.gstatic.com/s/jetbrainsmono/v16/1Ptug8zYS_SKggPNyC0ISg.woff2') format('woff2');
    }
    * { font-family: 'JetBrains Mono', monospace !important; }
    """
    svg = re.sub(r'(<style[^>]*>)', r'\1' + font_css, svg, count=1)

    # Add responsive style to <svg> tag (width:100%, max-width:600px, etc.)
    svg = re.sub(r'<svg([^>]*)', r'<svg\1 style="width:100%; max-width:600px; height:auto; display:block;"', svg, count=1)

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
