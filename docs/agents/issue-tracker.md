# Issue tracker: GitHub

Issues and specs for this repo live in GitHub Issues at `haitham113/pdfMining`. Use the `gh` CLI.

## Conventions

- Create an issue with `gh issue create --title "..." --body-file <file>`.
- Read an issue and its discussion with `gh issue view <number> --comments`.
- List issues with `gh issue list --state open --json number,title,body,labels,comments`, adding state or label filters as needed.
- Comment with `gh issue comment <number> --body-file <file>`.
- Apply or remove labels with `gh issue edit <number> --add-label "..."` or `--remove-label "..."`.
- Close with `gh issue close <number> --comment "..."`.

Run `gh` from this clone so it infers the repo from the GitHub remote.

## Pull requests as a triage surface

**PRs as a request surface: no.** Set to `yes` if this repo later treats external PRs as feature requests.

When enabled, read PRs with `gh pr view <number> --comments` and `gh pr diff <number>`; list, comment, label, and close with the corresponding `gh pr` commands. GitHub shares issue and PR numbers, so resolve an ambiguous number before acting on it.

## Skill instructions

When a skill says "publish to the issue tracker", create a GitHub issue. When it says "fetch the relevant ticket", read the issue and its comments.

For `/wayfinder`, keep the map in one issue labeled `wayfinder:map` and use GitHub sub-issues for child tickets. Use GitHub issue dependencies for blockers. If either feature is unavailable, list child tickets in the map body and record `Blocked by: #<number>` in the child. Claim an available ticket with `gh issue edit <number> --add-assignee @me`; record the result before closing it.
