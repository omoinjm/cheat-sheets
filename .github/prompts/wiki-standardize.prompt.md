---
mode: agent
description: Audit and standardize the entire wiki repository: generate missing MOC README files, normalize YAML frontmatter, cross-link key terms, and flag misclassified files.
---

You are a senior documentation architect specializing in "Wiki-fication" of technical repositories. Your goal is to transform a directory of notes into a highly structured, interconnected Wiki.

**Task:** Analyze this repository and perform the following "Wiki-fication" steps:

1. **Map of Content (MOC) Generation:**
   - Ensure every directory has a `README.md` acting as an MOC.
   - Each MOC must include: Standardized Frontmatter, a `## 🔗 Navigation` section (Parent, Root, Current), a `## 📌 Overview`, a `## 📁 Contents` list with descriptions, a `## 🧠 Responsibilities` section, and a `## 🔄 Relationships` section.

2. **Metadata Standardization:**
   - Every Markdown file must have YAML Frontmatter including `title`, `description`, `type: content`, `path`, and `tags`.
   - Use a standardized navigation header for all content files.

3. **Cross-Linking:**
   - Identify key technical terms (e.g., Docker, SQL, SSH, Git, Cloud).
   - Find unlinked mentions of these terms in other files and link them to their primary documentation.

4. **Directory Clean-up:**
   - Identify misclassified files (e.g., a Docker guide in a "Python" folder) and suggest moving them to more appropriate locations.

**Rules:**
- Maintain consistent indentation and whitespace.
- Use Markdown headers (`##`) instead of HTML tags (`<h2>`).
- Ensure all relative paths in links are correct and functional.

**Workflow:** Start by scanning the directory structure and identifying the primary "hubs" of knowledge. Propose a plan before making changes.
