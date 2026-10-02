# Preflight

Run `git status --porcelain -- . ':(exclude).agent-runbooks'` in `<repo>`. Keep repository files unchanged.

Write `preflight.md`: the command, its exit code, stdout and stderr. A non-zero exit code, `<repo>` not being a git repository included, is `failed` with the reason.

`clean` is true when the output is empty: no changed, staged or untracked files outside the run directory.

## Reply schema

```json
{
  "type": "object",
  "oneOf": [
    {
      "properties": {
        "status": { "const": "done" },
        "clean": { "type": "boolean" }
      },
      "required": ["status", "clean"],
      "additionalProperties": false
    },
    {
      "properties": {
        "status": { "enum": ["failed", "blocked"] },
        "reason": { "type": "string", "minLength": 1 }
      },
      "required": ["status", "reason"],
      "additionalProperties": false
    }
  ]
}
```
