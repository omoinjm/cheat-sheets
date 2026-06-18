---

title: Full-Stack E-Commerce Blueprint (Next.js + Shopify)
description: A master prompt and architectural guide for building production-ready, high-performance e-commerce applications using Shopify as the commerce backend.
type: content
path: prompts/app-generation/ecommerce-blueprint-shopify.md
tags: [prompts, app-generation, ecommerce, nextjs, shopify, headless-commerce, full-stack]
------------------------------------------------------------------------------------------

# Full-Stack E-Commerce Blueprint: Next.js + Shopify

## 🔗 Navigation

* [⬆ Parent](./README.md)
* [🏠 Root](../../README.md)

## 📌 Overview

This document serves as a master prompt and architectural guide to replicate high-end, dynamic e-commerce setups. It follows **SOLID** principles, Next.js 15+ best practices, and a **Commerce-First Headless** architecture using Shopify.

Shopify acts as both:

* **Commerce Engine** (products, variants, inventory, carts, orders)
* **CMS Layer** (collections, metafields, content models)

or optionally integrates with an external CMS later.

---

## 🛠️ The Master Prompt

**Role:** Act as a Senior Full-Stack Engineer specializing in Next.js, Headless Commerce, and Shopify integrations.

**Objective:** Transform a static or Vite-based frontend into a production-ready, highly performant Next.js application powered by Shopify.

---

## Phase 1: Core Architecture & Migration

### 1. Framework

Initialize/Migrate to **Next.js 15+** using:

* `src/` directory
* **App Router**
* **Turbopack**
* Server Components by default

### 2. Styling & UI

Integrate:

* **Tailwind CSS** for utility-first styling
* **shadcn/ui** for accessible primitives
* **Framer Motion** for high-signal animation patterns:

  * stagger entrances
  * product hover interactions
  * cart drawer transitions
  * page transitions

### 3. Optimization

Implement strict performance practices:

* Next.js Image optimization (`fill`, `priority`, `sizes`)
* Lazy load below-the-fold media
* Dynamic imports for heavy client components
* Minimize client bundles
* Optimize for Core Web Vitals

Targets:

* LCP < 2.5s
* CLS < 0.1
* INP < 200ms

---

## Phase 2: Shopify Commerce Architecture

### 1. Shopify Configuration

Set up:

* Shopify Store
* Storefront API
* Admin API
* Webhooks
* Custom App for secure server-side access

Environment variables:

```env
SHOPIFY_STORE_DOMAIN=
SHOPIFY_STOREFRONT_ACCESS_TOKEN=
SHOPIFY_ADMIN_ACCESS_TOKEN=
SHOPIFY_API_VERSION=2025-10
```

Security rules:

* Never expose Admin API tokens to client
* Store secrets in `.env.local`
* Route all privileged mutations through server actions or API routes

---

### 2. Data Modeling Strategy (SOLID)

Use Shopify as the primary source of truth.

#### Products

Store:

* title
* description
* variants
* inventory
* pricing
* images
* SEO metadata

#### Collections

Use Shopify collections for categories.

Examples:

* Supplements
* Herbs
* Electronics
* Apparel

#### Metafields

Use metafields for custom structured content.

Examples:

* ingredients
* nutrition facts
* dosage
* shipping weight
* FAQ
* promotional badges

Example TypeScript model:

```ts
interface ProductMetafields {
  ingredients?: string[]
  benefits?: string[]
  dosage?: string
  faq?: string[]
}
```

---

### 3. Shopify Client Layer

Create a dedicated client:

```bash
src/lib/shopify/
```

Structure:

```bash
src/lib/shopify/
 ├── client.ts
 ├── queries.ts
 ├── mutations.ts
 ├── types.ts
 ├── cart.ts
 └── products.ts
```

Responsibilities:

#### client.ts

* GraphQL communication
* request handling
* caching

#### queries.ts

* Read-only GraphQL queries

#### mutations.ts

* Cart/order mutations

#### cart.ts

Business logic:

* add item
* remove item
* update quantity

---

### 4. Data Fetching

Replace all client-side fetching with **Async Server Components**.

Example routes:

```bash
/app
 ├── page.tsx
 ├── products
 │   └── [handle]
 │       └── page.tsx
 ├── collections
 │   └── [handle]
 │       └── page.tsx
```

Use:

* Storefront GraphQL API
* ISR
* Route cache
* Server Actions

Example:

```ts
export const revalidate = 60
```

Fetch using GraphQL queries optimized for minimal payload.

---

## Phase 3: Cart, Checkout & Payments (Shopify Native)

### 1. Cart Infrastructure

Implement persistent carts using Shopify Cart API.

Features:

* add/remove/update items
* apply discount codes
* shipping estimation
* tax estimation
* cart persistence via cookies/local storage

Cart state strategy:

#### Server

* cart creation
* mutations

#### Client

* optimistic UI
* cart drawer
* local cache

---

### 2. Checkout Flow

Use Shopify Checkout.

Benefits:

* PCI compliant
* payment providers already integrated
* fraud protection
* tax calculations
* shipping calculations

Flow:

1. User adds items to cart
2. Cart mutation creates checkout URL
3. Redirect to Shopify checkout
4. Payment handled by Shopify
5. Webhook confirms order completion

Example mutation:

```graphql
mutation cartCheckoutCreate {
  cartCreate {
    cart {
      checkoutUrl
    }
  }
}
```

---

### 3. Webhooks

Implement webhook endpoints:

```bash
/api/webhooks
```

Handle:

* order creation
* payment success
* refunds
* fulfillment updates
* inventory changes

Example events:

* orders/create
* orders/paid
* orders/fulfilled
* products/update

Use HMAC verification.

---

## Phase 4: Advanced Commerce Features

### Search & Filtering

Implement:

* collection filtering
* price range
* availability
* variant filtering
* sorting

Examples:

* newest
* best selling
* price ascending
* price descending

---

### Personalization

Optional features:

* recently viewed products
* AI recommendations
* upsells
* cross-sells
* abandoned cart recovery

Examples:

* “Frequently Bought Together”
* “Customers Also Bought”

---

### Inventory Awareness

Display:

* in stock
* low stock
* out of stock
* preorder

Use inventory quantities from Shopify.

---

## Phase 5: Engineering Standards

### SOLID Principles

Single Responsibility examples:

* `ProductPage.tsx` → UI only
* `page.tsx` → data fetching only
* `shopify/products.ts` → domain logic only

Open/Closed:

```ts
interface CommerceProvider {
  getProducts(): Promise<Product[]>
  createCart(): Promise<Cart>
  checkout(cart: Cart): Promise<string>
}
```

Supports future providers:

* Shopify
* Medusa
* Commerce Layer
* BigCommerce

---

### Security

Move all secrets into:

```env
.env.local
```

Never expose:

* Admin API tokens
* webhook secrets
* internal APIs

Implement:

* HMAC verification
* rate limiting
* bot protection

---

### Maintainability

Use:

* absolute imports (`@/...`)
* shared interfaces
* strict TypeScript
* domain separation

Structure:

```bash
src/data/
src/types/
```

Example:

```ts
interface Product {
  id: string
  title: string
  handle: string
  price: number
  compareAtPrice?: number
  images: string[]
}
```

---

## Optional Enhancements

### CMS Hybrid Mode

If Shopify content editing becomes limiting, add a CMS later:

* Shopify + Sanity
* Shopify + Contentful
* Shopify + Payload

Pattern:

* Shopify → commerce
* CMS → marketing content

---

### International Commerce

Support:

* multiple currencies
* multiple languages
* regional pricing
* localized tax logic

Examples:

* ZAR
* USD
* GBP

---

### Analytics & Monitoring

Integrate:

* GA4
* Meta Pixel
* TikTok Pixel
* Sentry
* PostHog

Track:

* conversion rate
* abandoned carts
* AOV
* checkout drop-off

---

## 📋 Execution Checklist

* [ ] Remove hardcoded product arrays
* [ ] Connect all product pages to Shopify Storefront API
* [ ] Verify cart persistence across refreshes
* [ ] Validate Shopify checkout redirect
* [ ] Test webhook order flow
* [ ] Run `next build`
* [ ] Verify ISR and caching
* [ ] Confirm non-technical staff can manage products in Shopify Admin
