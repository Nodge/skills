Two participants, A and B, answer the same question and reconcile their answers by exchanging messages. The transcript is the conversation itself; nothing is written down elsewhere. A round is A's message, then B's. The goal is one answer both stand behind, not a win. Neither participant has authority over the other.

The consultation leaves nothing behind: an experiment to test a hypothesis (a scratch test, a script, a benchmark) is fine, and its code and output go into the message, since the file itself is removed afterwards; the working tree ends the consultation as it began. The code under discussion is not changed. Messages are written in the language of the question.

## A message

Titled `Round N — A` or `Round N — B`, with these parts:

1. **Position.** Your current answer to the question, in a few sentences. When it changed since your last message: what you held, and what refuted it.
2. **Reply to the other's last message.** Each Open item and each new claim gets one of: *agree*, with what convinced you or what you checked; *disagree*, with the reason and the evidence; *unclear*, with the question you need answered. What is already Agreed needs no reply.
3. **New ground**, only when it can change the answer: a consideration neither of you has raised, a check you ran, a case that breaks the current answer. Restating or refining an agreed point is not new ground.
4. **Status**, last: `Status: OPEN | CONVERGED`; `Agreed`, the points both participants have accepted; `Open`, the disagreements and unanswered questions; `Parking lot`, side issues worth noting, out of scope here. Each a list, empty when there is nothing.

Carry the lists forward from the previous message and edit them. A point enters Agreed in the message of the participant who accepts it, never in the message of the one who made it. A new disagreement joins Open.

Round 1 has no reply part: Agreed is empty, Open lists your own doubts, Status is OPEN. Round 2 — A builds the first shared lists from both round-1 messages.

## Substance

- Evidence over assertion. When the question touches code or data, check it and cite what you checked (file:line, command and its output, the document). A claim you cannot back is a hypothesis, and you say so.
- Agreement states what convinced you. "Agreed" alone, or agreeing to be done, does not count; when you would concede only to finish, keep the point Open and say the disagreement remains.
- Address the strongest form of the other's argument. Repeating your position in other words is not a reply.
- Building on a claim you have not understood or could not verify is worse than a question: mark it *unclear* and ask.
- Stay on the question. A related issue goes to the parking lot.

## Convergence

`Status: CONVERGED` means: Open is empty and this message adds no new ground. A message that adds new ground stays OPEN so the other can review it. The consultation ends when two consecutive messages, in either order, are CONVERGED, or when the round budget runs out, in which case the last Open list is the result.
