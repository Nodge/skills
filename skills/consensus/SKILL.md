---
name: consensus
description: "Think a question through together with a second model: both form positions independently, then reconcile them round by round until they agree or the crux is clear."
argument-hint: "<model> [--rounds N] <question>"
disable-model-invocation: true
---

# consensus

Needs the [throng](https://github.com/Nodge/throng-mcp) MCP server: B lives in a thronglet.

You are participant **A**. The second model, **B**, is one thronglet session that keeps its own context across the whole consultation: `run_thronglet` opens it, `send_message` carries every later message into it. Your messages to B are the prompts; B's replies are its messages, with the status as structured fields. You follow the same rules as B: [`references/rules.md`](references/rules.md) goes to B in the opening prompt and binds both of you.

## Inputs

From `$ARGUMENTS`: the first word names B's model, as a throng agent spec `<harness>/<model>[:<effort>]` (`codex/gpt-6-sol`, `claude/opus:max`) or as a code word your instructions map to one. No effort given: `:high`. A word you cannot resolve: ask, do not guess. `--rounds N`, anywhere, sets the budget; default 10, round 1 included. The rest is the question, verbatim.

B always runs through throng, whatever its vendor, even the one that runs you. B on your own model shares your blind spots: say so in one line and proceed.

Context for B carries facts, not assessments: files under discussion, constraints the user stated, what was tried. Your view goes into your messages.

## Calls to B

Every call to B passes this `schema`, so B's status comes back as fields and its message body as `message`:

```json
{
  "type": "object",
  "properties": {
    "message": { "type": "string", "description": "The message: position, reply, new ground, per the rules" },
    "status": { "enum": ["OPEN", "CONVERGED"] },
    "agreed": { "type": "array", "items": { "type": "string" } },
    "open": { "type": "array", "items": { "type": "string" } },
    "parking_lot": { "type": "array", "items": { "type": "string" } }
  },
  "required": ["message", "status", "agreed", "open", "parking_lot"]
}
```

Round 1: `mcp__throng__run_thronglet`, `agent` = the resolved spec, `cwd` = your cwd, `description` = `consensus: B (<spec>)`, `background: true`; keep the `session_id`. Rounds 2 and on: `mcp__throng__send_message` with that `session_id`, synchronous. A failed call: `structured_missing` / `structured_invalid` get one `send_message` with the correction; any other error, one retry; then end with a Conclusion that says what failed.

## Round 1: independent positions

1. Launch B in the background. The prompt carries the rules, the question and the context, and nothing of your position:

   ```
   You are participant B in a consultation: two agents answer the same question independently, then reconcile over several rounds of messages. The rules below bind you. This is round 1: form your own position from the question, the context and whatever you check in the working tree. Submit your message in the `message` field and your status in the other fields.

   <rules>
   <references/rules.md, verbatim>
   </rules>

   Question: <the question, verbatim>

   Context: <facts B lacks; "none" if nothing>

   You are running as a subagent of another agent session.
   ```

2. While B works, form your `Round 1 — A` from the question and your own checks, and write it in your reply to the user, per the rules.
3. `mcp__throng__wait_thronglet` on the session. The result holds B's round 1.

## Rounds 2 and on

1. Write your `Round N — A` per the rules. In round 2 open the message with your `Round 1 — A` verbatim, so B sees the position you formed independently, then the round-2 message. If B's last status was CONVERGED and yours is too: stop.
2. Send it with `send_message`, ending with:

   ```
   Reply as `Round N — B`: your message in the `message` field, your status in the other fields.
   ```

3. Read B's reply. If your status was CONVERGED and B's is too: stop. Otherwise, next round while the budget lasts.

## Ending

Report to the user, in the user's language: the agreed answer, which is the last `agreed` list and nothing beyond it; the points that were contested and what settled them; the `open` list if the budget ran out, with any new ground from B's final message added to it. What is still Open is the user's call, not yours to resolve by picking a side.
