# Project Instructions

## Overview

Multi-agent project template with MCP servers and CLI tools for accessing databases and APIs.

## Architecture

```
├── agents/              # Python agent scripts (runtime implementations)
├── .claude/agents/      # Chat agents (.agent.md for VS Code Copilot)
├── .claude/skills/      # Skills (on-demand workflows for chat agents)
├── mcp/                 # MCP server implementations
├── tools/               # CLI tools and scripts
├── config/              # Environment and connection configs
└── docs/                # Documentation
```

## Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp config/.env.example config/.env
```

### Running Agents
```bash
# Start MCP server
python mcp/server.py

# Run agent with CLI tools
python agents/main.py --config config/agent.yaml
```

## Conventions

- Python agents: one file per agent in `agents/`, with matching config in `config/`
- Chat agents: one `.agent.md` per agent in `.claude/agents/`
- Skills: one folder per skill in `.claude/skills/<name>/SKILL.md`
- MCP servers expose tools via the Model Context Protocol standard
- CLI tools in `tools/` are standalone scripts that can also be invoked by agents
- All external connections (databases, APIs) are configured in `config/`
- Secrets go in `.env` files (never committed)

## Chat Agents

| Agent | Purpose |
|-------|----------|
| `@texting` | Text generation, greetings, messages |
| `@calculating` | Math operations and arithmetic |
| `@orchestrator` | Delegates to specialist agents |

## Agent Guidelines

- When adding a Python agent, create both the definition in `agents/` and config in `config/`
- When adding a chat agent, create `.claude/agents/<name>.agent.md` with YAML frontmatter
- Use `tools: [agent]` and `agents: [name1, name2]` in frontmatter for multi-agent delegation
- MCP tools should have clear descriptions for agent discovery
- Prefer composing existing tools over creating new ones
- Test tool access independently before integrating with agents
