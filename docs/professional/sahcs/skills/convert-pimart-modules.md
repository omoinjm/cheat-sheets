# PIMART PowerPoint → Word — Skill Export

This is a single-file markdown export of the `pimart-pptx-to-docx` skill
(normally packaged as three files: `SKILL.md`, `references/style-guide.md`,
`scripts/docx_helpers.js`). Combined here for easy reading/copying outside
the `.skill` format.

---

## 1. SKILL.md

---
name: pimart-pptx-to-docx
description: Convert a PIMART training-module PowerPoint (e.g. "16__PIMART_Safer_conception_....pptx", "17_1_PIMART_Contraception_....pptx") into a Word document that follows the established PIMART module structure — title/CONTENTS/Learning outcomes front matter, blue section headings, bulleted body text, flattened diagram images, boxed callouts, and a References list. Use this whenever the user uploads a PIMART (or similarly named training-module) .pptx and asks for a Word/.docx version, asks to "convert" it, or asks to produce a module document "using this structure." Also use it to update/extend a module document when a new or corrected .pptx for that same module is provided later.
---

# PIMART PowerPoint → Word module document

Converts a PIMART training-module slide deck into a Word document with a
consistent, previously-established house style. The style was reverse-
engineered from a human-produced reference document (`PIMART_Module_16_VM.docx`)
that was cross-checked slide-by-slide against its source deck and found to
match almost exactly — so the patterns below are the real target, not a guess.

Read `references/style-guide.md` before writing any XML/docx-js — it has the
exact colors, sizes, and paragraph patterns. Use `scripts/docx_helpers.js` as
a starting point for the build script; it implements those patterns as
ready-to-call functions.

## When to use this

- The user uploads a `.pptx` for a PIMART module (filenames look like
  `<module>_<part?>_PIMART_<topic>_<date>_Final.pptx`) and wants a Word
  document out of it.
- The user has previously shared (or shares now) a "structure" `.docx` to
  match — treat that as the style template, not just a content reference.
- A follow-up `.pptx` arrives for a module already converted in this
  conversation — extend/update the existing docx rather than starting over
  (see "Updating an existing module doc" below).

## Step-by-step workflow

### 1. If a reference/structure `.docx` is provided, reverse-engineer it first

Don't just skim it — extract its exact formatting before building anything:

```bash
pandoc -t markdown reference.docx -o reference.md      # content + image order
mkdir ref_extract && cd ref_extract && unzip -q reference.docx -d .
```

Then read `word/document.xml` directly (regex out `<w:p>` blocks, look at the
`<w:pStyle>`/`<w:rPr>` on each) to get the real color hex codes, font sizes,
and paragraph spacing — pandoc strips all of this. See
`references/style-guide.md` for the values found for the PIMART style; treat
them as defaults but re-derive them from any newly-provided reference doc,
since values can change between templates.

Also render the reference to images so you can see the finished layout,
especially for anything pandoc can't show (flattened diagrams, colored boxes,
side-by-side columns):

```bash
python /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf reference.docx
pdftoppm -jpeg -r 100 reference.pdf refpage
```

View each `refpage-N.jpg`. For every image embedded in the doc, open it
directly (`view` the PNG in `word/media/`) — this is the only way to tell
whether an image is a flattened multi-element diagram (title + icons + a
citation baked into one picture) or a simple photo. That distinction drives
step 3 below.

### 2. Extract everything from the source `.pptx`

```python
from pptx import Presentation
prs = Presentation('deck.pptx')
for i, slide in enumerate(prs.slides, 1):
    for shape in slide.shapes:
        if shape.has_text_frame and shape.text_frame.text.strip():
            ...  # collect text, keyed by shape name/order
        if shape.shape_type == 13:  # PICTURE
            ...  # note size/position
        if shape.has_table:
            ...  # collect table rows
    if slide.has_notes_slide:
        ...  # speaker notes (generally NOT included in the Word doc)
```

Also unzip the pptx and map each slide's pictures to media files, and pull
hyperlink targets out of each slide's `.rels` file (`grep -o 'r:id="[^"]*"'`
on the slide XML, cross-reference with the `.rels` — text runs alone don't
show you the URL, only the relationship does):

```bash
unzip -q deck.pptx -d pptx_extract
cat pptx_extract/ppt/slides/_rels/slideN.xml.rels | grep -o 'Target="[^"]*"'
```

**View every picture** referenced from a slide (`view` each media file) before
deciding how to handle it — file size/dimensions alone won't tell you if it's
a data-bearing diagram or a decorative stock photo.

### 3. Decide, slide by slide, how each becomes Word content

This is the core judgment call. Use these rules, in order:

| Slide content | Word treatment |
|---|---|
| Plain heading + bulleted text (even nested) | Live heading + live bullets — fully editable text, matching styles below |
| A diagram built from multiple shapes (icon circles, arrows, a flowchart, a multi-part infographic) where the meaning comes from the *layout*, not just the text | Flatten to a single image. If a matching reference doc already has the exact same diagram pre-cropped, reuse that image file directly (confirm visually first). Otherwise render the slide and crop out the title bar / margins. |
| A short quote/definition box, a colored "note" or "however" callout | A bordered/shaded box (table or shape) reproducing the box text — see style guide for exact colors used per box type |
| A citation line ("Source: X", "Adapted from: Y") | A single small underlined-label line placed right after the content it supports |
| A references/resources slide | A flat bulleted list, each entry hyperlinked to its real URL if one exists in the slide's `.rels` |
| A purely decorative photo, background texture, clip-art icon strip, or a title-page background/logo | **Omit.** The reference material consistently drops these — they carry no content. |
| A section-divider slide (title only, no body) immediately followed by a content slide | Merge under one heading — see "Two heading styles" in the style guide for how the *first* sub-slide right after a divider is styled slightly differently from later ones |
| "Congratulations, you've completed this module" closer slide | Omit — not included in the reference material |

When in doubt about whether something is decorative vs. informative, check
whether the reference doc (if any) included an equivalent image from an
equivalent slide in a prior module — it's a reliable precedent.

### 4. Verify content parity before building

If there's a reference doc, do a text diff to catch any real differences
(new bullets, updated numbers, changed guidance) versus artifacts of line
wrapping:

```python
# normalize both texts (strip markdown, whitespace, non-breaking spaces),
# split to lines, diff as sets — real differences are short and substantive;
# artifacts are line-break/whitespace noise. Read every genuine diff line by
# eye before deciding it's new content.
```

Report any genuine content differences to the user — don't silently choose
one version.

### 5. Build the document

Use `scripts/docx_helpers.js` (docx-js) with the color/size/spacing constants
from `references/style-guide.md`. Structure, in order:

1. Title block: `Module <N>` (bold, blue) / topic name (blue, not bold)
2. `CONTENTS` heading + bullets (one per top-level section in the deck,
   taken from the deck's own contents/agenda slide)
3. `Learning outcomes` heading + bullets
4. One block per section, following the table in step 3
5. `References & resources` (or equivalent) as the final bulleted, hyperlinked
   list, if the deck has one

### 6. Render and visually QA

```bash
python /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf out.docx --outdir check/
pdftoppm -jpeg -r 100 check/out.pdf check/pg
```

View every page image. Check: headings are the right color/weight, bullets
nested correctly, images present and not stretched, hyperlinks underlined,
no orphaned section headers at the bottom of a page with no content.

### 7. Deliver

Copy to `/mnt/user-data/outputs/` and call `present_files`. In your reply,
proactively flag anything the user should know:
- If the source deck only covers part of the module (e.g. a `17_1` file
  covering just one sub-section of a 6-part CONTENTS list), say so explicitly.
- If a reference doc was provided and its content already matched the deck
  almost exactly, say that plainly rather than implying you built everything
  from scratch.
- Any genuine content differences found in step 4.

## Updating an existing module doc

If a new/corrected `.pptx` arrives for a module already converted earlier in
the conversation:
1. Re-run steps 2–4 against the new deck.
2. Diff the new content against what's already in the built docx (not the
   original reference — the docx you produced is now the source of truth).
3. Edit only the affected sections (unzip → edit `word/document.xml` → 
   rezip — see the main `docx` skill for the edit workflow), rather than
   rebuilding the whole document from scratch.
4. Re-render and re-QA the whole document, not just the changed pages, since
   pagination can shift.

## Multi-part modules

Some modules are split across several files (`17_1_...`, `17_2_...`, etc.).
When asked to add a later part to a module already converted, append its
sections to the existing document under the same title block and CONTENTS
list rather than creating a second file — check the CONTENTS bullets against
what's now actually covered and note in your reply if some listed topics are
still missing.
-e 
---

## 2. references/style-guide.md

# PIMART module document — style guide

Derived from `PIMART_Module_16_VM.docx` (reference doc, verified against its
source deck) and applied to Module 17. Re-derive/confirm these values from
any newly-supplied reference doc rather than assuming they never change —
but absent a new reference, these are the defaults.

## Fonts and base sizes

- Font throughout: **Calibri**
- Body text: 11pt (`sz`/`szCs` = 22 half-points) — this is Word's default
  Normal style, so it often doesn't need to be set explicitly
- Headings and title-block lines: 13pt (`sz`/`szCs` = 26 half-points)

## Colors (hex, no `#`)

| Element | Color | Notes |
|---|---|---|
| Section headings ("blue heading") | `4C94D8` | Used for every slide-title-derived heading: title-block lines, CONTENTS, Learning outcomes, and each major section header |
| Bold sub-heading (e.g. "Safer conception") | default black (`000000`), **bold** | Used for the *first* content slide's title immediately following a section-divider slide — see "Two heading styles" below |
| Body bullets | default black in most sections; some source sections use a dark teal `133B43` — this appears to be a deliberate section accent, not an error; when unsure, default to plain black | |
| Callout/box text | varies by box — see "Boxes" below | |
| Hyperlinks | standard Word `Hyperlink` character style (blue, underlined) | |

## Two heading styles — when to use bold-black vs. blue

Every slide title in the deck becomes a heading in the doc, styled blue
13pt **except** the very first content-slide title that immediately follows
a section-divider slide (a slide that's just a title with no body — e.g.
"Pre-conception management for the HIV affected couple" in Module 16). That
one divider gets the normal blue 13pt heading, but the *next* slide's title
(the first one with actual body content, e.g. "Safer conception") is styled
as bold-black 11pt instead, so you don't get two blue headings back-to-back
with nothing but a page-fold between them. All headings *after* that one go
back to blue 13pt.

If a module doesn't have this divider-then-content pattern (e.g. Module 17's
`17.1 Background` is itself the divider, and its first content slide
"Preventing unintended pregnancies" is the bold-black one), apply the same
rule: divider = blue, its first child = bold-black, everything else = blue.

## Bullets

Three levels, standard Word list glyphs:
- Level 0: `•` (solid round bullet)
- Level 1: `o` (open circle)
- Level 2: `▪` (small square)

Indent roughly 0.25in per level, hanging indent = bullet width. No blank
paragraph between consecutive bullets; use one empty spacer paragraph
between distinct subsections (e.g. after a bullet list, before the next
sub-heading).

## Title block

```
Module <N>          -> bold, blue, 13pt
<Topic name>         -> blue, 13pt, NOT bold
CONTENTS             -> blue, 13pt
  • <bullet per top-level section from the deck's own contents slide>
Learning outcomes    -> blue, 13pt
  • <bullet per learning outcome from the deck>
```

## Source / citation lines

A short line crediting a source, placed directly under the content it
supports:

```
Source: <citation>            (or "Adapted from: <citation>")
```

- The label ("Source: " / "Adapted from: ") is **underlined**
- If the citation was a hyperlink in the deck, keep it as one
- Not bulleted — its own plain paragraph, slightly indented/centered
  under an image where relevant

## Boxes / callouts

Three variants seen in the reference material:

1. **Plain bordered box, no fill** — a thin black border around centered
   bold-ish text. Used for neutral operational notes
   (e.g. "Oral PrEP is safe in pregnancy... but... refer these clients").
2. **Shaded grey box, no border, bold text** — used for short imperative
   statements ("However, only oral PrEP will be available in the pharmacy
   setting"). Fill approx. `F2F2F2`.
3. **Shaded + colored-border box** — used for the most important
   operational instruction on a page (referral instructions). Green fill
   with a dark red border in the Module 16 example — treat the exact
   color pairing as illustrative, not a fixed rule; what matters is that
   the single most action-critical instruction on a page gets the
   strongest visual treatment on that page.

Implement boxes as a one-cell table with shading/border set on the cell,
per the `docx` skill's guidance (never use `ShadingType.SOLID`, always
`ShadingType.CLEAR` with the fill color).

## Images

- Full body width, centered: target width **6.27in** (matches the
  reference doc's embedded images — this is essentially "fill the text
  column").
- Flattened diagrams are inserted with **no visible border/caption
  paragraph** other than the source line described above.
- Never stretch — preserve aspect ratio; compute height from the
  original image's aspect ratio at 6.27in width.

## Page setup

- US Letter: `width: 12240, height: 15840` (DXA) — do not use docx-js's A4
  default.

## What gets omitted (established by precedent, not stated by the user)

- Purely decorative photography (stock photos of people, textured
  backgrounds, title-page/logo art)
- Icon strips / clip-art rows with no accompanying data
- Closing "Congratulations, you've completed this module" slides
- Speaker notes (unless the user asks for them separately)
-e 
---

## 3. scripts/docx_helpers.js

```javascript
/**
 * Reusable building blocks for PIMART module documents (docx-js).
 *
 * Usage:
 *   const H = require('./docx_helpers');
 *   const { Document, Packer } = require('docx');
 *   const fs = require('fs');
 *
 *   const doc = new Document({
 *     numbering: H.numberingConfig,
 *     sections: [{
 *       properties: { page: { size: H.US_LETTER } },
 *       children: [
 *         ...H.titleBlock('17', 'Contraception', contentsBullets, outcomeBullets),
 *         H.headingPara('17.1 Background'),
 *         H.subBoldHeading('Preventing unintended pregnancies'),
 *         H.bullet('Unintended pregnancies contribute to ...'),
 *         ...
 *       ],
 *     }],
 *   });
 *   Packer.toBuffer(doc).then(buf => fs.writeFileSync('out.docx', buf));
 *
 * See references/style-guide.md for the design rationale behind every
 * value here (colors, sizes, when to use headingPara vs subBoldHeading,
 * box variants, etc). Don't change these constants without re-reading
 * that doc — they were reverse-engineered from an approved reference file.
 */
const {
  Paragraph, TextRun, ExternalHyperlink, LevelFormat, AlignmentType,
  convertInchesToTwip, Table, TableRow, TableCell, WidthType, ShadingType,
  BorderStyle, ImageRun,
} = require("docx");

const CALIBRI = "Calibri";
const BLUE = "4C94D8";
const US_LETTER = { width: 12240, height: 15840 };

const numberingConfig = {
  config: [
    {
      reference: "main-bullets",
      levels: [
        { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: convertInchesToTwip(0.25), hanging: convertInchesToTwip(0.25) } } } },
        { level: 1, format: LevelFormat.BULLET, text: "o", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: convertInchesToTwip(0.75), hanging: convertInchesToTwip(0.25) } } } },
        { level: 2, format: LevelFormat.BULLET, text: "\u25AA", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: convertInchesToTwip(1.25), hanging: convertInchesToTwip(0.25) } } } },
      ],
    },
  ],
};

// Blue 13pt heading -- every slide-title-derived heading EXCEPT the first
// content slide right after a section-divider slide (use subBoldHeading
// for that one). See style-guide.md "Two heading styles".
function headingPara(text) {
  return new Paragraph({
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text, font: CALIBRI, size: 26, color: BLUE })],
  });
}

// Bold black 11pt -- the one exception described above, and also usable
// as a generic in-section sub-label (e.g. "Reduces:" / "Increases and
// supports:").
function subBoldHeading(text) {
  return new Paragraph({
    spacing: { after: 80 },
    children: [new TextRun({ text, font: CALIBRI, size: 22, bold: true })],
  });
}

function body(text, opts = {}) {
  return new Paragraph({
    spacing: { after: opts.after ?? 120, line: 276 },
    children: [new TextRun({ text, font: CALIBRI, size: 22, italics: opts.italics, bold: opts.bold })],
  });
}

function bullet(text, level = 0, opts = {}) {
  return new Paragraph({
    numbering: { reference: "main-bullets", level },
    spacing: { after: 0, line: 276 },
    children: [new TextRun({ text, font: CALIBRI, size: 22, bold: opts.bold, color: opts.color })],
  });
}

// A "Source: X" / "Adapted from: X" citation line. label should include
// the trailing ": " e.g. "Source: " -- it is rendered underlined, cite is not.
function sourceLine(label, cite) {
  return new Paragraph({
    spacing: { before: 120, after: 200 },
    children: [
      new TextRun({ text: label, font: CALIBRI, size: 22, underline: {} }),
      new TextRun({ text: cite, font: CALIBRI, size: 22 }),
    ],
  });
}

// A bulleted reference/resource line with a real hyperlink.
function linkBullet(preText, linkText, url, level = 0) {
  const children = [];
  if (preText) children.push(new TextRun({ text: preText, font: CALIBRI, size: 22 }));
  children.push(new ExternalHyperlink({
    link: url,
    children: [new TextRun({ text: linkText, font: CALIBRI, size: 22, style: "Hyperlink" })],
  }));
  return new Paragraph({
    numbering: { reference: "main-bullets", level },
    spacing: { after: 100, line: 276 },
    children,
  });
}

function spacer() {
  return new Paragraph({ text: "", spacing: { after: 120 } });
}

// Full-width centered image. Pass the aspect-ratio-correct height you
// computed from the source file -- never stretch to a fixed height.
function fullWidthImage(path, widthIn, heightIn) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 120 },
    children: [
      new ImageRun({
        type: path.split(".").pop() === "jpg" ? "jpg" : "png",
        data: require("fs").readFileSync(path),
        transformation: {
          width: convertInchesToTwip(widthIn) / 15, // EMU-ish px approximation; prefer computing from DPI in practice
          height: convertInchesToTwip(heightIn) / 15,
        },
      }),
    ],
  });
}

// Variant 1: plain bordered box, no fill -- neutral operational note.
function borderedBox(text, opts = {}) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [new TableRow({ children: [new TableCell({
      children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text, font: CALIBRI, size: 22, bold: opts.bold ?? true })],
      })],
      shading: { type: ShadingType.CLEAR, fill: "FFFFFF" },
      borders: allBorders("000000", 8),
      margins: { top: 100, bottom: 100, left: 150, right: 150 },
    })] })],
  });
}

// Variant 2: shaded grey box, no border, bold text -- short imperative statement.
function shadedBox(text, fill = "F2F2F2") {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [new TableRow({ children: [new TableCell({
      children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text, font: CALIBRI, size: 22, bold: true })],
      })],
      shading: { type: ShadingType.CLEAR, fill },
      borders: allBorders(fill, 2),
      margins: { top: 100, bottom: 100, left: 150, right: 150 },
    })] })],
  });
}

// Variant 3: shaded + colored border -- the single most action-critical
// instruction on a page. Default colors match the Module 16 referral box;
// override for other modules as appropriate.
function highlightBox(text, opts = {}) {
  const fill = opts.fill ?? "E2EFDA";
  const border = opts.border ?? "7F030C";
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [new TableRow({ children: [new TableCell({
      children: text.split("\n").map(line => new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 100 },
        children: [new TextRun({ text: line, font: CALIBRI, size: 22, bold: true })],
      })),
      shading: { type: ShadingType.CLEAR, fill },
      borders: allBorders(border, 12),
      margins: { top: 150, bottom: 150, left: 200, right: 200 },
    })] })],
  });
}

function allBorders(color, size) {
  const side = { style: BorderStyle.SINGLE, size, color };
  return { top: side, bottom: side, left: side, right: side };
}

// Title block: Module N / Topic / CONTENTS bullets / Learning outcomes bullets.
// contentsBullets and outcomeBullets are plain string arrays.
function titleBlock(moduleNumber, topic, contentsBullets, outcomeBullets) {
  return [
    new Paragraph({ children: [new TextRun({ text: `Module ${moduleNumber}`, font: CALIBRI, size: 26, bold: true, color: BLUE })] }),
    new Paragraph({ children: [new TextRun({ text: topic, font: CALIBRI, size: 26, color: BLUE })] }),
    new Paragraph({ spacing: { before: 120 }, children: [new TextRun({ text: "CONTENTS", font: CALIBRI, size: 26, color: BLUE })] }),
    ...contentsBullets.map(t => bullet(t)),
    spacer(),
    headingPara("Learning outcomes"),
    ...outcomeBullets.map(t => bullet(t)),
    spacer(),
  ];
}

module.exports = {
  CALIBRI, BLUE, US_LETTER, numberingConfig,
  headingPara, subBoldHeading, body, bullet, sourceLine, linkBullet, spacer,
  fullWidthImage, borderedBox, shadedBox, highlightBox, titleBlock,
};
-e 
```
