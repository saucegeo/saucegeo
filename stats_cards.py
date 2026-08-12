import os
import re
import requests
from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.panel import Panel

# Color taken from https://rich.readthedocs.io/en/stable/appendix/colors.html
# ASCII text generated using https://patorjk.com/software/taag/#p=display&f=Big&t=saucegeo

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
        
        # Check if the API request was successful (status code 200)
        if response.status_code != 200:
            break
        repos_data = response.json() # Parse the JSON response
        
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

# Create a terminal-like UI using Rich library and generate SVG output
def generate_terminal_svg(stats, light_theme=False):

# Define colors based on the system theme (light or dark)
    if light_theme == True:
        # Light theme colors
        c_prompt = "grey23" # For command prompt
        c_red = "#40c463" # For headers and important text (GitHub green)
        c_text = "black" # For regular text
        c_title = "grey23" # For titles
        c_border = c_red # For panel border

    else:
        c_prompt = "grey66" # For command prompt
        c_red = "#39d353" # For headers and important tex (GitHub green)
        c_text = "grey84" # For regular text
        c_title = "dark_sea_green4" # For titles
        c_border = c_red # For panel border

    # Create a console object to record the output and generate SVG
    # SVG use vectors instead of pixels, so can scale image without losing quality
    console = Console(width=70, record=True, force_terminal=True, legacy_windows=False)
    console.print("\n")

    # Display command (mimicking a terminal)
    console.print(f"[{c_prompt}]saucegeo@github-profile ~ $ [/{c_prompt}]", end="")
    console.print(f"[{c_text}]fetch-profile --user saucegeo[/{c_text}]\n")

    # Display ASCII name for GitHub profile
    # Use rich Align to center function to center the ASCII art in the terminal
    console.print(Align.center(f"[{c_red}]  ▗▖  ▗▖▗▄▖  ▗▄▄▖▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖[/{c_red}]"))
    console.print(Align.center(f"[{c_red}]   ▝▚▞▘▐▌ ▐▌▐▌     █  ▐▛▚▖▐▌▐▌   [/{c_red}]"))
    console.print(Align.center(f"[{c_red}]    ▐▌ ▐▛▀▜▌▐▌     █  ▐▌ ▝▜▌▐▛▀▀▘[/{c_red}]"))
    console.print(Align.center(f"[{c_red}]    ▐▌ ▐▌ ▐▌▝▚▄▄▖▗▄█▄▖▐▌  ▐▌▐▙▄▄▖[/{c_red}]"))
    console.print(Align.center(f"[{c_text}]\nComputer Engineering Student @ Concordia[/{c_text}]"))
    console.print("")
    
    # Display GitHub stats and description
    console.print(f"  [{c_red}]➤[/{c_red}] [{c_text}]Stats: {stats['Total Commits']} Commits | {stats['Stars']} Stars | {stats['Open PRs']} PRs[/{c_text}]")
    console.print(f"  [{c_red}]➤[/{c_red}] [{c_text}]Languages : C, C++, Java, ARM Assembly [/{c_text}]")
    console.print(f"  [{c_red}]➤[/{c_red}] [{c_text}]Graphics : OpenGL [/{c_text}]")
    console.print(f"  [{c_red}]➤[/{c_red}] [{c_text}]Hardware : ESP32, Arduino, Rasperry Pi [/{c_text}]")
    console.print(f"  [{c_red}]➤[/{c_red}] [{c_text}]Learning : Python & Lua [/{c_text}]")
    console.print("\n")


    # Footer with border to mimic a terminal window
    console.print(f"[{c_red}]└{' ' * 68}┘[/{c_red}]")   

    svg = console.export_svg()

# Replace the default background color
    if light_theme == True:
        svg = svg.replace('fill="#292929"', 'fill="#ffffff"') 
        svg = svg.replace('fill="#c9c9c9"', 'fill="#24292e"')
        svg = svg.replace('fill="#cccccc"', 'fill="#24292e"')
        svg = svg.replace('stroke="rgba(255,255,255,0.35)"', 'stroke="rgba(0,0,0,0.1)"')
    else:
        svg = svg.replace('fill="#292929"', 'fill="#0d1117"')

    # Remove width and height attributes from the <svg ...> tag
    svg = re.sub(r'(<svg[^>]*)\swidth="[^"]*"', r'\1', svg)
    svg = re.sub(r'(<svg[^>]*)\sheight="[^"]*"', r'\1', svg)

    # Use JetBrains Mono font for the SVG output -> terminal like display
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

    # SVG will scale to fit the container, maintaing the aspect ratio (max width: 600px)
    svg = re.sub(r'<svg([^>]*)', r'<svg\1 style="width:100%; max-width:600px; height:auto; display:block;"', svg, count=1)

    return svg

# Main method to run the script and generate the terminal UI SVG
if __name__ == "__main__":
    user = "saucegeo" # GitHub username
    token = os.getenv("GHT") # GitHub token for authenticated requests -> used to avoid rate limit using GitHub API
    
    stats = github_stats(user, token=token) # Get GitHub stats
    os.makedirs("assets", exist_ok=True) # Create the assets directory if it doesn't exist

    # Generate and save dark mode SVG
    terminal_svg_dark = generate_terminal_svg(stats) # Generate the terminal UI SVG with stats
    with open("assets/terminal-dark.svg", "w") as f:
        f.write(terminal_svg_dark)

    # Generate and save light mode SVG
    terminal_svg_light = generate_terminal_svg(stats, light_theme=True)
    with open("assets/terminal-light.svg", "w") as f:
        f.write(terminal_svg_light)