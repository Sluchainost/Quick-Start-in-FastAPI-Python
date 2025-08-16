# Quick Start in FastAPI Python

This repository is created to store solutions to problems from the course on [Stepik](https://stepik.org/179694) < -- click

## Who is this course for

The target audience for this course includes Python developers and web programmers who want to learn how to build modern web APIs using FastAPI, regardless of their level of experience with web frameworks or API development.

## ⚙️ Project Configuration Files

This section describes the purpose of key configuration files used in this project to ensure consistency, automation, and a streamlined development process.

### `pyproject.toml`

* **Purpose:** The modern standard file for configuring Python projects, introduced in PEP 518.
* **How it works:** Used to define project metadata, build dependencies (e.g., for `setuptools`, `poetry`, `pdm`), and can also contain configurations for various development tools (e.g., `black`, `isort`, `pytest`, `mypy`, `ruff`).
* **Benefit:** Centralizes project and tool configuration, replacing multiple individual configuration files (e.g., `setup.py`, `MANIFEST.IN`, `.isort.cfg`). Provides a more declarative and standardized way to manage the project.
  * *Note: If `pyproject.toml` is used for dependency management (e.g., with Poetry or PDM), it can replace `requirements.txt`.*

### `.gitignore`

* **Purpose:** Specifies intentionally untracked files and directories that Git should ignore.
* **How it works:** Git reads this file and does not track changes in files/folders matching the patterns listed.
* **Benefit:** Prevents unnecessary, temporary, local, or sensitive files (e.g., `__pycache__`, `venv/`, `.env`, logs, compiled files) from being committed to the repository, keeping the repository clean, small, and secure.

### `.editorconfig`

* **Purpose:** Helps maintain consistent coding styles for multiple developers working on the same project across various editors and IDEs.
* **How it works:** Defines basic formatting rules (indentation style, indent size, encoding, line endings, etc.). Editors with EditorConfig support automatically apply these settings.
* **Benefit:** Helps avoid formatting conflicts and makes the codebase more consistent and readable for all team members.

### `.vscode/` (Directory for Visual Studio Code Settings)

This directory contains configuration files specific to the Visual Studio Code editor, which help standardize the development environment for developers using this editor.

#### `.vscode/extensions.json`

* **Purpose:** Contains a list of recommended VS Code extensions for this project.
* **How it works:** When the project is opened, VS Code can prompt the user to install these extensions if they are not already present.
* **Benefit:** Simplifies environment setup for new developers and ensures a consistent set of tools is used across the team.

#### `.vscode/launch.json`

* **Purpose:** Defines configurations for launching and debugging the project in VS Code.
* **How it works:** Allows you to configure how to run the application (e.g., with specific arguments, environment variables) and how to attach the debugger.
* **Benefit:** Streamlines the process of running and debugging the application directly from the editor, making it more efficient.

#### `.vscode/settings.json`

* **Purpose:** Allows overriding global VS Code settings at the project (workspace) level.
* **How it works:** Settings specified here (e.g., default formatter, linter-specific settings) will take precedence over global VS Code settings, but only when this project is open.
* **Benefit:** Tailors the development environment to the specific needs of the project without altering global editor preferences.

#### `.vscode/tasks.json`

* **Purpose:** Defines custom tasks that can be run in VS Code.
* **How it works:** Allows you to set up commands for performing routine operations (e.g., running tests, formatting code, building the project, starting a development server).
* **Benefit:** Automates frequently performed actions, making them accessible with a single click or keyboard shortcut from the editor.
