---
title: Git - Tagging and Pushing
description: A quick guide on how to create lightweight and annotated tags in Git and push them to a remote repository.
type: content
path: workspace/vcs/git_tags.md
tags: [workspace, vcs, git, tagging]
---
# Git - Tagging and Pushing

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

To tag on Git and push it, you typically follow these steps:

1.  **Create a lightweight tag:**
    ```bash
    git tag <tag-name>
    ```
    (e.g., `git tag v1.0.0`)

2.  **Create an annotated tag (recommended, includes message, author, date):**
    ```bash
    git tag -a <tag-name> -m "Tag message"
    ```
    (e.g., `git tag -a v1.0.0 -m "Release version 1.0.0"`)

3.  **Push the tag to the remote repository:**
    ```bash
    git push origin <tag-name>
    ```
    (e.g., `git push origin v1.0.0`)

4.  **To push all tags at once:**
    ```bash
    git push origin --tags
    ```
