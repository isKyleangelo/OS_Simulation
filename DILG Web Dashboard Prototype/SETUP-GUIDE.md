# Setup Guide - DILG Dashboard

## Quick Start (3 Steps)

### 1️⃣ Download the Project
- Click the **Export/Download** button in Figma Make
- Extract the ZIP file to your desired location

### 2️⃣ Install Dependencies
Open terminal in the project folder:
```bash
pnpm install
```

### 3️⃣ Run the Project
```bash
pnpm dev
```
Visit: `http://localhost:5173`

---

## Detailed Setup

### System Requirements
- **Node.js**: v16 or higher ([Download](https://nodejs.org))
- **pnpm**: Recommended package manager
  ```bash
  npm install -g pnpm
  ```

### For Different Code Editors

#### **VS Code** (Recommended)
1. Open folder: `File → Open Folder → Select project`
2. Install recommended extensions:
   - ESLint
   - Tailwind CSS IntelliSense
   - TypeScript and JavaScript Language Features

#### **Other Editors**
- WebStorm, Sublime Text, Atom, etc. - Just open the project folder

### Editing the Project

#### **Change Content/Text**
Edit component files in `src/app/components/`:
- `ViolationStats.tsx` - Dashboard statistics
- `ReportForm.tsx` - Submission form
- `ViolationsTable.tsx` - Violations list
- etc.

#### **Modify Styles**
- **Tailwind classes**: Edit directly in components
- **Custom CSS**: Edit `src/styles/theme.css`

#### **Add New Pages/Tabs**
In `src/app/App.tsx`:
```tsx
<TabsTrigger value="new-tab">New Tab</TabsTrigger>

<TabsContent value="new-tab">
  <YourNewComponent />
</TabsContent>
```

#### **Update Mock Data**
Find data arrays in component files and modify:
```tsx
const mockViolations = [
  // Add/edit your data here
];
```

### Common Tasks

#### Add Animation
```tsx
import { motion } from "motion/react";

<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.5 }}
>
  Your content
</motion.div>
```

#### Add New Component
1. Create file: `src/app/components/MyComponent.tsx`
2. Write component:
```tsx
export function MyComponent() {
  return <div>My Content</div>;
}
```
3. Import in App.tsx:
```tsx
import { MyComponent } from "./components/MyComponent";
```

#### Install New Package
```bash
pnpm add package-name
```

### Troubleshooting

**Port already in use:**
```bash
# Use different port
pnpm dev -- --port 3000
```

**Dependencies issue:**
```bash
# Clear and reinstall
rm -rf node_modules
pnpm install
```

**TypeScript errors:**
- Check imports are correct
- Ensure files are saved
- Restart VS Code

### Deploy to Production

#### Build
```bash
pnpm build
```
Output: `dist/` folder

#### Deploy Options
- **Vercel**: `vercel deploy`
- **Netlify**: Drag `dist/` folder to Netlify
- **GitHub Pages**: Push to GitHub and enable Pages

---

## Need Help?

- Check component files for examples
- All UI components are in `src/app/components/ui/`
- Mock data shows the expected structure
