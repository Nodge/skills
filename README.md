# skills

Agent skills I use in my daily work, in the [Agent Skills](https://agentskills.io) format: a directory with a `SKILL.md`. They work in Claude Code, Codex CLI, opencode and other harnesses that load skills.

| Skill | What it does |
|---|---|
| [agent-runbook-authoring](skills/agent-runbook-authoring) | Write runbooks: multi-step procedures a main session executes through subagents, with transitions computed by a small Python engine instead of reasoned about |

[`examples/`](examples) has a complete runbook, a task cycle with two reviewers, and the files of a real run.

Runbooks pair well with [throng](https://github.com/Nodge/throng-mcp), an MCP server that runs Claude Code, Codex or OpenCode as subagents of each other: any step of a runbook can go to any harness and model.

## Install

Claude Code:

```
/plugin marketplace add Nodge/skills
/plugin install agent-runbook-authoring@nodge-skills
```

Anywhere else: copy `skills/<name>` into your harness's skills directory (`~/.claude/skills`, `~/.codex/skills`, `~/.config/opencode/skills`).

## License

MIT
