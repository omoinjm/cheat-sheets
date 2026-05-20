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
>
> **Expected Deliverables:**
> - Target folder structure for the migrated app
> - A prioritized migration checklist with milestones
> - Updated dependency map (keep, replace, remove)
> - Key configuration files to create or modify
> - Performance and security hardening checklist
> - Post-migration validation checklist for Android and iOS

---

## 💡 How to Use
1. Copy the skill prompt above.
2. Add your current React project details under **Input Context**.
3. Ask your AI assistant to execute the migration plan in phases.
4. Validate each milestone before moving to the next phase.
