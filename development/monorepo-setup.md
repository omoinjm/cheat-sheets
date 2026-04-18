---
title: Monorepo Setup with npm Workspaces
description: A comprehensive guide to converting a single-repo React project into a monorepo with Web and Mobile targets using npm workspaces.
type: content
path: development/monorepo-setup.md
tags: [javascript, npm, monorepo, workspaces, react, vite, mobile, architecture]
---

# Monorepo Setup with npm Workspaces

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../README.md)

## 📌 Overview

This guide covers converting a single-repo React project into a **monorepo** using **npm workspaces** to support multiple applications (Web and Mobile) while sharing a common UI component library.

## 🎯 Goals

1. Restructure a React application into a monorepo supporting:
   - `apps/web`: Vite + React web application
   - `apps/mobile`: Ionic + Capacitor mobile application
   - `packages/ui`: Shared component library
   - `packages/tailwind-config`: Shared design tokens and Tailwind configuration

2. Enable code sharing and unified dependency management
3. Maintain consistent design systems across platforms

---

## 🏗️ File Structure Plan

```
monorepo/
├── package.json (root, with workspaces)
├── pnpm-workspace.yaml or .npmrc (if using pnpm)
├── apps/
│   ├── web/
│   │   ├── package.json
│   │   ├── vite.config.js
│   │   ├── src/
│   │   │   ├── main.jsx
│   │   │   └── App.jsx
│   │   └── index.html
│   └── mobile/
│       ├── package.json
│       ├── capacitor.config.json
│       ├── vite.config.js
│       ├── src/
│       │   ├── main.jsx
│       │   └── App.jsx
│       └── index.html
├── packages/
│   ├── ui/
│   │   ├── package.json
│   │   ├── src/
│   │   │   ├── index.js (main export)
│   │   │   ├── components/
│   │   │   │   ├── SectionHeader.jsx
│   │   │   │   ├── Card.jsx
│   │   │   │   ├── IntroSection.jsx
│   │   │   │   ├── VariablesSection.jsx
│   │   │   │   └── ControlFlowSection.jsx
│   │   │   └── hooks/
│   │   │       └── (shared logic)
│   │   └── tailwind.config.js
│   └── tailwind-config/
│       ├── package.json
│       └── tailwind.config.js
└── README.md
```

---

## 📋 Step-by-Step Implementation

### Step 1: Root `package.json`

```json
{
  "name": "monorepo",
  "version": "1.0.0",
  "private": true,
  "description": "Monorepo for web and mobile applications",
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev": "npm run dev -w",
    "build": "npm run build -w",
    "preview": "npm run preview -w",
    "lint": "npm run lint -w",
    "dev:web": "npm run dev -w apps/web",
    "dev:mobile": "npm run dev -w apps/mobile",
    "build:web": "npm run build -w apps/web",
    "build:mobile": "npm run build -w apps/mobile"
  },
  "devDependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "typescript": "^5.0.0",
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "tailwindcss": "^4.0.0",
    "postcss": "^8.0.0",
    "autoprefixer": "^10.0.0"
  }
}
```

### Step 2: `packages/ui/package.json`

```json
{
  "name": "@repo/ui",
  "version": "1.0.0",
  "type": "module",
  "main": "./src/index.js",
  "exports": {
    ".": "./src/index.js",
    "./components": "./src/components/index.js"
  },
  "peerDependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "dependencies": {
    "lucide-react": "^latest"
  },
  "devDependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  }
}
```

### Step 3: `packages/ui/src/index.js` (Main Export)

```javascript
// Export all components
export { SectionHeader } from './components/SectionHeader.jsx';
export { Card } from './components/Card.jsx';
export { IntroSection } from './components/IntroSection.jsx';
export { VariablesSection } from './components/VariablesSection.jsx';
export { ControlFlowSection } from './components/ControlFlowSection.jsx';

// Export hooks if applicable
export * from './hooks/index.js';
```

### Step 4: `packages/tailwind-config/package.json`

```json
{
  "name": "@repo/tailwind-config",
  "version": "1.0.0",
  "main": "./tailwind.config.js",
  "exports": {
    ".": "./tailwind.config.js"
  }
}
```

### Step 5: `packages/tailwind-config/tailwind.config.js`

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    '../../packages/ui/src/**/*.{jsx,js}',
    './src/**/*.{jsx,js}'
  ],
  theme: {
    extend: {
      colors: {
        // Add shared design tokens here
      }
    }
  },
  plugins: []
};
```

### Step 6: `apps/web/vite.config.js`

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@repo/ui': path.resolve(__dirname, '../../packages/ui/src'),
      '@repo/tailwind-config': path.resolve(__dirname, '../../packages/tailwind-config')
    }
  }
});
```

### Step 7: `apps/web/package.json`

```json
{
  "name": "@repo/web",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@repo/ui": "*",
    "@repo/tailwind-config": "*"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "^5.0.0",
    "tailwindcss": "^4.0.0",
    "postcss": "^8.0.0"
  }
}
```

### Step 8: `apps/mobile/package.json` (with Ionic + Capacitor)

```json
{
  "name": "@repo/mobile",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "cap:add:ios": "npx cap add ios",
    "cap:add:android": "npx cap add android",
    "cap:sync": "npx cap sync",
    "cap:open:ios": "npx cap open ios",
    "cap:open:android": "npx cap open android"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@ionic/react": "^latest",
    "@ionic/react-router": "^latest",
    "@capacitor/core": "^latest",
    "@capacitor/cli": "^latest",
    "@repo/ui": "*",
    "@repo/tailwind-config": "*"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "^5.0.0",
    "@capacitor/ios": "^latest",
    "@capacitor/android": "^latest"
  }
}
```

---

## 🔗 Linking `@repo/ui` to Applications

### Via npm Workspaces (Automatic)

Once `packages/ui` is defined in the root `package.json` with `"workspaces": ["packages/*", "apps/*"]`, npm automatically symlinks the package. In your app code:

```javascript
// apps/web/src/App.jsx
import { SectionHeader, Card, IntroSection } from '@repo/ui';

export default function App() {
  return (
    <div>
      <SectionHeader title="Welcome" />
      <Card>
        <IntroSection />
      </Card>
    </div>
  );
}
```

### Manual Override (if needed)

In `apps/web/package.json`:

```json
{
  "dependencies": {
    "@repo/ui": "file:../../packages/ui"
  }
}
```

Then run: `npm install`

---

## ⚙️ Vite Configuration for Workspaces

### Issue: Module Resolution

Vite may not automatically resolve `@repo/ui` imports. Add aliases in both app `vite.config.js`:

```javascript
import path from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@repo/ui': path.resolve(__dirname, '../../packages/ui/src')
    }
  }
});
```

### TypeScript Support (Optional)

If using TypeScript, create `tsconfig.json` in root:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@repo/ui": ["packages/ui/src/index.js"],
      "@repo/ui/*": ["packages/ui/src/*"]
    }
  }
}
```

---

## 📦 Tailwind v4 Shared Configuration

### Approach 1: Shared Config Package

Create `packages/tailwind-config/index.js`:

```javascript
import tailwindConfig from './tailwind.config.js';
export default tailwindConfig;
```

In apps, reference it:

```javascript
// apps/web/tailwind.config.js
import sharedConfig from '@repo/tailwind-config';

export default {
  ...sharedConfig,
  content: [
    '../../packages/ui/src/**/*.{jsx,js}',
    './src/**/*.{jsx,js}'
  ]
};
```

### Approach 2: Direct Inheritance

In `apps/web/tailwind.config.js`:

```javascript
import { resolve } from 'path';

export default {
  content: [
    resolve(__dirname, '../../packages/ui/src/**/*.{jsx,js}'),
    './src/**/*.{jsx,js}'
  ],
  theme: {
    extend: {
      // App-specific overrides
    }
  },
  plugins: []
};
```

---

## 🚀 Dependency Management Best Practices

| Approach | When to Use | Pros | Cons |
|----------|-----------|------|------|
| **Hoisted (Root)** | Common deps (React, Tailwind, TypeScript) | Single version, smaller lock file | All apps must use same version |
| **Workspace Package** | Shared UI, utilities | Explicit, versionable | Duplicate deps in lock file |
| **Peer Dependencies** | Optional integrations | Flexible, apps choose versions | Requires explicit installation |

### Recommended Setup:

```json
{
  "root": {
    "dependencies": ["react", "react-dom", "tailwindcss", "typescript"]
  },
  "packages/ui": {
    "peerDependencies": ["react", "react-dom"]
  },
  "apps/web": {
    "dependencies": ["@repo/ui", "@repo/tailwind-config"]
  },
  "apps/mobile": {
    "dependencies": ["@repo/ui", "@repo/tailwind-config", "@ionic/react", "@capacitor/core"]
  }
}
```

---

## 🔄 Workflow & Commands

### Install Dependencies

```bash
npm install
```

### Development

```bash
# All workspaces
npm run dev

# Specific app
npm run dev:web
npm run dev:mobile
```

### Build

```bash
# All workspaces
npm run build

# Specific app
npm run build:web
npm run build:mobile
```

### Adding Dependencies

```bash
# To root (hoisted)
npm install lodash

# To specific workspace
npm install lodash -w apps/web

# To UI package
npm install my-utility -w packages/ui
```

---

## ⚠️ Common Pitfalls & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Module not found: `@repo/ui` | Vite alias not configured | Add `resolve.alias` to `vite.config.js` |
| Tailwind classes not applied | Content paths incorrect | Verify `content` includes all source dirs |
| Duplicate React instances | Each app has own React copy | Hoist React to root `package.json` |
| Import cycles | UI imports from apps | Keep UI package pure, import only from apps |
| Capacitor plugins not found | Plugins not installed in mobile app | Run `npm install` in `apps/mobile` after adding plugins |

---

## 📚 Related Topics

- **[npm Workspaces](../standards/)** – Dependency management
- **React** – Component development
- **[Vite](../languages/)** – Build tooling
- **Tailwind CSS v4** – Styling framework
- **Ionic + Capacitor** – Mobile framework
- **TypeScript** (optional) – Type safety

---

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../README.md)
