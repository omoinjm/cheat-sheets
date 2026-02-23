---
title: Full-Stack E-Commerce Blueprint (Next.js + Sanity + Stripe)
description: A master prompt and architectural guide for building production-ready, high-performance e-commerce applications with headless CMS and fintech integration.
type: content
path: prompts/app-generation/ecommerce-blueprint.md
tags: [prompts, app-generation, ecommerce, nextjs, sanity-cms, stripe, fintech, full-stack]
---
# Full-Stack E-Commerce Blueprint: Next.js + Sanity + Stripe

## 🔗 Navigation
- [⬆ Parent](./README.md)
- [🏠 Root](../../README.md)

## 📌 Overview
This document serves as a master prompt and architectural guide to replicate high-end, dynamic e-commerce setups. It follows **SOLID** principles, Next.js 15+ best practices, and a "Headless-First" philosophy.

---

## 🛠️ The Master Prompt

**Role:** Act as a Senior Full-Stack Engineer specializing in Next.js, Headless CMS, and Fintech integrations.

**Objective:** Transform a static or Vite-based frontend into a production-ready, highly performant Next.js application powered by Sanity CMS and Stripe.

### Phase 1: Core Architecture & Migration
1.  **Framework:** Initialize/Migrate to **Next.js 15+** using the `src` directory, **App Router**, and **Turbopack**.
2.  **Styling & UI:** 
    *   Integrate **Tailwind CSS** for utility-first styling.
    *   Install and configure **shadcn/ui** for accessible, low-level components.
    *   Use **Framer Motion** for sophisticated, high-signal animations (e.g., fade-ins, stagger effects).
3.  **Optimization:** Implement strict Next.js Image optimization (using `fill`, `priority`, and calculated `sizes` props) to ensure perfect Core Web Vitals.

### Phase 2: Headless CMS Strategy (Sanity)
1.  **Configuration:** 
    *   Embed **Sanity Studio v5** directly into the Next.js app at `/studio`.
    *   Configure a robust client with environment variable protection and **ISR (Incremental Static Regeneration)** using `revalidate = 60`.
2.  **Schema Design (SOLID):**
    *   **Singletons:** Create a `siteSettings` schema for global elements (Logo, Nav, Socials).
    *   **Documents:** Define `product`, `category`, and `pageContent` schemas.
    *   **References:** Use Sanity references for relationships (e.g., `product -> category`) rather than hardcoded strings.
3.  **Migration Pipeline:**
    *   Write a custom TypeScript migration script using `@sanity/client`.
    *   Automate the transformation of static assets (local images) into Sanity Assets.
    *   Convert hardcoded data structures into dynamic Sanity documents.
4.  **Data Fetching:**
    *   Replace all `use client` data fetching with **Async Server Components**.
    *   Use optimized GROQ queries with joins to minimize requests.

### Phase 3: Payment & Fintech (Stripe)
1.  **Infrastructure:**
    *   Set up a secure Stripe client on the server.
    *   Implement **Stripe Checkout** for a seamless, PCI-compliant payment flow.
2.  **API Routes:**
    *   Create `api/checkout` routes to generate secure sessions.
    *   Implement a **Stripe Webhook** handler at `api/webhooks` to handle asynchronous events (payment success, fulfillment).
3.  **Dynamic Pricing:** Map Sanity `price` fields directly to Stripe Line Items.

### Phase 4: Engineering Standards
*   **SOLID Principles:** Ensure Single Responsibility (e.g., `ShopContent.tsx` handles UI, `page.tsx` handles data).
*   **Security:** Rigorously move all sensitive keys (Sanity Write Tokens, Stripe Secrets) to `.env.local`.
*   **Maintainability:** Use absolute imports (`@/...`) and shared TypeScript interfaces in `src/data/`.

---

## 📋 Execution Checklist

- [ ] **Cleanup:** Remove hardcoded arrays from `src/data/` once migration is verified.
- [ ] **SEO:** Bind Sanity `siteSettings` to the root `layout.tsx` Metadata object.
- [ ] **Performance:** Run `next build` to verify all routes are statically generated or using ISR.
- [ ] **Validation:** Ensure Sanity Studio is accessible and editors can update content without developer intervention.
