# Project Guidelines

## Overview

Multi-agent project template with MCP servers and CLI tools for accessing databases and APIs.

## Architecture

```
agents/              → Python agent scripts (runtime implementations)
.claude/agents/      → Chat agents (.agent.md for VS Code Copilot)
.claude/skills/      → Skills (on-demand workflows for chat agents)
mcp/                 → MCP server implementations (Model Context Protocol)
tools/               → CLI tools and standalone scripts
config/              → Environment configs and connection settings
docs/                → Documentation
```

## Agent Types

This project has two kinds of agents:

| | Python Agents (`agents/`) | Chat Agents (`.claude/agents/`) |
|---|---|---|
| **What** | Executable Python scripts | VS Code Copilot personas |
| **Format** | `.py` files | `.agent.md` (Markdown + YAML frontmatter) |
| **Config** | Matching YAML in `config/` | Self-contained in frontmatter (`tools`, `model`) |
| **Run via** | `python agents/<name>.py` | `@agent-name` in Copilot chat |
| **Use case** | Standalone tasks, CI, pipelines, MCP integration | Interactive AI assistant in editor |
| **Skills** | N/A | `.claude/skills/<name>/SKILL.md` (slash commands) |

### Python Agents
- Located in `agents/`, one file per agent
- Configuration in `config/<agent_name>.yaml`
- Run from terminal or invoked by other systems
- Example: `python agents/sum_numbers.py 3 5`

### Chat Agents
- Located in `.claude/agents/`, one `.agent.md` per agent
- Configuration is in the YAML frontmatter (tools, model, description)
- Invoked via `@agent-name` in VS Code Copilot chat
- Skills (slash commands) in `.claude/skills/<name>/SKILL.md`
- Example: `@calculating what is 9+27`

## Build and Test

```bash
pip install -r requirements.txt        # Install dependencies
cp config/.env.example config/.env     # Configure environment
python mcp/server.py                   # Start MCP server
python agents/main.py --config config/agent.yaml  # Run agent
```

## Conventions

- One agent per file in `agents/`, with a matching config in `config/`
- MCP tools must have clear, descriptive names and docstrings for agent discovery
- CLI tools in `tools/` are standalone — they work both independently and when invoked by agents
- All database/API connections configured via `config/` (never hardcoded)
- Secrets in `.env` files — never committed to version control

## Key Patterns

- **Adding an agent**: Create definition in `agents/` + config in `config/`
- **Adding an MCP tool**: Implement in `mcp/`, register in server, add tool description
- **Adding a CLI tool**: Create script in `tools/`, make it independently testable
- **Composability**: Prefer reusing existing tools over creating new ones
