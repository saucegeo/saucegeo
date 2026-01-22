# Terminal-Style GitHub Profile Setup Guide

A comprehensive guide to create a terminal-inspired GitHub profile README, inspired by [github-readme-terminal](https://github.com/x0rzavi/github-readme-terminal), [pixel-profile](https://github.com/LuciNyan/pixel-profile), and [github-stats-terminal-style](https://github.com/yogeshwaran01/github-stats-terminal-style).

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Understanding the Three Inspiration Sources](#understanding-the-three-inspiration-sources)
4. [Step-by-Step Implementation](#step-by-step-implementation)
5. [Troubleshooting Commit Count Issues](#troubleshooting-commit-count-issues)
6. [Customization Options](#customization-options)
7. [Best Practices](#best-practices)

---

## Prerequisites

Before starting, ensure you have:

- **GitHub account** with a repository you want to showcase
- **Python 3.9+** installed locally for testing
- **GitHub Personal Access Token (PAT)** for API access
- Basic understanding of **GitHub Actions**
- **Git** installed and configured

---

## Project Setup

### Current Project Structure

```
saucegeo/
├── .env                     # Environment variables (NOT commit to git)
├── .gitignore               # Git ignore rules
├── main.yml                 # GitHub Actions workflow
├── README.md                # Your profile README (this file)
├── requirements.txt         # Python dependencies
├── stats_cards.py           # Python script for generating stats
└── venv/                    # Virtual environment
```

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Current dependencies:
- `PyInquirer` - Interactive CLI prompts
- `rich` - Beautiful terminal output
- `requests` - HTTP library for GitHub API

---

## Understanding the Three Inspiration Sources

### 1. github-readme-terminal by x0rzavi

**Approach:** Creates animated GIFs simulating a retro terminal boot sequence.

**Key Features:**
- Generates animated GIF files (not static images)
- Simulates neofetch-style output
- 10+ color schemes (yoru, gruvbox, dracula, etc.)
- ANSI escape sequence support
- TOML-based configuration
- Requires FFmpeg for GIF generation

**Best for:** Visual flair and animated profiles

**Install:**
```bash
pip install github-readme-terminal
```

**Basic Usage:**
```python
import gifos

t = gifos.Terminal(width=320, height=240, xpad=5, ypad=5)
t.gen_text(text="Hello World!", row_num=1)
github_stats = gifos.utils.fetch_github_stats(user_name="yourusername")
t.gen_gif()
```

---

### 2. pixel-profile by LuciNyan

**Approach:** Generates static pixel-art style SVG cards via API.

**Key Features:**
- Web-based API (no local setup required)
- 8 prebuilt themes (CRT, Journey, Rainbow, etc.)
- Query parameter customization
- Dark/light mode support via `<picture>` tag
- Self-hosting option to avoid rate limits
- GitHub Actions integration for auto-updates

**Best for:** Quick, easy, and beautiful static cards

**Basic Usage:**
```markdown
![GitHub Stats](https://pixel-profile.vercel.app/api/github-stats?username=saucegeo&theme=rainbow)
```

**With Dark Mode Support:**
```html
<picture decoding="async" loading="lazy">
  <source media="(prefers-color-scheme: light)" srcset="https://pixel-profile.vercel.app/api/github-stats?username=saucegeo&theme=summer">
  <source media="(prefers-color-scheme: dark)" srcset="https://pixel-profile.vercel.app/api/github-stats?username=saucegeo&screen_effect=true&theme=rainbow">
  <img alt="github stats" src="https://pixel-profile.vercel.app/api/github-stats?username=saucegeo&theme=summer">
</picture>
```

**Available Parameters:**
- `username` - GitHub username (required)
- `theme` - Theme name (crt, journey, rainbow, etc.)
- `hide` - Comma-separated list to hide (avatar,commits,issues,prs,rank,stars)
- `include_all_commits` - Count all commits (true/false)
- `pixelate_avatar` - Apply pixelation (true/false)
- `screen_effect` - Enable CRT effect (true/false)
- `dithering` - 256-color palette with dithering (true/false)
- `background` - Custom background color/image
- `color` - Custom text color

---

### 3. github-stats-terminal-style by yogeshwaran01

**Approach:** Generates static SVG images simulating terminal output with typing effects.

**Key Features:**
- Generates SVG files (not GIFs)
- 10 terminal themes (ubuntu, hacker, dracula, monokai, etc.)
- Command-line JavaScript/Node.js based
- GitHub Actions auto-update
- Direct SVG file generation

**Best for:** Terminal purists who want SVG format

**Themes Available:**
- ubuntu (default), hacker, atom, googledark, default, googlelight, dracula, monokai, github, powershell

**Usage in GitHub Actions:**
```bash
node updater.js ${{ github.repository_owner }} ubuntu
```

---

## Step-by-Step Implementation

### Approach Selection

Choose based on your needs:

| Feature | github-readme-terminal | pixel-profile | github-stats-terminal-style |
|---------|----------------------|---------------|----------------------------|
| **Format** | Animated GIF | Static SVG/IMG | Static SVG |
| **Setup Difficulty** | Medium | Easy | Easy |
| **Customization** | High | High | Medium |
| **Auto-update** | Manual/Custom | GitHub Actions | GitHub Actions |
| **API vs Local** | Local | API + Self-host | Local |
| **Visual Style** | Animated retro | Pixel art | Terminal |

---

### Implementation Option 1: Using Your Current Python Script (Custom Approach)

Your `stats_cards.py` generates a terminal-style table. Here's how to enhance it:

#### Step 2: Enhance the Script

Add image capture and GitHub Actions integration:

```python
# Add to stats_cards.py
import html2text
from rich import file_export

def generate_markdown_table(stats):
    table = Table(title="[bold green]Saucegeo's Stats[/bold green]", show_header=True, header_style="bold magenta")
    table.add_column("Stat", style="cyan", no_wrap=True)
    table.add_column("Count", style="yellow")
    
    for k, v in stats.items():
        table.add_row(k, str(v))
    
    return table

def generate_ascii_art():
    return """
╔══════════════════════════════════════════╗
║     SAUCEGEO'S GITHUB TERMINAL            ║
╠══════════════════════════════════════════╣
║  > Type 'help' for available commands     ║
╚══════════════════════════════════════════╝
    """
```

#### Step 3: Add to README

```markdown
## 📊 GitHub Stats

```text
╔══════════════════════════════════════════╗
║     SAUCEGEO'S GITHUB TERMINAL            ║
╠══════════════════════════════════════════╣
║  ⭐ Stars: 123                            ║
║  🔄 Commits: 456                          ║
║  🐛 Issues: 78                            ║
║  🔀 PRs: 23                               ║
╚══════════════════════════════════════════╝
```
```

#### Step 4: GitHub Actions Setup

Your `main.yml` is already configured. Ensure:

```yaml
name: Update Github Stats

on:
  schedule:
    - cron: "47 2 * * *"  # Runs daily at 2:47 UTC
  workflow_dispatch:      # Allow manual trigger

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run stats script
        run: python stats_cards.py
        env:
          GHT: ${{ secrets.GHT }}
      
      - name: Commit changes
        run: |
          git config --global user.name "Github Actions"
          git config --global user.email "action@github.com"
          git add .
          git commit -m "Updated GitHub stats 🎉" || echo "No changes"
          git push
```

---

### Implementation Option 2: Using pixel-profile API (Recommended for Beginners)

#### Step 1: Add to README

```markdown
## 📊 GitHub Stats

<picture decoding="async" loading="lazy">
  <source media="(prefers-color-scheme: light)" srcset="https://pixel-profile.vercel.app/api/github-stats?username=saucegeo&theme=summer">
  <source media="(prefers-color-scheme: dark)" srcset="https://pixel-profile.vercel.app/api/github-stats?username=saucegeo&screen_effect=true&theme=rainbow">
  <img alt="github stats" src="https://pixel-profile.vercel.app/api/github-stats?username=saucegeo&theme=summer">
</picture>
```

#### Step 2: Customize Your Theme

Try different themes:
- `theme=summer` - Light, colorful
- `theme=rainbow` - Dark with rainbow gradient
- `theme=crt` - Retro CRT effect
- `theme=journey` - Pixel art adventure
- `theme=monica` - Clean, modern

#### Step 3: Hide Unwanted Stats

```markdown
https://pixel-profile.vercel.app/api/github-stats?username=saucegeo&hide=rank,avatar
```

---

### Implementation Option 3: Using github-readme-terminal (For Animations)

#### Step 1: Install the Package

```bash
pip install github-readme-terminal
```

#### Step 2: Create a Script

```python
# generate_gif.py
import gifos

# Initialize terminal
t = gifos.Terminal(
    width=320, 
    height=240, 
    xpad=5, 
    ypad=5,
    color_scheme="dracula"  # Choose your theme
)

# Add boot sequence
t.gen_text("Booting system...", row_num=1)
t.gen_text("Loading kernel modules...", row_num=2)
t.gen_text("Mounting filesystem...", row_num=3)

# Fetch GitHub stats
github_stats = gifos.utils.fetch_github_stats(
    user_name="saucegeo"
)

# Display stats
t.gen_text("", row_num=4)
t.gen_text("╔═══════════════════════════╗", row_num=5)
t.gen_text("║   GITHUB STATISTICS       ║", row_num=6)
t.gen_text("╠═══════════════════════════╣", row_num=7)
t.gen_text(f"║ Name: {github_stats.account_name}", row_num=8)
t.gen_text(f"║ Repos: {github_stats.repo_count}", row_num=9)
t.gen_text(f"║ Stars: {github_stats.total_stars}", row_num=10)
t.gen_text("╚═══════════════════════════╝", row_num=11)

# Generate GIF
t.gen_gif()

# Optional: Upload to ImgBB
image = gifos.utils.upload_imgbb(
    file_name="output.gif", 
    expiration=60
)
print(f"GIF URL: {image.url}")
```

#### Step 3: Add to README

```markdown
## 💻 Terminal Profile

![Terminal Gif](./output.gif)
```

---

### Implementation Option 4: Using github-stats-terminal-style (SVG Terminal)

#### Step 1: Fork the Repository

Visit: https://github.com/yogeshwaran01/github-stats-terminal-style/generate

#### Step 2: Set Up GitHub Actions

1. Go to your forked repository
2. Settings → Secrets and Variables → Actions
3. Add secret `GHT` with your Personal Access Token

#### Step 4: Modify Workflow

Edit `.github/workflows/main.yml`:
```yaml
- name: Generate Terminal Stats
  run: node updater.js ${{ github.repository_owner }} dracula
```

#### Step 5: Add to README

```markdown
## 📊 Terminal Stats

![GitHub Stats](./github_stats.svg)
```

---

## Troubleshooting Commit Count Issues

### Issue: Commit count not displaying correctly

**Root Causes:**

1. **Token not passed to API** (Fixed in your script)
2. **API Rate Limiting**
3. **Repository has too many commits**
4. **Pagination not handling all pages**

### Solutions:

#### 1. Verify Token Authentication

```python
# Test locally
import os
import requests

token = os.getenv("GHT")
if not token:
    print("ERROR: GHT token not found!")
else:
    headers = {"Authorization": f"token {token}"}
    response = requests.get("https://api.github.com/user", headers=headers)
    print(f"Authenticated as: {response.json().get('login')}")
```

#### 2. Check Rate Limits

```python
response = requests.get("https://api.github.com/rate_limit", headers=headers)
print(response.json())
```

#### 3. Use GitHub's Contribution Count API

For repositories with many commits, use the `/stats/participation` endpoint:

```python
def get_total_commits_v2(user, repo, token=None):
    headers = {"Authorization": f"token {token}"} if token else {}
    
    # Get contributor stats (more accurate for large repos)
    response = requests.get(
        f"https://api.github.com/repos/{user}/{repo}/stats/contributors",
        headers=headers
    )
    
    if response.status_code == 200:
        contributors = response.json()
        total = sum(sum(c['weeks'][i]['c'] for i in range(len(c['weeks']))) 
                   for c in contributors)
        return total
    else:
        # Fallback to original method
        return get_total_commits_v1(user, repo, token)
```

#### 4. Add Caching to GitHub Actions

Modify `main.yml`:
```yaml
- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

#### 5. Use GraphQL API (Better for Complex Queries)

```python
def get_commits_graphql(user, repo, token):
    query = """
    query {
        repository(owner: "%s", name: "%s") {
            defaultBranchRef {
                target {
                    ... on Commit {
                        history(first: 100) {
                            totalCount
                        }
                    }
                }
            }
        }
    }
    """ % (user, repo)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query},
        headers=headers
    )
    
    return response.json()["data"]["repository"]["defaultBranchRef"]["target"]["history"]["totalCount"]
```

---

## Customization Options

### Color Themes

#### For Python/Rich Terminal

```python
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "error": "bold red",
    "success": "bold green",
})

console = Console(theme=custom_theme)
```

#### For pixel-profile

```markdown
https://pixel-profile.vercel.app/api/github-stats?username=saucegeo&background=#1a1a2e&color=#e94560
```

#### For github-stats-terminal-style

```bash
node updater.js saucegeo dracula  # Available: ubuntu, hacker, atom, googledark, default, googlelight, dracula, monokai, github, powershell
```

### Adding More Stats

Add these to your Python script:

```python
def github_stats_extended(user, repo, token=None):
    headers = {"Authorization": f"token {token}"} if token else {}
    
    # Basic repo data
    repo_data = requests.get(f"https://api.github.com/repos/{user}/{repo}", headers=headers).json()
    
    # Extended stats
    watchers = repo_data.get("subscribers_count", 0)
    forks = repo_data.get("forks_count", 0)
    size = repo_data.get("size", 0)  # Size in KB
    language = repo_data.get("language", "Unknown")
    created_at = repo_data.get("created_at", "")
    
    return {
        "Stars": repo_data.get("stargazers_count", 0),
        "Total Commits": get_total_commits_v2(user, repo, token),
        "Open Issues": repo_data.get("open_issues_count", 0),
        "Open PRs": len(requests.get(f"https://api.github.com/repos/{user}/{repo}/pulls?state=open", headers=headers).json()),
        "Watchers": watchers,
        "Forks": forks,
        "Size (KB)": size,
        "Language": language,
        "Created": created_at[:10],  # YYYY-MM-DD
    }
```

### Adding ASCII Art Header

```python
def get_ascii_header(username):
    return f"""
╔══════════════════════════════════════════════════╗
║                                                  ║
║     ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███╗     ║
║     ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║████╗    ║
║     ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║██╔██╗   ║
║     ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║██║╚██╗  ║
║     ██║ ╚████║███████╗██║ ╚████║   ██║██║ ╚████ ║
║     ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝   ╚═╝╚═╝  ╚═══╝ ║
║                                                  ║
║              github.com/{username.ljust(23)} ║
║                                                  ║
╚══════════════════════════════════════════════════╝
    """
```

---

## Best Practices

### 1. Security

- ✅ Never commit `.env` file (already in `.gitignore`)
- ✅ Use GitHub Secrets for tokens
- ✅ Use fine-grained PAT with minimal permissions
- ✅ Rotate tokens regularly

### 2. Performance

- ✅ Use GitHub Actions caching
- ✅ Set reasonable cron schedules (don't run too frequently)
- ✅ Implement proper error handling
- ✅ Use pagination for large datasets

### 3. Maintenance

- ✅ Document your setup
- ✅ Keep dependencies updated
- ✅ Monitor GitHub Actions logs
- ✅ Test changes locally before pushing

### 4. README.md Best Practices

```markdown
# [Your Name]

## 🎯 About Me

Brief description...

## 📊 Stats

[Your stats card here]

## 🛠️ Tech Stack

- Python
- JavaScript
- Etc.

## 🔗 Links

- [Portfolio](https://yourportfolio.com)
- [LinkedIn](https://linkedin.com/in/you)
```

---

## Complete Example README

```markdown
# 👨‍💻 Saucegeo

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=00ff00&background=000000&center=true&vCenter=true&width=600&lines=Hello,+I'm+Saucegeo!;Full+Stack+Developer;Open+Source+Enthusiast;Welcome+to+my+terminal!" alt="Typing SVG" />
</p>

## 📊 GitHub Stats

<picture decoding="async" loading="lazy">
  <source media="(prefers-color-scheme: light)" srcset="https://pixel-profile.vercel.app/api/github-stats?username=saucegeo&theme=summer">
  <source media="(prefers-color-scheme: dark)" srcset="https://pixel-profile.vercel.app/api/github-stats?username=saucegeo&screen_effect=true&theme=rainbow">
  <img alt="github stats" src="https://pixel-profile.vercel.app/api/github-stats?username=saucegeo&theme=summer">
</picture>

## 🛠️ Tech Stack

```text
Languages:
  Python       ████████████████░░░░  70%
  JavaScript   ██████████████░░░░░░  60%
  TypeScript   ██████████░░░░░░░░░░  40%
  Go           █████░░░░░░░░░░░░░░░  20%
```

## 🔗 Connect

- [Website](https://saucegeo.dev)
- [GitHub](https://github.com/saucegeo)
- [LinkedIn](https://linkedin.com/in/saucegeo)

---

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=saucegeo&label=Profile+Views&color=00ff00&style=flat-square" alt="Profile Views" />
</p>
```

---

## Resources & References

### Inspiration Repositories

- [github-readme-terminal](https://github.com/x0rzavi/github-readme-terminal) - Animated GIF terminal generator
- [pixel-profile](https://github.com/LuciNyan/pixel-profile) - Pixel art stats cards API
- [github-stats-terminal-style](https://github.com/yogeshwaran01/github-stats-terminal-style) - SVG terminal stats generator

### Useful Tools

- [Readme Typing SVG](https://github.com/DenverCoder1/readme-typing-svg) - Animated typing effect
- [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats) - Classic stats cards
- [Termtosvg](https://github.com/nbedos/termtosvg) - Terminal to SVG converter
- [ASCII Art Generator](https://patorjk.com/software/taag/) - Create ASCII art

### Documentation

- [GitHub API Documentation](https://docs.github.com/en/rest)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Rich Library](https://rich.readthedocs.io/)

---

## License

This guide is inspired by and built upon the work of:
- [x0rzavi/github-readme-terminal](https://github.com/x0rzavi/github-readme-terminal) (MIT License)
- [LuciNyan/pixel-profile](https://github.com/LuciNyan/pixel-profile) (MIT License)
- [yogeshwaran01/github-stats-terminal-style](https://github.com/yogeshwaran01/github-stats-terminal-style) (MIT License)

---

<p align="center">
  <sub>Built with ❤️ using terminal vibes</sub>
</p>
