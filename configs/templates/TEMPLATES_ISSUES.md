# Issue templates

This file contains special templates for the issues, which can't be used as
direct (in repository) ways, so this is a storage for them.

## Issue for release tracking

When project (repository) is only created from the start, you don't have any
issues, but you probably still want to add your new project into the board-tracker.

This issue is created specially for the needs like these.

```yml
title:
    [BACKLOG]: release-issue for tracking initial development of project <PROJECT_NAME>
body: |
    This is an issue of special template-purpose: to track start of development for any project.
    
    > [!Note]
    > In this case, project "<PROJECT_NAME>" is the one.
    
    Issue like is created to not only track, but possibly discuss initial releases.
labels:
    - announcement
    - backlog
projects:
    - <TRACKER_PROJECT>
milestones:
    - Initial release
development:
    - <CUSTOM>
assignees:
    - <CUSTOM>
```

Replace `<PROJECT_NAME>` with the name (or preferenced title) of your project and replace
`<TRACKER_PROJECT>` with your project-tracker (dropbox choice). For development branch and
assignees, implement your choice (depending on your team and conventions).

## From draft issue of project to normalized issue

In projects with very big planning, you often do drafts to not spam your project with issues
you won't fix in the near future, and, as I think, this is a good practice: you know what you
want, but do not force it right at the moment.

But when you actually start to think about developing new features and releases from project,
you want to create issues for consistency and more advanced controls over the issues system on
GitHub than using "just texts" drafts.

The problem is, when you convert draft to the issue, no templates are applied, so you need to
customize it from the start: this "template" fixes this issue.

> [!Important]
> Do not work with this kind of issues individually, think as
> an authomathon: if some template can be applied to your newly
> drafted issue, apply them.

```yml
body: |
    > [!Note]
    > **This issue was auto-generated from <PROJECT_NAME>'s project.**
```

Replace `<PROJECT_NAME>` with your project's name accordingly. Also include text of what the
issue is and, if there some are, list of the subissues. To display the [practice][2] of this template,
I would show some of my issues from [UNITADE][1] project, in which such practices are often occur.

```markdown
> [!Note]
> **This issue was auto-generated from UNITADE's project.**

Add basic commands for:
1. Enabling/disabling code editor module;
2. Enabling/disabling safe mode;
3. Enabling/disabling case-sensitive mode;
4. Add extension to "extensions-as-markdown";
5. Add extension to "extensions-as-codeview";

**Subissues:**
- request docs for this commands;
- request lang support for this commands in the settings (enable/disable commands interface);
```

[1]: https://github.com/Falcion/UNITADE.md
[2]: https://github.com/Falcion/UNITADE.md/issues/96
