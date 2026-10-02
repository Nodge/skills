# Examples

## runbook-task-cycle

A runbook written with [agent-runbook-authoring](../skills/agent-runbook-authoring): one coding task end to end in a git repository. A coder implements the brief, a cheap model runs the checks, two different models review independently, an arbiter triages their findings against the code, the coder fixes what is worth fixing, a verifier checks the fixes, and a last pass cleans up comments and wording. The human is asked only when the repository is dirty at the start or the fix rounds run out. The changes stay uncommitted.

```
SKILL.md        what the orchestrator reads: inputs, execution rules, end of run
flow.py         steps and transitions
runbook.py      the engine, a copy of the skill's
prompts/        common.md and one prompt per step
smoke/textkit   a tiny Python project to try it on
```

[`runs/20261002-slugify-max-length`](runs/20261002-slugify-max-length) is a real run on the fixture: `progress.md`, `state.json`, every step's output, and the resulting `changes.diff`. Step outputs are numbered by launch, so the directory reads top to bottom: one reviewer found nothing, the other found that `max_length` cut words like `3.14` in the middle, triage confirmed it, the coder fixed it, and the verifier checked the fix, fuzzing included.

### Try it

Copy `runbook-task-cycle` into your skills directory (`~/.claude/skills/` for Claude Code), then make a repository from the fixture:

```bash
cp -r runbook-task-cycle/smoke/textkit /tmp/textkit && cd /tmp/textkit && git init -q && git add -A && git commit -qm init
```

Start a session in `/tmp/textkit` and ask: "Run runbook-task-cycle: add an optional `max_length` to `slugify`, cut on a word boundary; checks `python3 -m unittest`."

### Adapting it

The executors in `flow.py` are described for Claude Code. In another harness, rewrite their descriptions to name its subagent tool and models.

The second reviewer is a different model of the same vendor. A model from another vendor catches more, and [throng](https://github.com/Nodge/throng-mcp) makes that one line. It is an MCP server that runs Claude Code, Codex or OpenCode as a subagent of any of them and returns the agent's final message, which is the shape a runbook executor already has. `wait_thronglet` waits for an hour-long step without a shell timeout, and parallel steps run as background thronglets collected one by one. No relay subagent in between:

```python
rb.executor('second', 'GPT through throng: run_thronglet with agent codex/gpt-6-sol:high, cwd = repo')
```

Any step can go the same way: a Codex coder, an OpenCode model as a cheap checker, a Claude reviewer when the orchestrator runs in Codex.
