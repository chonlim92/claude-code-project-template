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

**Path Configuration:** If Git is not globally registered, add its fallback location inside your `~/.claude/settings.json`:

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

## 3. Claude Code Settings (`~/.claude/settings.json`)

Claude Code uses its own settings file at `~/.claude/settings.json` (user home directory) for global configuration.

### Settings File Location

| OS | Path |
|----|------|
| **Windows** | `C:\Users\<username>\.claude\settings.json` |
| **Linux** | `~/.claude/settings.json` |
| **macOS** | `~/.claude/settings.json` |

### Configuration

The settings file uses JSON format with the following keys:

```json
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe",
    "ANTHROPIC_MODEL": "claude-sonnet-4-20250514"
  },
  "theme": "auto"
}
```

### Environment Variables (`env`)

The `env` object passes environment variables to the Claude Code runtime. Common variables:

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_GIT_BASH_PATH` | Path to Git Bash (Windows only, if Git is not on PATH) |
| `ANTHROPIC_API_KEY` | Anthropic API key (if not using `claude` login) |
| `ANTHROPIC_MODEL` | Default model to use (e.g., `claude-sonnet-4-20250514`, `claude-opus-4-6`) |
| `CLAUDE_CODE_USE_BEDROCK` | Set to `1` to use AWS Bedrock as the provider |
| `ANTHROPIC_BEDROCK_BASE_URL` | Custom Bedrock endpoint URL |
| `AWS_BEARER_TOKEN_BEDROCK` | Bearer token for Bedrock authentication |

### Theme

| Value | Description |
|-------|-------------|
| `"auto"` | Follow system theme |
| `"dark"` | Dark mode |
| `"light"` | Light mode |

### Example: Direct Anthropic API

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "<YOUR_ANTHROPIC_API_KEY>",
    "ANTHROPIC_MODEL": "claude-sonnet-4-20250514"
  },
  "theme": "auto"
}
```

### Example: AWS Bedrock Provider

```json
{
  "env": {
    "CLAUDE_CODE_USE_BEDROCK": "1",
    "ANTHROPIC_BEDROCK_BASE_URL": "<YOUR_BEDROCK_ENDPOINT_URL>",
    "AWS_BEARER_TOKEN_BEDROCK": "<YOUR_BEARER_TOKEN>",
    "ANTHROPIC_MODEL": "claude-opus-4-6"
  },
  "theme": "auto"
}
```

> **Security:** The `~/.claude/settings.json` file is local to your machine and not committed to version control. Replace all `<YOUR_...>` placeholders with your actual values. Do NOT copy these values into project-level files that may be committed.

## 4. CLI Configuration & Files

Claude Code stores its configuration across several files and directories. Here is the full layout:

### Configuration File Map

| File / Directory | Location | Purpose |
|-----------------|----------|---------|
| `settings.json` | `~/.claude/settings.json` | Global settings (env vars, theme, model) |
| `.mcp.json` (user) | `~/.claude/.mcp.json` | User-global MCP servers (`--scope user`) |
| `.mcp.json` (local) | `<project>/.claude/.mcp.json` | Per-project MCP servers, gitignored (`--scope local`) |
| `.mcp.json` (project) | `<project>/.mcp.json` | Shared project MCP servers, committed (`--scope project`) |
| `CLAUDE.md` | `<project>/CLAUDE.md` | Project instructions, auto-discovered by Claude |
| `AGENTS.md` | `<project>/AGENTS.md` | Project guidelines, auto-discovered by Claude |
| `.agent.md` | `<project>/.claude/agents/*.agent.md` | Chat agent definitions |
| `SKILL.md` | `<project>/.claude/skills/<name>/SKILL.md` | Skill definitions |
| `history.jsonl` | `~/.claude/history.jsonl` | CLI session history |
| `sessions/` | `~/.claude/sessions/` | Persisted session data |
| `projects/` | `~/.claude/projects/` | Per-project state |

### CLI Authentication

```bash
# Log in to Anthropic
claude auth login

# Check authentication status
claude auth status

# Log out
claude auth logout
```

### CLI Session Management

```bash
# Start interactive session
claude

# Start with a specific model
claude --model claude-opus-4-6

# Continue most recent session
claude --continue

# Resume a specific session (interactive picker)
claude --resume

# Resume by session ID
claude --resume <session-id>

# Name a session for easy identification
claude --name "my-feature-work"
```

### CLI Flags Reference

| Flag | Description |
|------|-------------|
| `-p, --print` | Non-interactive mode: print response and exit |
| `--agent <name>` | Run a specific `.agent.md` agent |
| `--model <model>` | Override model for this session |
| `--allowedTools <tools>` | Pre-approve tools (space-separated) |
| `--disallowedTools <tools>` | Block specific tools |
| `--permission-mode <mode>` | Permission mode (`default`, `plan`, `auto`, `bypassPermissions`) |
| `--max-budget-usd <amount>` | Spending cap for API calls (with `--print`) |
| `--output-format <format>` | Output format: `text`, `json`, `stream-json` (with `--print`) |
| `--system-prompt <prompt>` | Override the system prompt |
| `--append-system-prompt <prompt>` | Append to the default system prompt |
| `--add-dir <dirs>` | Additional directories to allow tool access to |
| `--mcp-config <configs>` | Load MCP servers from JSON files |
| `-c, --continue` | Continue most recent conversation |
| `-r, --resume [id]` | Resume a conversation by session ID |
| `-n, --name <name>` | Set display name for the session |
| `--effort <level>` | Effort level: `low`, `medium`, `high`, `xhigh`, `max` |
| `--verbose` | Enable verbose output |
| `-d, --debug` | Enable debug mode |
| `-v, --version` | Show version |

### CLI Subcommands

```bash
# Authentication
claude auth login|logout|status

# MCP server management
claude mcp add|add-json|list|get|remove <server>

# Agent management
claude agents

# Update Claude Code
claude update

# Health check
claude doctor
```

## 5. Setting Up MCP Servers

MCP (Model Context Protocol) allows Claude to access external tools and data sources. MCP servers expose tools that agents can discover and invoke.

### How MCP Works

```
Agent ──► Claude Code CLI ──► MCP Server ──► External Service (GitHub, DB, API, etc.)
```

- MCP servers are registered with Claude Code and run as background processes
- Each server exposes one or more tools with descriptions
- Agents discover and call these tools automatically based on task needs

### Managing MCP Servers

```bash
# List all configured MCP servers
claude mcp list

# Get details of a specific server
claude mcp get <server-name>

# Remove a server
claude mcp remove <server-name>
```

### Scope Options

When adding an MCP server, use `--scope` to control where the config is stored:

| Scope | Description |
|-------|-------------|
| `local` (default) | Available only to you in the current project |
| `project` | Shared with everyone in the project (stored in `.mcp.json`) |
| `user` | Available to you across all projects |

### `.mcp.json` File Locations

| Scope | Location |
|-------|----------|
| `local` (default) | `<project>/.claude/.mcp.json` (project's `.claude/` folder, gitignored) |
| `project` | `<project>/.mcp.json` (project root, committed & shared) |
| `user` | `~/.claude/.mcp.json` (global, in the user's `.claude/` folder) |

Example: `claude mcp add-json myserver '...' --scope user`

### Adding a Remote MCP Server (Streamable HTTP)

For servers hosted remotely (e.g., GitHub MCP Server):

```bash
claude mcp add-json <server-name> '{"type":"http","url":"<SERVER_URL>","headers":{"Authorization":"Bearer <TOKEN>"}}'
```

**Example — GitHub MCP Server:**

```bash
claude mcp add-json github '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer <YOUR_GITHUB_PAT>"}}'
```

> **Windows / CLI note**: `claude mcp add-json` may return `Invalid input` when adding an HTTP server. If that happens, use the legacy format:
> ```powershell
> $pat = "<YOUR_GITHUB_PAT>"
> claude mcp add github --transport http https://api.githubcopilot.com/mcp/ -H "Authorization: Bearer $pat"
> ```

### Adding a Local MCP Server (stdio)

For servers running locally via Docker or a binary:

**With npx:**

```bash
claude mcp add github -e GITHUB_PERSONAL_ACCESS_TOKEN=<YOUR_GITHUB_PAT> -e GITHUB_API_URL=<YOUR_GIT_DOMAIN> -- npx -y @modelcontextprotocol/server-github
```

**With Docker:**

```bash
claude mcp add <server-name> -e API_TOKEN=<YOUR_TOKEN> -- docker run -i --rm -e API_TOKEN <image>
```

**Example — GitHub MCP Server (Docker):**

```bash
claude mcp add github -e GITHUB_PERSONAL_ACCESS_TOKEN=<YOUR_GITHUB_PAT> -- docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server
```

**With a local binary:**

```bash
claude mcp add-json <server-name> '{"command": "<binary>", "args": ["stdio"], "env": {"API_TOKEN": "<YOUR_TOKEN>"}}'
```

### Adding a Custom Project MCP Server

To add your own MCP server defined in the `mcp/` directory:

```bash
claude mcp add-json mytools '{"command": "python", "args": ["mcp/server.py"], "env": {}}'
```

### Configuring MCP for Claude Desktop (Not in Scope)

> **Note:** Claude Desktop is a separate application and is **not in scope** for this repository. The `mcpServers` key in a JSON config file is a **Claude Desktop-only** concept. Claude Code CLI uses `.mcp.json` files managed via `claude mcp add` commands (see above). Do not confuse the two.

Claude Desktop uses a JSON config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Example config:

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_GITHUB_PAT>"
      }
    }
  }
}
```

### Security Best Practices

- **Never hardcode tokens** — use environment variables or `.env` files
- Add `.env` and `.mcp.json` to `.gitignore`
- Use scoped Personal Access Tokens with minimum required permissions
- Review MCP server tool descriptions to understand what access you're granting

### Verification & Troubleshooting

```bash
# Verify server is configured
claude mcp list
claude mcp get <server-name>

# If server isn't working
claude mcp remove <server-name>   # Remove and re-add
```

**Common issues:**
- **Auth failed**: Check token has correct scopes and hasn't expired
- **Docker issues**: Ensure Docker Desktop is running; try `docker pull <image>`
- **Tools not showing**: Restart Claude Code, check `/mcp` command, validate JSON syntax
- **Windows path issues**: Use forward slashes or escaped backslashes in JSON

See [mcp-github-server-install-claude.md](mcp-github-server-install-claude.md) for detailed GitHub MCP Server setup.
