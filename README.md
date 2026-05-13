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
- Claude Code CLI (see installation below)

### Claude Code Installation

#### Windows

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

#### Linux

```bash
npm install -g @anthropic-ai/claude-code
```

Alternative native installations can be pulled via GitHub Debian Build Releases for specific package management tooling.

#### Initial Authentication

```bash
claude
```

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

#### Python Automated Pipeline (subprocess)

```python
import subprocess
import os

def run_claude_pipeline(prompt_text: str) -> str:
    env = os.environ.copy()
    command = ["claude", "--p", prompt_text]

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
    prompt = "Review python script syntax errors in the current directory."
    pipeline_output = run_claude_pipeline(prompt)
    print(f"Pipeline Execution Output:\n{pipeline_output}")
```

See [docs/claude-code-installation-usage.md](docs/claude-code-installation-usage.md) for the full guide.

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
