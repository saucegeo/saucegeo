# TUI GitHub Portfolio

## Overview
My profile README.md is designed to look a Terminal User Interface (TUI)
directly on the GitHub profile page. It was made using Python and the rich library.

## How it works
1. Authentification: the pipeline use a GitHub Personal Access Token to authenticate API requests
2. Data Fetching: once authenticated, the script fetch up to 100 repos and parse the JSON data
3. Rendering: a function processes the data, structure the TUI layout and export an SVG file (light and dark mode)
4. Pipeline: a GitHub Actions workflow automatically triggers script every 50 to 70 minutes to update the GitHub Stats

## Features
- Terminal UI that is highly customizable and text formatting powered by the Textualize/rich library
- Real-time automation pipeline
