# Claude Code Project Template

**Author:** Chong Kiat Lim

A multi-agent project template with MCP servers and CLI tools for accessing databases and APIs. Designed for use with VS Code Copilot chat agents and Python-based automation.

## Architecture

```
├── agents/              # Python agent scripts (runtime implementations)
├── .claude/agents/      # Chat agents (.agent.md for VS Code Copilot)
├── .claude/skills/      # Skills (on-demand workflows for chat agents)
├── mcp/                 # MCP server implementations (Model Context Protocol)
├── tools/               # CLI tools and standalone scripts
├── config/              # Environment configs and connection settings
├── docs/                # Documentation
└── tests/               # Test suite
```

## Getting Started

### Prerequisites

- Python 3.10+
- VS Code with GitHub Copilot extension (for chat agents)
- Claude Code CLI (requires Node.js and npm — see installation below)

### Claude Code Installation

#### Node.js and npm (required)

Claude Code is an npm package. Install Node.js (v18+) and npm first:

**Windows:**

```powershell
winget install OpenJS.NodeJS.LTS
```

Or download from https://nodejs.org (LTS installer includes npm).

**Linux:**

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

Verify:

```bash
node --version
npm --version
```

#### Windows

```powershell
# Create the missing npm global directory (if it doesn't exist)
New-Item -ItemType Directory -Path "$env:APPDATA\npm" -Force

# Install Claude Code globally
npm install -g @anthropic-ai/claude-code
```

Alternatively, use the native installer:

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

#### Linux

```bash
npm install -g @anthropic-ai/claude-code
```

Alternative native installations can be pulled via GitHub Debian Build Releases for specific package management tooling.

#### Initial Authentication

```bash
claude
```

### Claude Code Settings (`~/.claude/settings.json`)

Configure Claude Code globally via `~/.claude/settings.json` (Windows: `C:\Users\<username>\.claude\settings.json`):

```json
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe",
    "ANTHROPIC_MODEL": "claude-sonnet-4-20250514"
  },
  "theme": "auto"
}
```

For AWS Bedrock or custom endpoints, see [docs/claude-code-installation-usage.md](docs/claude-code-installation-usage.md) for all available settings.

### Project Installation

```bash
# Clone the repository
git clone <repo-url>
cd claude-code-project-template

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp config/.env.example config/.env
```

### Running

```bash
# Start MCP server
python mcp/server.py

# Run a Python agent
python agents/sum_numbers.py 3 5

# Run tests
pytest
```

### Calling an Agent

#### Terminal (Interactive & Non-Interactive)

Launch a direct interactive agent session:

```bash
claude
```

Execute a single instruction non-interactively:

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

> **Why `--p` and `--approvedTool`?** In automated pipelines there is no human to respond to prompts. `--p` makes execution non-interactive (no REPL). `--approvedTool` pre-authorizes tools so Claude doesn't halt at confirmation walls. Together they enable fully unattended execution.

#### Python Automated Pipeline (subprocess)

```python
import subprocess
import os

def run_claude_pipeline(prompt_text: str, agent: str = None) -> str:
    env = os.environ.copy()
    command = [
        "claude", "--p", prompt_text,
        "--approvedTool", "edit",
        "--approvedTool", "bash",
        "--approvedTool", "read",
    ]
    if agent:
        command.extend(["--agent", agent])

    try:
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

See [docs/claude-code-installation-usage.md](docs/claude-code-installation-usage.md) for the full guide.

### Setting Up MCP Servers

MCP (Model Context Protocol) lets Claude access external tools and data sources (GitHub, databases, APIs).

```
Agent ──► Claude Code CLI ──► MCP Server ──► External Service (GitHub, DB, API, etc.)
```

```bash
# Add a remote MCP server (e.g., GitHub)
claude mcp add-json github '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer <YOUR_GITHUB_PAT>"}}'

# Add a local MCP server (e.g., Docker-based)
claude mcp add github -e GITHUB_PERSONAL_ACCESS_TOKEN=<YOUR_GITHUB_PAT> -- docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server

# Add a custom project MCP server
claude mcp add-json mytools '{"command": "python", "args": ["mcp/server.py"], "env": {}}'

# Manage servers
claude mcp list
claude mcp get <server-name>
claude mcp remove <server-name>
```

**Scope options:** `--scope local` (default, you only), `--scope project` (shared via `.mcp.json`), `--scope user` (all projects).

**Verify MCP setup:**

```bash
claude mcp list                  # Confirm server appears and shows "connected"
claude mcp get <server-name>     # Check config + health status for a specific server
```

Inside a Claude Code session, type `/mcp` to see all connected servers and their available tools.

> **Security:** Never hardcode tokens. Use `.env` files and add `.env` / `.mcp.json` to `.gitignore`.

See [docs/claude-code-installation-usage.md](docs/claude-code-installation-usage.md) for full MCP setup details and [docs/mcp-github-server-install-claude.md](docs/mcp-github-server-install-claude.md) for GitHub MCP Server specifics.

## Agent Types

This project supports two kinds of agents:

### Python Agents (`agents/`)

Executable Python scripts for standalone tasks, CI pipelines, and MCP integration.

- One file per agent in `agents/`, with a matching config in `config/`
- Run via terminal: `python agents/<name>.py [args]`

| Agent | Description |
|-------|-------------|
| `hello_world.py` | Prints a hello world greeting |
| `sum_numbers.py` | Adds two numbers together |

### Chat Agents (`.claude/agents/`)

VS Code Copilot personas invoked interactively via `@agent-name` in chat.

- One `.agent.md` file per agent with YAML frontmatter
- Skills defined in `.claude/skills/<name>/SKILL.md`

| Agent | Purpose |
|-------|---------|
| `@texting` | Text generation, greetings, messages |
| `@calculating` | Math operations and arithmetic |
| `@orchestrator` | Delegates to specialist agents |

### Skills

Reusable workflows that chat agents can invoke:

| Skill | Description |
|-------|-------------|
| `/hello-world` | Print a hello world greeting |
| `/sum` | Calculate the sum of two numbers |

## Adding New Components

| Component | Steps |
|-----------|-------|
| **Python Agent** | Create `agents/<name>.py` + `config/<name>.yaml` |
| **Chat Agent** | Create `.claude/agents/<name>.agent.md` with YAML frontmatter |
| **Skill** | Create `.claude/skills/<name>/SKILL.md` |
| **MCP Tool** | Implement in `mcp/`, register in server, add tool description |
| **CLI Tool** | Create script in `tools/`, make it independently testable |

## Conventions

- All external connections (databases, APIs) are configured in `config/`
- Secrets go in `.env` files (never committed to version control)
- MCP tools must have clear, descriptive names and docstrings for agent discovery
- CLI tools in `tools/` are standalone — they work both independently and when invoked by agents
- Prefer composing existing tools over creating new ones
