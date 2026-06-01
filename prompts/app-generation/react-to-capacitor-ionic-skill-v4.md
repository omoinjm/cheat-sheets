---
title: React to Capacitor Ionic Skill v4
description: Complete skill for transforming a React app into a signed Android release APK via GitHub Actions, with CI/CD fixes, responsive app guidelines, and automated versioned releases.
type: content
path: prompts/app-generation/react-to-capacitor-ionic-skill-v4.md
tags: [react, capacitor, ionic, android, github-actions, tailwind, ci-cd, mobile]
---

# GitHub Actions + Vite + Tailwind + Capacitor Build Skill (v4)

## Skill Installation

Install this skill locally in the project you are working on:

```bash
npx skills add https://github.com/vercel-labs/skills --skill find-skills
```

Use `find-skills` to discover the best skills for building **responsive apps** that fit and function on any device size, following mobile UI/UX guidelines:
- Safe area insets (notch, home indicator)
- Adaptive layouts (phone, tablet, desktop)
- Touch target sizing (min 44×44px)
- Platform-specific navigation patterns (iOS vs Android)

---

## Problem Statement
Building React + Vite + Tailwind + Capacitor projects in GitHub Actions fails with native binding errors, Node version issues, and permission problems. This guide prevents those errors and produces a **signed release APK** named `app-{name_of_app}-{version_tag}.apk`.

## Root Causes & Solutions

### 1. Tailwind CSS Native Binding Issue (CRITICAL)
**Error**: "Cannot find native binding" for @tailwindcss/oxide in CI

**Root Cause**: 
- `@tailwindcss/vite` (v4+) requires native modules (@tailwindcss/oxide)
- GitHub Actions runners can't build these reliably
- npm caching makes it worse

**Solution**: Use **Tailwind v3 with PostCSS** (no native deps)

```json
{
  "devDependencies": {
    "tailwindcss": "^3.4.1",
    "autoprefixer": "^10.4.21"
  }
}
```

Remove from vite.config.ts:
```ts
// ❌ DELETE THIS
import tailwindcss from '@tailwindcss/vite';
export default defineConfig({
  plugins: [react(), tailwindcss()],  // Remove tailwindcss()
});

// ✅ USE THIS
export default defineConfig({
  plugins: [react()],
});
```

### 2. CSS Syntax (v3 vs v4)
**Wrong** (v4 syntax):
```css
@import "tailwindcss";
```

**Correct** (v3 syntax) in `src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 3. PostCSS Configuration
Create `postcss.config.js`:
```js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

Create `tailwind.config.js`:
```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

### 4. GitHub Actions Workflow Issues

#### Issue: npm cache conflicts
**Solution**: Disable npm caching in setup-node
```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '22'
    cache: null  # ← CRITICAL: Prevents corrupted cache
```

#### Issue: npm ci doesn't rebuild native modules
**Solution**: Use `npm install` instead and clear cache
```yaml
- name: Clear npm cache and remove lock file
  run: |
    npm cache clean --force
    rm -f package-lock.json

- name: Install dependencies
  run: npm install --legacy-peer-deps
```

#### Issue: Capacitor CLI requires Node 22+
**Solution**: Set Node version to 22
```yaml
node-version: '22'  # NOT 18
```

#### Issue: Release creation fails with 403
**Solution**: Add permissions block to job
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # ← REQUIRED for creating releases
    
    steps: ...
```

---

## APK Signing Setup (Release Build)

A **signed release APK** is required for distribution. Debug builds cannot be installed on most devices and are not suitable for release.

### Step 1: Generate a Keystore (one-time, locally)
```bash
keytool -genkey -v -keystore release.keystore \
  -alias my-key-alias \
  -keyalg RSA -keysize 2048 -validity 10000
```

### Step 2: Encode Keystore as Base64 and Add to GitHub Secrets
```bash
base64 -w 0 release.keystore | pbcopy  # macOS
base64 -w 0 release.keystore           # Linux — copy the output
```

Add the following secrets to your GitHub repository (`Settings > Secrets and variables > Actions`):

| Secret Name              | Value                                  |
|--------------------------|----------------------------------------|
| `KEYSTORE_BASE64`        | Base64-encoded keystore file           |
| `KEYSTORE_PASSWORD`      | Password set during keytool generation |
| `KEY_ALIAS`              | Alias used during keytool generation   |
| `KEY_PASSWORD`           | Key password (often same as keystore)  |

### Step 3: Configure Signing in `android/app/build.gradle`
```groovy
android {
    signingConfigs {
        release {
            storeFile file(System.getenv("KEYSTORE_PATH") ?: "release.keystore")
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias System.getenv("KEY_ALIAS")
            keyPassword System.getenv("KEY_PASSWORD")
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

---

## APK Naming Convention

The APK must be named using this pattern:
```
app-{name_of_app}-{version_tag}.apk
```

Example: pushing tag `v1.2.0` on a project named `my-tracker` produces:
```
app-my-tracker-v1.2.0.apk
```

Set `APP_NAME` as a workflow-level env var (see complete template below).

---

## Complete GitHub Actions Template

```yaml
name: Android Release Build

on:
  push:
    tags:
      - 'v*'

env:
  APP_NAME: my-app-name  # ← Change this to your app's name (kebab-case)

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: null
      
      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '21'
      
      - name: Setup Android SDK
        uses: android-actions/setup-android@v3
      
      - name: Decode Keystore
        run: |
          echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > android/app/release.keystore
        env:
          KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
      
      - name: Clear npm cache and remove lock file
        run: |
          npm cache clean --force
          rm -f package-lock.json
      
      - name: Install dependencies
        run: npm install --legacy-peer-deps
      
      - name: Build web assets
        run: npm run build
      
      - name: Sync with Android
        run: npx cap sync android
      
      - name: Build signed release APK
        run: |
          cd android
          chmod +x gradlew
          ./gradlew assembleRelease
          cd ..
        env:
          KEYSTORE_PATH: app/release.keystore
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
      
      - name: Extract version tag
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT
      
      - name: Rename APK
        run: |
          mv android/app/build/outputs/apk/release/app-release.apk \
             android/app/build/outputs/apk/release/app-${{ env.APP_NAME }}-${{ steps.version.outputs.VERSION }}.apk
      
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: android/app/build/outputs/apk/release/app-${{ env.APP_NAME }}-*.apk
          draft: false
          prerelease: false
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Checklist for New Projects

- [ ] Install skill: `npx skills add https://github.com/vercel-labs/skills --skill find-skills`
- [ ] Run `find-skills` to identify responsive layout and mobile UI skills
- [ ] Use Tailwind v3, NOT v4 (v4 requires native modules)
- [ ] Create `postcss.config.js` + `tailwind.config.js`
- [ ] Use v3 CSS syntax: `@tailwind base; components; utilities;`
- [ ] Set Node.js to 22+ in GitHub Actions (Capacitor requirement)
- [ ] Add `cache: null` to setup-node (prevents corrupted cache)
- [ ] Use `npm install`, not `npm ci` (rebuilds native deps properly)
- [ ] Add `permissions: contents: write` for release creation
- [ ] Clear npm cache before install: `npm cache clean --force`
- [ ] Remove `@tailwindcss/vite` from dependencies
- [ ] Remove tailwindcss plugin from vite.config.ts
- [ ] Generate keystore and add `KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD` secrets
- [ ] Configure `android/app/build.gradle` signing config (release block)
- [ ] Use `assembleRelease` (NOT `assembleDebug`) in workflow
- [ ] Set `APP_NAME` env var in workflow (kebab-case)
- [ ] APK output: `app-{APP_NAME}-{VERSION_TAG}.apk`

---

## Why This Works

1. **Tailwind v3** = No native modules = Portable to any CI/CD
2. **PostCSS** = Standard, battle-tested approach
3. **npm install** = Handles peer deps + rebuilds properly
4. **No cache** = Fresh, reliable builds every time
5. **Node 22** = Meets Capacitor requirements
6. **Explicit permissions** = GitHub Actions security model
7. **Signed release APK** = Distributable on real devices and stores
8. **`find-skills`** = Discovers responsive/mobile UI skills for the project

## Performance Notes
- Tailwind v3 with PostCSS is ~5-10ms slower than v4 plugin, but 100% reliable in CI
- Trade-off: Reliability > Speed for CI/CD pipelines

---

## 🔗 Navigation

- [← App Generation README](README.md)
- [← Cheat Sheets Home](../../README.md)
