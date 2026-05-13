# Claude Code Installation & Usage Guide

## 1. Installation

### Windows Installation

Run the native installer via PowerShell to install Claude Code:

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

### Python Automated Pipeline (subprocess)

When wrapping Claude within automated pipelines, use the `--p` prompt argument. To prevent the CLI from hanging on interactive confirmation walls, use yes tools or pass inputs directly into standard input channels:

```python
import subprocess
import os

def run_claude_pipeline(prompt_text: str) -> str:
    # Ensure your Anthropic API Key is visible to the process environment
    env = os.environ.copy()

    # Execute non-interactively via argument list
    command = ["claude", "--p", prompt_text]

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
    prompt = "Review python script syntax errors in the current directory."
    pipeline_output = run_claude_pipeline(prompt)
    print(f"Pipeline Execution Output:\n{pipeline_output}")
```
