# Issue Tracker: GitHub

Issues and PRDs for this repo live in GitHub Issues for `GalaxyRuler/lughat-althuban`. Use the `gh` CLI for issue operations from inside this clone.

## Conventions

- Create an issue: `gh issue create --title "..." --body "..."`
- Read an issue: `gh issue view <number> --comments`
- List issues: `gh issue list --state open --json number,title,body,labels,comments`
- Comment on an issue: `gh issue comment <number> --body "..."`
- Apply a label: `gh issue edit <number> --add-label "..."`
- Remove a label: `gh issue edit <number> --remove-label "..."`
- Close an issue: `gh issue close <number> --comment "..."`

Infer the repository from `git remote -v`; `gh` does this automatically when run inside the clone.

## When A Skill Says "Publish To The Issue Tracker"

Create a GitHub issue in `GalaxyRuler/lughat-althuban`.

## When A Skill Says "Fetch The Relevant Ticket"

Run `gh issue view <number> --comments` and inspect labels, body, and comments.
