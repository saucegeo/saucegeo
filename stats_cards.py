import os
import re
import requests
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.panel import Panel

# Extract GitHub stats from profile
def github_stats(user, token=None):
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        # Token is used for authenticated requests
        headers["Authorization"] = f"token {token}" 

    # Get the total number of stars across repositories
    stars = 0
    page = 1
    while True:
        # Fetch public repositories and limit to 100 repos per page
        repos_url = f"https://api.github.com/users/{user}/repos?per_page=100&page={page}"
        response = requests.get(repos_url, headers=headers)
        if response.status_code != 200:
            break
        repos_data = response.json()  # FIXED: .json() au lieu de .jsons()
        if not repos_data:
            break
        stars += sum(repo.get("stargazers_count", 0) for repo in repos_data)
        if len(repos_data) < 100:
            break
        page += 1

    # Total commits and open issues/PRs
    commit_search_url = f"https://api.github.com/search/commits?q=author:{user}"
    commit_response = requests.get(commit_search_url, headers=headers).json()
    total_commits = commit_response.get("total_count", 0)

    # Open PRs globales
    pr_search_url = f"https://api.github.com/search/issues?q=author:{user}+type:pr+state:open"
    pr_response = requests.get(pr_search_url, headers=headers).json()
    open_prs = pr_response.get("total_count", 0)

    # Open issues globales 
    issue_search_url = f"https://api.github.com/search/issues?q=author:{user}+type:issue+state:open"
    issue_response = requests.get(issue_search_url, headers=headers).json()
    open_issues = issue_response.get("total_count", 0)

    return {
        "Stars": stars,
        "Total Commits": total_commits,
        "Open Issues": open_issues,
        "Open PRs": open_prs
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

    # Use a panel to display the learning roadmap
    console.print("[khaki1]saucegeo@github-profile ~ $ [/khaki1]", end="")
    console.print(" learning-roadmap\n")
    
    roadmap_text = (
        "[indian_red1]Embedded C & Robotics:[/indian_red1]\n"
        "[pale_turquoise1] ➔ ROS2 (Robot Operating System)[/pale_turquoise1]\n"
        "[pale_turquoise1] ➔ Assembly Programming (x86/ARM)[/pale_turquoise1]\n\n"
        "[indian_red1]Hardware & Simulation:[/indian_red1]\n"
        "[pale_turquoise1] ➔ VHDL & Digital System Design[/pale_turquoise1]\n"
        "[pale_turquoise1] ➔ LTSpice Circuit Analysis[/pale_turquoise1]\n\n"
        "[indian_red1]Systems & Tools:[/indian_red1]\n"
        "[pale_turquoise1] ➔ Linux Environments & Shell Scripting[/pale_turquoise1]\n"
        "[pale_turquoise1] ➔ PlatformIO Framework & Git[/pale_turquoise1]"
    )

    panel = Panel(
        roadmap_text, 
        title="[light_pink1]Currently Learning[/light_pink1]", 
        style="white", 
        border_style="indian_red1",
        width=52,
        expand=False
    )
    console.print(panel)
    console.print("")

    console.print("[khaki1]saucegeo@github-profile ~ $ [/khaki1]", end="")
    console.print(" exit\n")
    console.print("[light_pink1]thank you for passing by ( ˘▽˘)っ♨ [/light_pink1]\n")

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
    token = os.getenv("GHT")
    
    stats = github_stats(user, token=token)

    terminal_svg = generate_terminal_svg(stats)

    os.makedirs("assets", exist_ok=True)
    with open("assets/terminal.svg", "w") as f:
        f.write(terminal_svg)