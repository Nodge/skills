# Skills

[![skills.sh](https://skills.sh/b/nodge/skills)](https://skills.sh/nodge/skills/consensus)

Agent skills I use in my daily work, in the [Agent Skills](https://agentskills.io) format: a directory with a `SKILL.md`. They work in Claude Code, Codex CLI, opencode and any other harness that loads skills.

## Install

Two ways in. The **Claude Code plugin** installs the skills as a managed bundle that updates when I push. The **[skills CLI](https://github.com/vercel-labs/skills)** copies the skill files into your project or home directory, for any agent, as files you own and can edit. Pick one, otherwise each skill shows up twice.

<details>
<summary><strong>Claude Code plugin</strong></summary>

```bash
claude plugin marketplace add Nodge/skills
claude plugin install consensus@nodge-skills
```

Or from inside a session:

```
/plugin marketplace add Nodge/skills
/plugin install consensus@nodge-skills
```

</details>

<details>
<summary><strong>skills CLI: Claude Code, Codex, opencode, Cursor and others</strong></summary>

```bash
npx skills add Nodge/skills
```

It asks which skills to take and which agents to install them on. Non-interactive, into the user directory of one agent:

```bash
npx skills add Nodge/skills --skill consensus -g -a claude-code -y
```

`npx skills update` pulls my changes later.

</details>

<details>
<summary><strong>By hand</strong></summary>

Copy `skills/<name>` into your harness's skills directory: `~/.claude/skills`, `~/.codex/skills`, `~/.config/opencode/skills`.

</details>

## Skills

### ◆ consensus

Think a question through with a second model: `/consensus codex/gpt-6-sol <question>`. The session you are in and the model you named answer **independently**, then reconcile round by round under one set of rules: reply to every open point with what convinced you or what you checked, concede only when refuted, stop at two CONVERGED in a row. The report is what both stand behind, what was contested, and what stayed open. Needs [throng](https://github.com/agent-runbooks/throng-mcp). [Read more](skills/consensus).

## Runbooks have moved

The runbook skills now live in the [agent-runbooks](https://github.com/agent-runbooks) organization, and the copies here no longer get updates:

- `agent-runbook-authoring` and `runbook-viewer`: [agent-runbooks/skills](https://github.com/agent-runbooks/skills)
- `runbook-task-cycle`: [agent-runbooks/gallery](https://github.com/agent-runbooks/gallery)

If you installed any of them from here, remove that copy and install from the new place, otherwise the skill shows up twice. As a Claude Code plugin:

```bash
claude plugin uninstall runbook-task-cycle@nodge-skills
claude plugin marketplace add agent-runbooks/gallery
claude plugin install runbook-task-cycle@agent-runbooks-gallery
```

With the skills CLI:

```bash
npx skills remove runbook-task-cycle
npx skills add agent-runbooks/gallery --skill runbook-task-cycle
```

The install commands for the other two are in the [agent-runbooks/skills README](https://github.com/agent-runbooks/skills#install).

## License

MIT
