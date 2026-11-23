# Skill: Web-to-Mobile App Transformation (React + Vite + Capacitor)

## Overview
This skill provides a comprehensive workflow for transforming a standalone React component file into a production-ready mobile application for Android, featuring native storage, in-app update checks, and automated GitHub releases.

## Prerequisites
- Node.js (v18+)
- Android SDK & Java 21 (for native builds)
- GitHub Repository for CI/CD

---

## Phase 1: Web Foundation (React + Vite + Tailwind)

### 1. Initialize Project
Create a modern React project using Vite and install styling dependencies.
```bash
npm create vite@latest . -- --template react
npm install
npm install -D tailwindcss @tailwindcss/vite
```

### 2. Configure Tailwind CSS v4
Update `vite.config.js` to include the Tailwind plugin and set up your CSS entry point.
```javascript
// vite.config.js
import tailwindcss from '@tailwindcss/vite'
export default defineConfig({
  plugins: [react(), tailwindcss()],
})

// src/index.css
@import "tailwindcss";
```

### 3. Integrate Source Code
Migrate your logic from your source file (e.g., `SC`) into `src/App.jsx`. Ensure all icons, components, and state logic are correctly imported.

---

## Phase 2: Mobile Integration (Ionic + Capacitor)

### 1. Install Mobile Core
Add Ionic components for mobile UI patterns and Capacitor for the native bridge.
```bash
npm install @ionic/react @ionic/react-router ionicons
npm install @capacitor/core @capacitor/cli @capacitor/android
```

### 2. Initialize Capacitor
Configure the native project metadata.
```bash
npx cap init "App Name" com.yourdomain.app --web-dir dist
npx cap add android
```

---

## Phase 3: Native Feature Migration

### 1. Native Preferences (LocalStorage Replacement)
Replace standard `localStorage` with `@capacitor/preferences` for persistent native storage.

**Installation:**
```bash
npm install @capacitor/preferences
```

**Implementation Pattern:**
```javascript
import { Preferences } from '@capacitor/preferences';

// Loading data
const loadData = async () => {
  const { value } = await Preferences.get({ key: 'my-key' });
  return value ? JSON.parse(value) : null;
};

// Saving data
const saveData = async (data) => {
  await Preferences.set({ key: 'my-key', value: JSON.stringify(data) });
};
```

### 2. In-App Update Checker
Fetch the latest release version from the GitHub API to notify users of updates.
```javascript
const checkForUpdates = async () => {
  const response = await fetch('https://api.github.com/repos/OWNER/REPO/releases/latest');
  const data = await response.json();
  const latest = data.tag_name;
  if (latest !== APP_VERSION) {
    // Show update prompt with data.html_url
  }
};
```

---

## Phase 4: Automation & CI/CD

### 1. Build Script (`scripts/build-android.sh`)
Create a robust script to handle the web-to-native build flow.
```bash
#!/usr/bin/env bash
set -euo pipefail
npm run build
npx cap sync android
cd android && ./gradlew assembleDebug && cd ..
```

### 2. GitHub Actions Workflow (`.github/workflows/android-release.yml`)
Configure a workflow to automatically build and release an APK when a version tag (e.g., `v1.0.0`) is pushed.

**Key Steps:**
- Setup Node, Java, and Android SDK.
- Run `scripts/build-android.sh`.
- Rename the APK using the pattern: `app-name-${VERSION_TAG}.apk`.
- Use `softprops/action-gh-release` to create a release and attach the APK.

---

## Best Practices & Troubleshooting

### Linting for CI
Ensure your code is "CI-ready" by resolving these common React issues:
- **Avoid setState in Effects:** Calculate derived values during render to avoid cascading re-renders.
- **Initialization Order:** Declare helper functions (`useCallback`) above their usage in `useEffect`.
- **Ignore Rules:** Configure `eslint.config.js` to ignore the `android` and `dist` directories.

### Syncing
Always run `npx cap sync android` after making changes to web assets or installing new Capacitor plugins.
