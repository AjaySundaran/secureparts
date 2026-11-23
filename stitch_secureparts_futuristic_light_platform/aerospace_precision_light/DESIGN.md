---
name: Aerospace Precision Light
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#434655'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#0060ac'
  on-secondary: '#ffffff'
  secondary-container: '#64a8fe'
  on-secondary-container: '#003c70'
  tertiary: '#005b7c'
  on-tertiary: '#ffffff'
  tertiary-container: '#00759f'
  on-tertiary-container: '#e1f2ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#d4e3ff'
  secondary-fixed-dim: '#a4c9ff'
  on-secondary-fixed: '#001c39'
  on-secondary-fixed-variant: '#004883'
  tertiary-fixed: '#c4e7ff'
  tertiary-fixed-dim: '#7bd0ff'
  on-tertiary-fixed: '#001e2c'
  on-tertiary-fixed-variant: '#004c69'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '600'
    lineHeight: 48px
    letterSpacing: -0.025em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.005em
  label-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.04em
  code-mono:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system delivers an ultra-pure, light-mode enterprise environment tailored for mission-critical supply chains, defense logistics, and advanced hardware manufacturing. Drawing from Apple-caliber industrial refinement and modern high-end aerospace interfaces, the aesthetic balances sterile optical cleanliness with subtle kinetic warmth. 

The visual identity relies on surgical layout discipline: strict geometric alignments, abundant white breathing room, translucent structural tiers, and precise micro-accents. Key emotional markers are absolute structural integrity, state-of-the-art computational velocity, and effortless clarity. Interactions feel frictionless and weighted—resembling calibrated glass instruments over mechanical assemblies. Dark background inversions are omitted entirely; contrast and focal depth are driven purely through optical shifts in high-value blues, icy translucent fills, and delicate edge luminescence.

## Colors

The color architecture enforces a high-luminance environment structured around crisp blues and clinical neutral tones.

- **Primary Canvas (`#FFFFFF`):** Base layer for default viewport backgrounds, active card sheets, and primary input fields.
- **Secondary Canvas (`#F5F8FC`):** Recessed ground plane for application wrappers, table headers, master-detail sidebars, and structural wells.
- **Alternative Canvas (`#EDF5FF`):** Tinted structural layer reserved for highlighted modules, feature panels, active drop zones, and verified system alerts.
- **Primary Brand Blue (`#2563EB`):** High-intent interactive trigger, primary buttons, confirmed validation status, and dominant key focus states.
- **Secondary Blue (`#60A5FA`):** Structural framing, active selection tabs, and subtle edge lighting.
- **Accent Cyan (`#38BDF8`):** Live telemetry indicators, micro-badges, data stream highlights, and laser-precise focus rings.
- **Heading Text (`#172B4D`):** Deep cobalt-graphite ink providing high-contrast readability across all white and tinted surfaces.
- **Body & Metadata (`#64748B`):** Muted slate neutral delivering balanced hierarchy without optical vibration.
- **Subtle Border (`#E2EAF4`):** Crisp structural line work separating surfaces without visual clutter.

## Typography

The typography leverages Inter to emulate the clean, neutral authority of modern system-level enterprise software. Precision tracking and tight vertical metrics eliminate ambient visual drift. 

Headings command strong presence via tight negative tracking (`-0.025em` down to `-0.01em`) and medium-to-semibold weights, rendered exclusively in deep `#172B4D`. Body copy maintains absolute legibility in `#64748B`, while interactive labels and table metadata employ medium weights with subtle uppercase tracking on sub-12px badges (`label-sm`). For serial numbers, crypto hashes, part identifiers, and telemetry specs, fallback to `JetBrains Mono` maintains monospace tabular alignment.

## Layout & Spacing

The layout model uses a responsive 12-column fluid grid pegged to a 1440px desktop frame with a strict 4px/8px vertical rhythm. 

- **Desktop (1024px+):** 12-column grid, 24px (`1.5rem`) gutters, and 32px (`2rem`) side margins. Complex engineering dashboards utilize fluid data grids with sticky sidebar mechanics.
- **Tablet (768px - 1023px):** 8-column layout, 16px (`1rem`) gutters, and 24px (`1.5rem`) outer canvas margins. Multi-column metric panels reflow to 2x2 configurations.
- **Mobile (< 768px):** 4-column layout, 16px (`1rem`) gutters, and 16px (`1rem`) margins. Complex telemetry tables collapse into modular stacked cards.

Vertical composition prioritizes generous whitespace to ensure complex logistical datasets feel airy rather than crowded.

## Elevation & Depth

Spatial depth avoids heavy pitch-black shadows, relying on layered optical clarity: multi-tier glassmorphism, hyper-diffused ambient blue shadows, and sub-pixel structural borders.

- **Level 0 (Flat Ground):** Base page canvases (`#FFFFFF` or `#F5F8FC`) with zero elevation.
- **Level 1 (Card & Section Containers):** Background `#FFFFFF` with 88% opacity and `backdrop-filter: blur(16px)`. Framed by a 1px solid border in `#E2EAF4`. Base shadow: `0 1px 3px rgba(37, 99, 235, 0.04), 0 6px 16px rgba(23, 43, 77, 0.03)`.
- **Level 2 (Hover States & Active Units):** Background `#FFFFFF` with 94% opacity and `backdrop-filter: blur(20px)`. Enhanced ambient illumination: `0 4px 12px rgba(37, 99, 235, 0.06), 0 12px 28px rgba(37, 99, 235, 0.05)`. Border shifts slightly toward `#60A5FA` at 40% opacity.
- **Level 3 (Modals, Overlays, Floating Controls):** Solid `#FFFFFF` or 96% frosted acrylic backdrop with an ambient cyan glow: `0 12px 32px -4px rgba(37, 99, 235, 0.12), 0 4px 16px rgba(56, 189, 248, 0.08)`. Border utilizes `#E2EAF4`.

## Shapes

The geometric framework uses consistent curvature matching modern high-precision hardware:
- Base components (inputs, list items, action buttons) apply a uniform 8px radius (`0.5rem`).
- Module panels, modal sheets, and primary enterprise cards leverage 16px (`1rem` / `rounded-lg`).
- High-level viewport groupings and floating application sheets scale to 24px (`1.5rem` / `rounded-xl`).
- Status pills, tracking chips, and micro-avatars use full circular radius (`9999px`).

## Components

### Buttons
- **Primary:** Background `#2563EB`, text `#FFFFFF`, borderless with subtle inner upper highlight (`inset 0 1px 0 rgba(255, 255, 255, 0.2)`). On hover: `#1D4ED8` with a soft ambient blue glow (`0 4px 14px rgba(37, 99, 235, 0.25)`).
- **Secondary:** Frosted background `#FFFFFF`, text `#172B4D`, border 1px solid `#E2EAF4`. On hover: background `#F5F8FC`, border `#60A5FA`.
- **Ghost:** Transparent background, text `#64748B`. On hover: text `#172B4D`, background `#EDF5FF`.

### Cards & Panels
- Constructed from `#FFFFFF` frosted glass (`backdrop-filter: blur(16px)`), bordered by 1px `#E2EAF4`, resting on `rounded-lg` (16px).
- Internal margins use `space-lg` (24px). Headers separate body content using a clean 1px `#E2EAF4` dividing rule without dark gradients.

### Input Fields & Controls
- **Inputs:** Background `#FFFFFF`, height 40px, padding 0 12px, border 1px solid `#E2EAF4`, text `#172B4D`, placeholder `#64748B`. Focused state applies border `#2563EB` along with a distinct focus ring: `0 0 0 3px rgba(56, 189, 248, 0.25)`.
- **Checkboxes & Radios:** 16px frame with 1px solid `#CBD5E1`. When selected, fills with `#2563EB` bearing a crisp white glyph.
- **Chips & Badges:** Height 24px, 8px padding, pill-shaped. Verified state: background `#EDF5FF`, text `#2563EB`, border 1px solid rgba(96, 165, 250, 0.3). Live/Telemetry state: text `#0369A1` with an active pulsing `#38BDF8` 6px dot.

### Tables & Data Grids
- Header row rests on `#F5F8FC` with `label-sm` uppercase text in `#64748B`.
- Rows feature 1px bottom border in `#E2EAF4`. Hovering transitions background seamlessly to `#EDF5FF` at 50% opacity. Monospace serial tags render in `code-mono` with subtle `#EDF5FF` pill backgrounds.