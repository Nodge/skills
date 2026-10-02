#!/usr/bin/env python3
"""Steps and transitions of runbook-task-cycle. Run with --help for the commands."""
from runbook import Runbook, end, parallel

rb = Runbook()

rb.inputs(brief=str, repo=str, checks=str, coder='main', maxFixRounds=2)

rb.executor('main', 'the model the main session runs, through the subagent tool (in Claude Code: Agent, subagent_type '
                    'general-purpose, model set to the session\'s own model), effort high where the tool has it')
rb.executor('light', 'the cheapest fast model, through the subagent tool (in Claude Code: Agent, subagent_type '
                     'general-purpose, model haiku), effort low where the tool has it')
rb.executor('second', 'a model other than the main session\'s, through the subagent tool (in Claude Code: Agent, subagent_type '
                      'general-purpose, model sonnet, or opus if the main session runs Sonnet), effort high where the tool has it')

coder = lambda s: 'second' if s.inputs.coder == 'second' else 'main'  # noqa: E731

rb.start('preflight')

rb.step('preflight', executor='light', prompt='prompts/00-preflight.md',
        reads=['working tree'], writes=['preflight.md'], reply={'clean': bool},
        next=lambda r, s: 'implement' if r.clean else 'ask-dirty')

rb.step('implement', executor=coder, prompt='prompts/01-implement.md', inputs=['checks'],
        reads=['brief.md', 'working tree'], writes=['implement.md'],
        next='checks')

rb.step('checks', executor='light', prompt='prompts/02-checks.md', inputs=['checks'],
        reads=['working tree'], writes=['checks.md'], reply={'passed': bool},
        next=lambda r, s: parallel('review-a', 'review-b') if r.passed
        else ('fix-checks' if not s.done('fix-checks') else end('failed', 'read <run>/checks.md')))

rb.step('fix-checks', executor=coder, prompt='prompts/03-fix-checks.md', inputs=['checks'],
        reads=['brief.md', 'implement.md', 'checks.md', 'working tree'], writes=['fix-checks.md'], reply={'fixed': bool},
        next=lambda r, s: 'checks' if r.fixed else end('failed', 'read <run>/fix-checks.md'))

for letter, executor in (('a', 'main'), ('b', 'second')):
    rb.step(f'review-{letter}', executor=executor, prompt='prompts/04-review.md',
            inputs=['checks', ('id-prefix', letter)],
            reads=['brief.md', 'implement.md', 'fix-checks.md', 'working tree'], writes=[f'review-{letter}.md'],
            reply={'findings': int},
            next='triage')

rb.step('triage', executor='main', prompt='prompts/05-triage.md', after=('review-a', 'review-b'),
        reads=['brief.md', 'review-a.md', 'review-b.md', 'working tree'], writes=['triage.md'], reply={'to_fix': int},
        skip=lambda s: 'polish' if all(getattr(s.reply(f'review-{x}'), 'findings', None) == 0 for x in 'ab') else None,
        next=lambda r, s: 'polish' if r.to_fix == 0 else 'fix')

rb.step('fix', executor=coder, prompt='prompts/06-fix.md', inputs=['checks'],
        reads=['brief.md', 'triage.md', 'verify.md', 'rounds.md', 'working tree'], writes=['fix.md'],
        next='verify')

rb.step('verify', executor='main', prompt='prompts/07-verify.md', inputs=['checks'],
        reads=['triage.md', 'fix.md', 'verify.md', 'working tree'], writes=['verify.md'],
        reply={'unresolved': int, 'passed': bool},
        next=lambda r, s: 'polish' if r.unresolved == 0 and r.passed
        else ('fix' if s.done('verify') < s.inputs.maxFixRounds else 'ask-rounds'))

rb.step('polish', executor=coder, prompt='prompts/08-polish.md', inputs=['checks'],
        reads=['brief.md', 'preflight.md', 'working tree'], writes=['polish.md'],
        reply={'passed': bool},
        next=lambda r, s: end('ready', 'read <run>/polish.md') if r.passed else end('needs_attention', 'read <run>/polish.md'))

rb.human('ask-rounds', writes='rounds.md', choices=['one more round', 'stop'],
         question='Fix rounds are spent. `<run>/verify.md` lists what is unresolved or which checks still fail. '
                  'One more round, or stop here? Anything you write here goes to the coder for the next round.',
         next=lambda choice, s: 'fix' if choice == 'one more round' else end('needs_attention', 'read <run>/verify.md'))

rb.human('ask-dirty', choices=['continue', 'stop'],
         question='The repository already has uncommitted changes, see `<run>/preflight.md`. '
                  'Continue, and they become part of what is implemented on and reviewed, or stop?',
         next=lambda choice, s: 'implement' if choice == 'continue' else end('failed', 'read <run>/preflight.md'))

if __name__ == '__main__':
    raise SystemExit(rb.main())
