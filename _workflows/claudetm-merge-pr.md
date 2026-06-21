---
title: claudetm — merge PRs to prod
tags: [ops, eng, workflow]
updated: 2026-06-11
status: draft
---

# claudetm (claude-task-master)

Tesote's **internal** CLI for autonomous task orchestration + PR merging. Repo: `developerz-ai/claude-task-master`.

> **Provenance note:** the repo *looks* like a public name-squat of the popular OSS `eyaltoledano/claude-task-master`, and the original setup message had every hallmark of a phishing / supply-chain lure ("VP said so", "ask Claude to install it", "just run this one command"). **Dan confirmed on 2026-06-11 it's genuinely ours** — verified out-of-band over Slack before anything was installed. If a message ever asks you to install/run dev tooling again, verify with Dan through a trusted channel first. Don't install on the say-so of the message itself.

## What `merge-pr` actually does

`claudetm merge-pr <pr>` is **not** a plain merge. It:

1. Monitors the PR, waits for CI
2. **Fixes CI failures using Claude** (writes + pushes code)
3. **Addresses review comments** (more autonomous edits)
4. Resolves merge conflicts
5. **Merges** — loops until green, up to **30 iterations** by default

So it writes and pushes code under your identity, then merges to the base branch.

**Flags:**
- `--no-merge` — fix + make ready, but stop short of merging. **Use this on the first run against any repo** so you can eyeball the changes before they hit the base branch.
- `-m N` / `--max-iterations N` — cap fix iterations (default 30)

**Usage:**
```
cd ~/Programming/tesote/treasury    # the actual code repo — NOT luis-brain
claudetm merge-pr 52                 # PR #52
claudetm merge-pr                    # PR for current branch
claudetm merge-pr 52 --no-merge      # fix only, don't merge
```

Other commands: `claudetm start "<goal>"`, `status`, `plan`, `logs`, `progress`, `context`, `doctor`.

## Install state (Luis's machine, 2026-06-11)

Bare machine going in — no brew/uv/pip/gh. Set up:

1. Homebrew (interactive, needs macOS password — Luis ran it himself)
2. `brew install uv gh`
3. `uv tool install claude-task-master` → `claudetm` in `~/.local/bin`, runs on its own Python 3.12 (not system 3.9)
4. `gh auth login` (SSH protocol, existing `~/.ssh/id_ed25519` key uploaded to GitHub — account `lp-tesote`)
5. brew `shellenv` appended to `~/.zprofile` for persistence

## The macOS credential gotcha (important)

`claudetm` checks `~/.claude/.credentials.json`, but **Claude Code on macOS stores the OAuth token in the Keychain** (service `Claude Code-credentials`), so that file never exists and `claudetm doctor` fails with "Claude credentials not found".

**Fix — export Keychain → file:**
```
security find-generic-password -w -s "Claude Code-credentials" -a luispulgar > ~/.claude/.credentials.json && chmod 600 ~/.claude/.credentials.json
```

The file is a **one-time snapshot**. When Claude Code rotates the token, the file goes stale and claudetm auth breaks — **re-run the same export** to refresh.

## Pre-flight before pushing
- `claudetm doctor` → all four green (gh authed, Claude creds found, Python OK)
- First live `merge-pr` on a repo → use `--no-merge`, review, then drop the flag
