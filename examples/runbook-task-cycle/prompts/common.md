# Common

Repository: `<repo>`, a git repository with the task's branch checked out. The task brief is `<run>/brief.md`. The rules of the repository are in its instructions file, `<repo>/AGENTS.md` or `<repo>/CLAUDE.md`, if there is one. Follow them, except for anything that would start a procedure the executor constraints below rule out.

"The changes" are everything uncommitted in `<repo>` outside `.agent-runbooks/`, where the run directory may live: `git status` and `git diff HEAD`, plus untracked files read in full. Files the checks write, such as caches and build output, are not part of the changes: leave them and do not report them.

"The checks" are the shell command the launch message gives as `checks`, run from `<repo>` exactly as given. A command that cannot run, because a binary or a dependency is missing, has failed, not been skipped.

A report that mentions the checks has a "Checks" section: the command, its exit code, and the full output when the exit code is not 0.

## Executor constraints

You run one step of a larger procedure. The project's procedures for task cycles, review and commit are not yours to start. Change repository files only as your step instructs, and leave the changes uncommitted unless it instructs a commit. File names in your step's prompt, such as `checks.md`, are names, not paths: the launch message gives a `write <name>: <path>` line for each file you write, and a `read <name>: <path>` line for each file you read, or says it is absent. Write other files only at the paths your launch message gives. Commits, pushes, comments, tickets and other external writes happen only when your step instructs them. Nobody will answer a question. If you cannot proceed, stop and reply `blocked`.

Your final message is the JSON your step's schema describes and nothing else. `status` is `done` when the deliverable exists as described, `failed` when you tried and it does not, `blocked` when you cannot proceed. `failed` and `blocked` carry a one-line `reason`. Other fields are required only with `done`. Explanations and evidence go into your step's output file.
