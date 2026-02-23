---
title: Automated Wiki Maintenance & Entry Template
description: A master instruction for AI assistants to autonomously add, categorize, and link new content into the Wiki structure.
type: content
path: prompts/documentation/automated-wiki-maintenance.md
tags: [prompts, llm, documentation, automation, wiki, maintenance]
---
# Automated Wiki Maintenance Prompt

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

## 📌 Overview
Use this prompt when you have a new piece of information, a tool, or a prompt that you want to add to the repository. It ensures the AI handles the categorization, formatting, and MOC updates autonomously.

---

## 🛠️ The "New Entry" Master Prompt

> **Task:** Add the following content to my Wiki-fied repository.
>
> **Content to Add:** [PASTE YOUR RAW NOTE/TOOL/PROMPT HERE]
>
> **Autonomous Workflow:**
> 1. **Analyze & Categorize:** Determine the most appropriate directory (e.g., `development/languages/`, `infrastructure/cloud/`, `prompts/app-generation/`).
> 2. **Format File:**
>    - Create a new `.md` file with a URL-friendly name.
>    - Add standardized YAML Frontmatter (title, description, type: content, path, tags).
>    - Add the `## 🔗 Navigation` section with correct relative paths to Parent and Root.
>    - Use standard Markdown headers (`##`) for the content.
> 3. **Update Parent MOC:**
>    - Locate the `README.md` in the target directory.
>    - Add the new file to the `## 📁 Contents` list with a concise one-sentence description.
>    - Ensure the list remains organized (alphabetical or logical).
> 4. **Cross-Link:**
>    - Scan the new content for keywords that exist as primary guides in the Wiki (e.g., Docker, SQL, SSH).
>    - Link those keywords to their respective primary files using relative paths.
>
> **Rules:**
> - Do not use HTML tags.
> - Ensure all relative paths are accurate based on the file depth.
> - Propose the file path and MOC update before executing.

---

## 💡 How to Use
1. Copy the prompt above.
2. Paste it into your AI chat.
3. Replace the `[PASTE YOUR RAW NOTE...]` section with your new info.
4. The AI will handle the rest of the "Wiki-fication" workflow.
