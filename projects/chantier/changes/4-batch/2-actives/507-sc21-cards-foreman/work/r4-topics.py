import json

P = 'C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next/topics.json'
raw = open(P, 'rb').read().decode('utf-8')
d = json.loads(raw)
eol = '\r\n' if '\r\n' in raw else '\n'


def dump(o):
    return (json.dumps(o, indent=2, ensure_ascii=False) + '\n').replace('\n', eol)


print('roundtrip', dump(d) == raw)

COS = ['chief-of-staff']
STEER = ['foreman', 'chief-of-staff']
TALK = ['chief-of-staff', 'griller']
DRIVERS = ['foreman', 'chief-of-staff', 'cr-driver', 'stack-driver', 'release-driver']
T = d['topics']


def add(name, readings, roles, trigger, rare=False):
    assert name not in T, name
    row = {'readings': readings, 'roles': roles, 'trigger': trigger}
    if rare:
        row['review_by'] = '0.16.0'
    T[name] = row


def claude(name, roles, trigger, rare=False, copilot='host-claude-only'):
    add(name, [{'claude': f'topics/{name}.md', 'copilot': f'topics/{copilot}.md'}], roles, trigger, rare)


T['sync']['readings'].append('sync-checkout.md')
add('sync-offer', ['topics/sync-offer.md'], STEER, '`sync pending` for 3 minutes')
claude('host-configuration', COS, 'a question on the host settings the user sets', copilot='host-configuration-copilot')
claude('host-allow-rules', COS, 'how an allow rule matches')
claude('host-allow-broad', COS, 'a broad rule, a moved path, a rule the base set leaves out')
claude('host-allow-extra', COS, 'a release or a grant that needs rules the base set lacks')
claude('host-allow-add', COS, 'the host refused your edit of the settings, or the file is not JSON')
claude('host-allow-add-lines', COS, 'the command lines to give for the allow rules')
claude('host-allow-not-add', COS, 'a rule auto mode drops, a rule not to propose')
claude('host-refused', STEER, 'a command the host refuses whatever the rules')
claude('host-auto-mode', DRIVERS, 'auto mode, a classifier refusal')
claude('host-auto-mode-steering', STEER, "the steering session's push in auto mode")
claude('host-auto-mode-trials', COS, 'a trial before the go', True)
claude('host-compact', ['foreman', 'chief-of-staff', 'griller'], 'a compaction, a compacting setting', copilot='host-compact-copilot')
claude('host-write-guard', DRIVERS, 'a write refused by the plugin, a `writes:` line')
claude('host-write-guard-shell', DRIVERS, 'a shell write refused by the plugin')
claude('host-sessions', COS, "a session to start, a session's class", copilot='host-sessions-copilot')
claude('host-sessions-more', COS, 'two sessions of one repository', True)
claude('host-remote', COS, 'a session to start from Remote Control', True)
claude('host-surfaces', TALK, 'where the user is, the options that fit')
claude('host-subagent-signs', DRIVERS, 'what the host says of a subagent')
claude('host-foreman-worktree', STEER, 'a Foreman started in a worktree', True)
claude('host-reuse-foreman', COS, 'a last Foreman session still there at a new batch', True)
claude('host-for-you', TALK, 'a step that is the user\'s')
claude('host-for-you-sessions', COS, 'a "For you" block for a reused Foreman or a new session', True)
claude('host-auto-fix', STEER, 'an Auto-fix event', True)
claude('host-turn-end', STEER, "the host's notice of a turn's end")
claude('host-driver-silence', STEER, 'a silent Driver')
claude('host-heartbeat', STEER, 'the heartbeat to arm', copilot='host-heartbeat-copilot')
add('init-checks', ['topics/init-checks.md'], COS, "the tour's checks of the gates", True)
add('init-tools', ['topics/init-tools.md'], COS, "the tour's checks of the allow rules and the forge's tools", True)
add('release-evidence', ['topics/release-evidence.md', 'topics/release-thread.md'], ['release-driver'], 'the pictures of the notes, the announcement thread')
add('status-notes', ['topics/status-notes.md', 'topics/status-notes-more.md'], COS, "a report's conditional Notes lines")

open(P, 'wb').write(dump(d).encode('utf-8'))
print(len(T))
