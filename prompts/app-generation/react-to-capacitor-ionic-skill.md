---
title: React to Capacitor + Ionic Migration Skill
description: A reusable prompt for converting an existing React app into a production-ready Capacitor + Ionic mobile application.
type: content
path: prompts/app-generation/react-to-capacitor-ionic-skill.md
tags: [prompts, app-generation, react, ionic, capacitor, mobile, migration]
---
# React to Capacitor + Ionic Migration Skill

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

## 📌 Overview
Use this skill prompt to transform an existing React codebase into a Capacitor + Ionic app with production-focused mobile engineering standards.

---

## 🛠️ The Skill Prompt

> **Role:** Act as a Senior Mobile Engineer specializing in React, Ionic, and Capacitor migrations.
>
> **Objective:** Transform my existing React project into a production-ready Capacitor + Ionic mobile app for Android and iOS without losing core functionality.
>
> **Input Context (I will provide):**
> - Current project structure and key React features
> - Existing routing/state management setup
> - Current API/auth integrations
> - Any web-only dependencies that may need mobile alternatives
> - Repository layout context (single-project root or monorepo path such as `apps/mobile`)
>
> **Migration Requirements:**
> 1. **Architecture First**
>    - Define a clear migration strategy (incremental vs full transition) with risk-aware sequencing.
>    - Keep business logic separated from presentation and platform adapters.
>    - Preserve reusable domain modules and isolate mobile-specific integrations.
> 2. **Ionic + Capacitor Foundation**
>    - Initialize and configure Ionic React with Capacitor for Android and iOS.
>    - Implement platform-safe routing/navigation patterns using Ionic primitives.
>    - Configure environment management for local, staging, and production builds.
> 3. **Industry-Standard Mobile Optimization**
>    - Optimize app startup time, bundle size, rendering performance, and memory usage.
>    - Apply mobile-first UX patterns: safe areas, responsive layouts, touch targets, and offline-aware states.
>    - Use lazy loading and route-level code splitting for large feature areas.
>    - Define image and asset optimization strategy for high-density screens.
> 4. **Native Capability Integration**
>    - Map required web APIs to Capacitor plugins (camera, storage, geolocation, push, etc.) where relevant.
>    - Ensure permissions, fallback behavior, and graceful degradation are handled.
> 5. **Security & Reliability**
>    - Enforce secure token handling and secret isolation for mobile builds.
>    - Add robust error boundaries, centralized logging hooks, and crash-safe recovery flows.
>    - Include network resilience patterns (timeouts, retries, backoff, and offline queueing where applicable).
> 6. **Build, Release, and Quality Gates**
>    - Provide a CI/CD-ready structure for Android/iOS builds and signing.
>    - Include test strategy recommendations (unit, integration, smoke/E2E) focused on mobile risk areas.
>    - Define acceptance criteria and a verification checklist for feature parity.
>    - Generate baseline Android CI/CD files (for example `scripts/build-android.sh` and `.github/workflows/android-release.yml`) and adjust paths to match the project layout.
>
> **Expected Deliverables:**
> - Target folder structure for the migrated app
> - A prioritized migration checklist with milestones
> - Updated dependency map (keep, replace, remove)
> - Key configuration files to create or modify
> - Performance and security hardening checklist
> - Post-migration validation checklist for Android and iOS

---

## 🚀 CI/CD Pipeline Templates

Use these as baseline templates in the generated project.
Assume these files are created from the application project root; adjust paths if using a monorepo (for example `apps/mobile`).
Typical monorepo adjustments include Android directory checks, APK output search paths, script working directories, and the `APK_SEARCH_ROOT` workflow environment variable.
The template files in `prompts/app-generation/android/` are reference copies; generated project output should use the destination paths shown below.

`scripts/build-android.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail
npm run build
if [[ ! -f "android/gradlew" ]]; then
  rm -rf android
  npx cap add android
fi
npm run android:sync
npm run android:build:debug
```

Create this file at `.github/workflows/android-release.yml`.

```yaml
name: Android Build & Release

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
    tags: ["v*"]
  workflow_dispatch:

jobs:
  build-android:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: npm

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "21"

      - name: Setup Android SDK
        uses: android-actions/setup-android@v3

      - name: Install dependencies
        run: npm ci

      - name: Validate web app (optional)
        continue-on-error: true
        run: npm run ci

      - name: Install Playwright Chromium (optional)
        continue-on-error: true
        run: npm run test:viewport:install

      - name: Run viewport matrix (optional)
        continue-on-error: true
        run: npm run test:viewport

      - name: Ensure Android platform exists
        run: |
          if [ ! -d "android/app" ]; then
            npx cap add android
          fi

      - name: Build Android APK
        env:
          BUILD_TYPE: debug
        run: ./scripts/build-android.sh

      - name: Locate APK
        id: locate_apk
        run: |
          APK_PATH=$(find android/app/build/outputs/apk -name "app-debug.apk" | head -n 1)
          if [ -z "$APK_PATH" ]; then
            echo "No APK was produced" >&2
            exit 1
          fi
          echo "path=$APK_PATH" >> "$GITHUB_OUTPUT"
          echo "Found APK: $APK_PATH"

      - name: Rename APK for release convention
        id: rename_apk
        run: |
          VERSION_TAG="${GITHUB_REF_NAME}"
          if [[ "${GITHUB_REF}" == refs/tags/v* ]]; then
            FINAL_NAME="app-prompt-${VERSION_TAG}.apk"
          else
            FINAL_NAME="app-prompt-${GITHUB_SHA::7}.apk"
          fi
          cp "${{ steps.locate_apk.outputs.path }}" "./${FINAL_NAME}"
          echo "path=./${FINAL_NAME}" >> "$GITHUB_OUTPUT"
          echo "Final APK name: ${FINAL_NAME}"

      - name: Upload APK artifact
        uses: actions/upload-artifact@v4
        with:
          name: prompt-repository-debug-apk
          path: ${{ steps.rename_apk.outputs.path }}

      - name: Create GitHub Release
        if: startsWith(github.ref, 'refs/tags/v')
        uses: softprops/action-gh-release@v2
        with:
          files: ${{ steps.rename_apk.outputs.path }}
          name: Prompt Repository ${{ github.ref_name }}
          draft: false
          prerelease: false
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## ✅ Required npm Scripts

These templates assume the target project defines the following npm scripts.

```json
{
  "scripts": {
    "android:sync": "npx cap sync android",
    "android:build:debug": "cd android && ./gradlew assembleDebug",
    "ci": "npm run build && npm test",
    "test:viewport:install": "npx playwright install chromium",
    "test:viewport": "playwright test"
  }
}
```

Adjust script commands to match your project tooling and test strategy.

---

## 💡 How to Use
1. Copy the skill prompt above.
2. Add your current React project details under **Input Context**.
3. Ask your AI assistant to execute the migration plan in phases.
4. Validate each milestone before moving to the next phase.
