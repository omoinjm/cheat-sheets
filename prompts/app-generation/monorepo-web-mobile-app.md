# Monorepo Transition Prompt

Use this prompt to guide an AI assistant in converting a single-repo React project into a monorepo with Web and Mobile targets.

---

Act as a Senior Full-Stack Engineer and Architect. I want to convert my existing React/Tailwind project into a Monorepo using npm workspaces. 

### Current Context:
- A React application with interactive components (SectionHeader, Card, etc.) and specific lecture sections (Intro, Variables, Control Flow).
- Stack: Vite, React 19, Tailwind CSS v4, Lucide-React.

### Goal:
Restructure the project into a Monorepo to support two applications:
1. `apps/web`: A standard Vite + React web application.
2. `apps/mobile`: An Ionic + Capacitor mobile application.
3. `packages/ui`: A shared component library containing all the core logic and UI from the existing project.

### Technical Requirements:
1. **Root Configuration**: Setup a root `package.json` with `workspaces: ["apps/*", "packages/*"]`.
2. **Shared UI**: Extract all functional components (IntroSection, VariablesSection, etc.) from the current `App.jsx` into `packages/ui`. Ensure they are exported properly.
3. **Tailwind Shared Config**: Create a `packages/tailwind-config` or similar mechanism so that both apps use the same design tokens and Tailwind v4 setup.
4. **App Migration**: 
   - Move the existing web logic to `apps/web`.
   - Initialize a mobile-ready React app in `apps/mobile` with Ionic components and Capacitor initialization.
5. **Dependency Management**: Hoist common dependencies (React, Lucide, Tailwind) to the root where appropriate or manage them strictly within workspace packages.

### Build & Release:
The project includes automated build and release infrastructure for Android:
- **`scripts/build-android.sh`**: Local build script that handles web asset compilation, Capacitor syncing, and Android APK generation.
- **`.github/workflows/android-release.yml`**: CI/CD workflow that automates Android builds on version tags and PRs, and creates GitHub releases with APK artifacts.

### Deliverables:
- A step-by-step file structure plan.
- The content for the new root `package.json`.
- The configuration for `packages/ui/package.json` and its main export file.
- Instructions on how to link `@repo/ui` to both `apps/web` and `apps/mobile`.
- The `vite.config.js` and `tailwind.config.js` adjustments needed for workspaces to resolve local package imports.
