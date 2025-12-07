# UI Changes Documentation

This document summarizes the UI modifications made to the 'Physical AI & Humanoid Robotics' Docusaurus project.

## 1. Files Modified

The following files were updated to implement the new UI theme:

- `docusaurus.config.ts`
- `src/css/custom.css`
- `src/pages/index.tsx`

## 2. Color Palette

A new color palette with support for both light and dark modes was implemented in `src/css/custom.css`.

### Light Mode
- **Background**: Light Blue (`#E0F2F7`)
- **Text**: Dark Blue (`#1C3D5A`)
- **Primary / Links**: Vibrant Blue (`#007BFF`)
- **Footer Background**: Dark Blue (`#1C3D5A`)

### Dark Mode
- **Background**: Dark Blue (`#1C3D5A`)
- **Text**: Alice Blue (`#F0F8FF`)
- **Primary / Links**: Sky Blue (`#87CEEB`)

## 3. Homepage Customization (`src/pages/index.tsx`)

The hero section of the homepage was updated with:
- A new title: "Welcome to the Future of Physical AI"
- A new subtitle: "Explore the intersection of artificial intelligence and humanoid robotics."
- Two call-to-action buttons: "Explore Modules" and "View on GitHub".
- An animated gradient background that respects the light and dark mode themes.

## 4. Global Styles (`src/css/custom.css`)

- **Light & Dark Mode**: CSS variables were structured to provide distinct color schemes for both modes.
- **Navbar**: The navbar link colors are now tied to the theme's primary color (`--ifm-link-color`).
- **Footer**: The footer is styled to be dark in light mode and uses the theme background color in dark mode.
- **Buttons**: Button hover effects were updated to match the new color scheme.
- **Animated Background**: The hero section features an animated gradient background.

## 5. Docusaurus Configuration (`docusaurus.config.ts`)

The configuration was verified to have `colorMode.disableSwitch` set to `false`, allowing users to toggle between light and dark modes. The `defaultMode` is set to `dark`.
