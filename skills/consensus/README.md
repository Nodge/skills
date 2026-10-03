# consensus

Think a question through with a second model. `/consensus codex/gpt-6-sol should we keep the monolith?` and the session you are in becomes one participant, the model you named the other.

## The problem

Ask a second model for its opinion and you get a second monologue. Paste it back to the first and the first agrees with it, or the second agrees with the first on the next turn: the models anchor on whatever they read last, and "we both think so" means nothing.

## The approach

Both participants answer the question **independently** first: the second model gets the question and the context, and nothing of the session's own position. Then they exchange messages under one set of rules, [`references/rules.md`](references/rules.md): a position, a reply to every open point with what convinced you or what you checked, new ground only when it can change the answer, and a status with the lists of what is agreed and what is open. Agreement has to state what convinced; conceding to be done keeps the point open. The exchange ends when two consecutive messages say CONVERGED, or when the round budget runs out, and the report to the user is the agreed list, the contested points and what settled them, and whatever stayed open, which is the user's call.

The second model is one [throng](https://github.com/agent-runbooks/throng-mcp) session that keeps its memory across the rounds; its status comes back as structured fields, so the stop condition is a comparison, not a reading of prose.

## Usage

```
/consensus <model> [--rounds N] <question>
```

`<model>` is a throng agent spec, `<harness>/<model>[:<effort>]`, or a code word your own instructions map to one. The budget defaults to 10 rounds, round 1 included; a converging exchange stops long before.

## Requirements

- The throng MCP server, with the harness of the second model installed.
- A session that can run skills and call MCP tools: Claude Code is where this is used; other harnesses that load skills should work.

## Contents

- [`SKILL.md`](SKILL.md): the procedure, for the session that runs it
- [`references/rules.md`](references/rules.md): the rules of the exchange, sent to the second model and binding both
