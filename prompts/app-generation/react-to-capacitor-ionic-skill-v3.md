# GitHub Actions + Vite + Tailwind + Capacitor Build Skill

## Problem Statement
Building React + Vite + Tailwind + Capacitor projects in GitHub Actions fails with native binding errors, Node version issues, and permission problems. This guide prevents those errors.

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

## Complete GitHub Actions Template

```yaml
name: Android Release Build

on:
  push:
    tags:
      - 'v*'

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
      
      - name: Build APK
        run: |
          cd android
          chmod +x gradlew
          ./gradlew assembleDebug
          cd ..
      
      - name: Extract version
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT
      
      - name: Rename APK
        run: |
          mv android/app/build/outputs/apk/debug/app-debug.apk \
             android/app/build/outputs/apk/debug/app-${{ steps.version.outputs.VERSION }}.apk
      
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: android/app/build/outputs/apk/debug/app-*.apk
          draft: false
          prerelease: false
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Checklist for New Projects

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

## Why This Works

1. **Tailwind v3** = No native modules = Portable to any CI/CD
2. **PostCSS** = Standard, battle-tested approach
3. **npm install** = Handles peer deps + rebuilds properly
4. **No cache** = Fresh, reliable builds every time
5. **Node 22** = Meets Capacitor requirements
6. **Explicit permissions** = GitHub Actions security model

## Performance Notes
- Tailwind v3 with PostCSS is ~5-10ms slower than v4 plugin, but 100% reliable in CI
- Trade-off: Reliability > Speed for CI/CD pipelines
