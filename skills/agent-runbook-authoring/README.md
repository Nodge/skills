# agent-runbook-authoring

A skill for writing **runbooks**: procedures an agent session executes step by step through subagents. Implement, run the checks, review with two models, triage, fix, verify, ask a human when the fix rounds run out.

## The problem

Write such a procedure as prose in a `SKILL.md`, and the orchestrating model drifts exactly where the procedure branches. It counts loop rounds wrong, takes a failed reply for a done one, reads files it was told to leave alone, pastes artifacts into its context until compaction eats the run. A workflow script fixes the branching but needs a runner, and the steps stop being prompts you can read and edit.

## The approach

A runbook is an ordinary skill. The steps are prompt files. Transitions live in `flow.py`, a few dozen lines of Python on top of `runbook.py`, a small engine copied into every runbook. The orchestrator never reasons about what comes next: it launches what `flow.py` prints, waits, and copies each executor's JSON reply back into `flow.py`. Steps hand work to each other through files in a run directory, so the orchestrator's context stays small, and an interrupted run resumes from `state.json`.

```python
rb.step('checks', executor='light', prompt='prompts/02-checks.md',
        writes=['checks.md'], reply={'passed': bool},
        next=lambda r, s: parallel('review-a', 'review-b') if r.passed
        else ('fix-checks' if not s.done('fix-checks') else end('failed', 'read <run>/checks.md')))
```

A finished runbook is self-sufficient: it runs where this skill is not installed.

## In practice

TODO: runs, end statuses, orchestrator deviations per run.

## Limits

- The orchestrating session must be able to launch subagents and learn when they finish.
- The engine computes transitions. Whether the orchestrator follows the execution rules is still up to the model; `progress.md` and the review checklist make deviations visible, not impossible.
- Tested only with Claude Code as the orchestrator. Other harnesses that meet the first point will likely work; I haven't tried them.

## Contents

- [`SKILL.md`](SKILL.md): how to write a runbook, for the agent
- [`references/template.md`](references/template.md): the shape of a runbook and the sections copied into it
- [`references/flow-language.md`](references/flow-language.md): the `flow.py` API
- [`references/review-checklist.md`](references/review-checklist.md): cold read, checklist, run review
- [`references/runbook.py`](references/runbook.py): the engine, Python 3.10+, no dependencies
- [`CHANGELOG.md`](CHANGELOG.md): engine versions
