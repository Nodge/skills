# Skills

[![skills.sh](https://skills.sh/b/nodge/skills)](https://skills.sh/nodge/skills/agent-runbook-authoring)

Agent skills I use in my daily work, in the [Agent Skills](https://agentskills.io) format: a directory with a `SKILL.md`. They work in Claude Code, Codex CLI, opencode and any other harness that loads skills.

| Skill | What it does |
|---|---|
| [agent-runbook-authoring](skills/agent-runbook-authoring) | Write runbooks: multi-step procedures a main session executes through subagents, with transitions computed by a small Python engine instead of reasoned about |

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

## Runbooks

A runbook is a procedure an agent session runs through subagents: implement, run the checks, review with two models, triage, fix, verify, ask a human when the fix rounds run out.

Write such a procedure as prose in a `SKILL.md`, and the orchestrating model drifts exactly where the procedure branches. It counts loop rounds wrong, takes a failed reply for a done one, reads files it was told to leave alone, pastes artifacts into its context until compaction eats the run. A workflow script fixes the branching, but it needs a runner, and the steps stop being prompts you can read and edit.

[agent-runbook-authoring](skills/agent-runbook-authoring) takes a third route. A runbook stays an ordinary skill, and the steps stay prompt files. Transitions live in `flow.py`, a few dozen lines on top of a small engine copied into every runbook. The orchestrator never reasons about what comes next: it launches what `flow.py` prints, waits, and copies each executor's JSON reply back. Steps hand work to each other through files in a run directory, so the orchestrator's context stays small, and an interrupted run resumes from `state.json`.

```python
rb.step('checks', executor='light', prompt='prompts/02-checks.md',
        writes=['checks.md'], reply={'passed': bool},
        next=lambda r, s: parallel('review-a', 'review-b') if r.passed
        else ('fix-checks' if not s.done('fix-checks') else end('failed', 'read <run>/checks.md')))
```

A finished runbook is self-sufficient: it runs where the skill is not installed.

### Examples

[`examples/`](examples) has [`runbook-task-cycle`](examples/runbook-task-cycle), a complete runbook for one coding task with two independent reviewers, a tiny project to try it on, and [the files of a real run](examples/runs/20261002-slugify-max-length): `progress.md`, `state.json`, every step's output, the resulting diff.

### Mixing models

Runbooks pair well with [throng](https://github.com/Nodge/throng-mcp), an MCP server that runs Claude Code, Codex or OpenCode as subagents of each other. Any step of a runbook can go to any harness and model: a Codex coder, an OpenCode model as a cheap checker, a reviewer from another vendor that catches what the first one missed.

## License

MIT
