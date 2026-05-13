# Claude Code Installation & Usage Guide

## 1. Installation

### Prerequisites: Node.js and npm

Claude Code is an npm package and requires **Node.js** (v18+) and **npm** to be installed first.

#### Windows

Download and install Node.js from the official site (includes npm):

1. Go to https://nodejs.org and download the LTS installer
2. Run the installer and follow the prompts (ensure "Add to PATH" is checked)
3. Verify installation:

```powershell
node --version
npm --version
```

Alternatively, install via `winget`:

```powershell
winget install OpenJS.NodeJS.LTS
```

#### Linux

Install via your package manager:

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version
npm --version
```

Or use `nvm` (Node Version Manager) for flexible version management:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
nvm install --lts
```

### Windows Installation

Create the missing npm global directory (if it doesn't exist) and install Claude Code:

```powershell
# Create the missing npm global directory
New-Item -ItemType Directory -Path "$env:APPDATA\npm" -Force

# Install Claude Code globally
npm install -g @anthropic-ai/claude-code
```

Alternatively, run the native installer via PowerShell:

```powershell
irm claude.ai | iex
```

**Git Requirement:** Ensure Git for Windows is installed, as Claude uses Git Bash internally for execution.

**Path Configuration:** If Git is not globally registered, add its fallback location inside your global `settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

### Linux Installation

Install via the global Node Package Manager (npm):

```bash
npm install -g @anthropic-ai/claude-code
```

Alternative native installations can be pulled via GitHub Debian Build Releases for specific package management tooling.

### Initial Authentication

Initialize the agent environment and log in to link your Anthropic credentials:

```bash
claude
```

## 2. Calling an Agent

### Terminal Execution (Interactive & Non-Interactive)

Launch a direct interactive agent session within any local directory:

```bash
claude
```

Execute a single, one-off instruction non-interactively using the `--p` parameter:

```bash
claude --p "Analyze the files in this directory and write a short summary to SUMMARY.md"
```

Pre-approve specific tools to avoid interactive confirmation prompts:

```bash
claude --p "Refactor utils.py" --approvedTool edit --approvedTool bash
```

Run a specific chat agent defined in `.claude/agents/`:

```bash
claude --p "What is 9 + 27" --agent calculating
claude --p "Say hello to the world" --agent texting
claude --p "Calculate 5^2 then greet me" --agent orchestrator
```

### Why `--p` and `--approvedTool` Are Needed for Automated Pipelines

When running Claude Code in an automated pipeline (CI/CD, cron jobs, subprocess calls), there is no human at the keyboard to respond to interactive prompts. Two flags solve this:

| Flag | Purpose |
|------|----------|
| `--p` | Passes the prompt as a non-interactive argument, so Claude executes the instruction and exits instead of launching an interactive REPL session. Without it, the process hangs waiting for user input. |
| `--approvedTool` | Pre-authorizes specific tools (e.g., `edit`, `bash`, `read`) so Claude can use them without pausing for confirmation. Without it, Claude will halt at every tool-use confirmation wall, blocking the pipeline. Specify once per tool. |

Together, these flags enable fully unattended execution — the CLI receives the prompt, uses the approved tools autonomously, and returns the result via stdout.

### Python Automated Pipeline (subprocess)

When wrapping Claude within automated pipelines, use `--p` for the prompt and `--approvedTool` for each tool the agent is allowed to use. This prevents the CLI from hanging on interactive confirmation walls:

```python
import subprocess
import os

def run_claude_pipeline(prompt_text: str, agent: str = None) -> str:
    # Ensure your Anthropic API Key is visible to the process environment
    env = os.environ.copy()

    # Execute non-interactively via argument list
    command = [
        "claude", "--p", prompt_text,
        "--approvedTool", "edit",
        "--approvedTool", "bash",
        "--approvedTool", "read",
    ]
    if agent:
        command.extend(["--agent", agent])

    try:
        # Pipeline execution capturing output channels securely
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            env=env
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Pipeline error status code: {e.returncode}")
        print(f"Error Diagnostic Info:\n{e.stderr}")
        return ""

if __name__ == "__main__":
    # Run default Claude
    output = run_claude_pipeline("Review python script syntax errors in the current directory.")
    print(f"Output:\n{output}")

    # Run a specific agent
    output = run_claude_pipeline("What is 9 + 27", agent="calculating")
    print(f"Agent Output:\n{output}")
```
