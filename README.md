# Skills

[![skills.sh](https://skills.sh/b/nodge/skills)](https://skills.sh/nodge/skills/agent-runbook-authoring)

Agent skills I use in my daily work, in the [Agent Skills](https://agentskills.io) format: a directory with a `SKILL.md`. They work in Claude Code, Codex CLI, opencode and any other harness that loads skills.

## Install

Two ways in. The **Claude Code plugin** installs the skills as a managed bundle that updates when I push. The **[skills CLI](https://github.com/vercel-labs/skills)** copies the skill files into your project or home directory, for any agent, as files you own and can edit. Pick one, otherwise each skill shows up twice.

<details>
<summary><strong>Claude Code plugin</strong></summary>

```bash
claude plugin marketplace add Nodge/skills
claude plugin install agent-runbook-authoring@nodge-skills
```

Or from inside a session:

```
/plugin marketplace add Nodge/skills
/plugin install agent-runbook-authoring@nodge-skills
```

</details>

<details>
<summary><strong>skills CLI: Claude Code, Codex, opencode, Cursor and others</strong></summary>

```bash
npx skills add Nodge/skills
```

It asks which skills to take and which agents to install them on. Non-interactive, into the user directory of one agent:

```bash
npx skills add Nodge/skills --skill agent-runbook-authoring -g -a claude-code -y
```

`npx skills update` pulls my changes later.

</details>

<details>
<summary><strong>By hand</strong></summary>

Copy `skills/<name>` into your harness's skills directory: `~/.claude/skills`, `~/.codex/skills`, `~/.config/opencode/skills`.

</details>

## Skills

### agent-runbook-authoring

Writes **runbooks**: procedures an agent session runs through subagents. Implement, run the checks, review with two models, triage, fix, verify, ask a human when the fix rounds run out. The steps are prompt files, the transitions are a few lines of Python on a small engine, and the orchestrator never reasons about what comes next. [Read more](skills/agent-runbook-authoring).

[`examples/`](examples) has a complete runbook for one coding task with two independent reviewers, a tiny project to try it on, and the files of a real run.

## License

MIT
