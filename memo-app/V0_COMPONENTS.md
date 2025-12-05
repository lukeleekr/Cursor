# Using v0 Components with Create React App

## Quick Fix

When adding components from v0.app, they may include Next.js-specific code that needs to be removed for Create React App.

### Automatic Fix

After adding a component from v0, run:

```bash
npm run fix-v0
```

This will automatically remove `"use client"` directives from all component files.

### Manual Fix

If you prefer to fix manually, remove the `"use client";` line from the top of any component file.

## Common Issues

1. **"use client" directive** - Remove this line (Next.js only)
2. **TypeScript files (.tsx)** - The project uses JavaScript (.jsx), but v0 may create .tsx files. You can either:
   - Rename `.tsx` to `.jsx` and remove type annotations
   - Or install TypeScript support: `npm install --save-dev typescript @types/react @types/react-dom`

## Adding Components

```bash
# Add from v0
npx shadcn@latest add "https://v0.app/chat/..."

# Fix automatically
npm run fix-v0

# Or add standard shadcn components
npx shadcn@latest add button
npx shadcn@latest add card
```

## Current Components

- ✅ `note-card.jsx` - Note card component
- ✅ `note-form.jsx` - Note form component  
- ✅ `ui/button.jsx` - Button component











