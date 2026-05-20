---
mode: agent
description: Autonomously add a new entry to this wiki repository: categorize the content, create the markdown file with standardized frontmatter, update the parent README MOC, and register it in nav.json.
---

**Task:** Add the following content to this Wiki repository.

**Content to Add:** [PASTE YOUR RAW NOTE/TOOL/PROMPT HERE]

**Autonomous Workflow:**
1. **Analyze & Categorize:** Determine the most appropriate directory (e.g., `development/languages/`, `infrastructure/cloud/`, `prompts/app-generation/`).
2. **Format File:**
   - Create a new `.md` file with a URL-friendly name.
   - Add standardized YAML Frontmatter (title, description, type: content, path, tags).
   - Add the `## 🔗 Navigation` section with correct relative paths to Parent and Root.
   - Use standard Markdown headers (`##`) for the content.
3. **Update Parent MOC:**
   - Locate the `README.md` in the target directory.
   - Add the new file to the `## 📁 Contents` list with a concise one-sentence description.
   - Ensure the list remains organized (alphabetical or logical).
4. **Update nav.json:**
   - Add the new entry under the correct section so it appears in the sidebar.
5. **Cross-Link:**
   - Scan the new content for keywords that exist as primary guides in the Wiki (e.g., Docker, SQL, SSH).
   - Link those keywords to their respective primary files using relative paths.

**Rules:**
- Do not use HTML tags.
- Ensure all relative paths are accurate based on the file depth.
- Propose the file path and MOC update before executing.
