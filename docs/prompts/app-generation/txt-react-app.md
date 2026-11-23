You are an expert frontend developer. Convert the following code into a modern React + Vite application.

## Tech Stack Requirements
- **React 18** with functional components and hooks
- **Vite** as the build tool
- **Tailwind CSS v3** for utility-first styling
- **shadcn/ui** for accessible UI primitives (Button, Card, Dialog, Badge, etc.)
- **Framer Motion** for animations and transitions

## Conversion Rules

### Structure
- Split logical sections into individual React components (e.g. `<Navbar />`, `<HeroSection />`, `<QuotesSection />`)
- Place components in `src/components/`
- Main composition lives in `src/App.jsx`
- Global styles in `src/index.css`

### Styling
- Replace all raw CSS classes with Tailwind utility classes
- Move custom CSS variables into `tailwind.config.js` under `theme.extend`
- Replace `<style>` block keyframe animations with Framer Motion `variants` and `animate` props
- Use `cn()` utility from shadcn for conditional class merging

### Animations
- Replace CSS `@keyframes` and `transition` with Framer Motion:
  - Use `motion.div`, `motion.section`, `motion.h1`, etc.
  - Use `variants` for staggered children
  - Use `whileHover`, `whileTap` for interactive states
  - Use `useInView` or `AnimatePresence` for scroll-triggered reveals
  - Replace `animate-spin`, `animate-pulse` with Framer Motion equivalents

### Components
- Replace plain `<button>` and `<a>` tags with shadcn `<Button>` where appropriate
- Replace modal/overlay patterns with shadcn `<Dialog>`
- Replace card-like containers with shadcn `<Card>`, `<CardContent>`, etc.
- Replace nav links with shadcn `<NavigationMenu>` if applicable

### JavaScript / State
- Convert imperative DOM manipulation (`document.getElementById`, `innerHTML`) to React state (`useState`, `useRef`)
- Convert `window.onload` logic to `useEffect`
- Convert event listeners to React synthetic event handlers
- Convert dynamic content rendering to `.map()` over state/data arrays

### Data
- Extract hardcoded data arrays (news items, quotes, etc.) into separate files: `src/data/news.js`, `src/data/quotes.js`

### File Output
Provide the following files:
1. `src/App.jsx`
2. `src/components/<ComponentName>.jsx` for each major section
3. `src/data/<dataFile>.js` for extracted data
4. `src/index.css` (only global resets and Tailwind directives)
5. `tailwind.config.js` with any custom tokens
6. `package.json` with all required dependencies

## Code to Convert:
[PASTE YOUR CODE HERE]