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

### Installation

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
