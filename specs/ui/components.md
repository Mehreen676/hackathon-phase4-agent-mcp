# UI Spec – Components & Visual Style (Phase II)

## Design Goals (Must-Have)
- Modern, professional, colorful (premium SaaS feel)
- Clean spacing, consistent typography
- Fully responsive (mobile-first)
- Clear visual hierarchy (headings, cards, buttons)
- Accessible contrast and readable text

## Brand / Theme (Guideline)
- App feel: "Task dashboard" with friendly color accents
- Use Tailwind utility classes (no inline styles)

## Layout
### App Shell
- Top header with app name (left)
- User menu/profile button (right)
- Main area: centered container with max-width
- Background: subtle gradient or very light pattern
- Content sits inside cards/panels

### Pages
1) Auth Pages
- /signin
- /signup
Design:
- Centered card, subtle gradient background
- Clear CTA button, minimal fields
- Small helper links

2) Tasks Dashboard
- Header: "My Tasks"
- Primary action button: "Add Task"
- Task list inside a card
- Filters row (All / Pending / Completed)
- Empty state illustration/text when no tasks

## Core Components
### Buttons
- Primary (colorful, prominent)
- Secondary (neutral)
- Destructive (delete)
- Loading state

### Cards / Panels
- Rounded corners, subtle shadow
- Title + content slots

### Task Item
- Checkbox toggle complete
- Title + optional description
- Small status pill (Pending/Completed)
- Actions: Edit, Delete (icon buttons)

### Modal / Drawer (for Create/Edit)
- Form fields: title (required), description (optional)
- Save + Cancel buttons
- Validation messages

### Alerts / Toasts
- Success: task created/updated/deleted
- Error: API/auth errors

## UI Behavior Requirements
- Smooth interactions (hover/focus states)
- Disable buttons while saving
- Show skeleton/loader on initial load
- Show friendly empty state

## Visual Quality Bar
The UI must not look like a basic tutorial.
It should resemble a polished SaaS dashboard.
