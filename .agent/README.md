# .agent — Coding Agent Setup

This folder contains the configuration, context, and instructions for the AI coding agent powering EagleEye development. It is designed to be agent-agnostic — whether you are using Claude Code, Cursor, GitHub Copilot, Codeium, or any other AI coding assistant, this folder is your starting point.

---

> **Disclaimer**
>
> This setup was not built for one specific agent. Different agents have different capabilities, context windows, tool access, and instruction formats. **Some configurations, prompts, or workflows in this folder will need to be tuned depending on the agent you are using.** The agent working in this repo must be aware of this and should not assume that every instruction here applies to it out of the box. When in doubt, adapt rather than skip.

---

## What Goes Here

- Agent instructions and system prompts
- Task context and project-specific rules
- Workflow definitions the agent should follow
- Any agent-specific config files (e.g., `CLAUDE.md`, `.cursorrules`, etc.)

## Agent Compatibility Notes

| Agent | Notes |
|---|---|
| Claude Code | Reads `CLAUDE.md` for persistent instructions |
| Cursor | Uses `.cursorrules` for repo-level rules |
| GitHub Copilot | Limited repo-level config; rely on comments and prompts |
| Others | Check your agent's docs for how it loads project context |

## Ground Rules for Any Agent Working in This Repo

1. Read the root `README.md` first to understand what EagleEye is.
2. Follow the workflows defined in this folder before taking action.
3. Flag anything in this folder that conflicts with your capabilities — do not silently skip it.
4. When unsure, ask. Do not assume.
