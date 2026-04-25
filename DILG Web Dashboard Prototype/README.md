# DILG Santa Cruz Community Violation Reporting System

A crowdsourced community violation reporting and machine learning-based classification system aligned with DILG Road Clearing and Public Order Policies in Santa Cruz, Laguna.

## Features

- 📊 **Real-time Dashboard** - Statistics and violation tracking
- 📝 **Report Submission** - Crowdsourced violation reporting with file upload
- 🤖 **ML Classification** - Automated violation categorization with confidence scores
- 📈 **Analytics & Charts** - Data visualization using Recharts
- 🗺️ **Geographic Mapping** - Heat map of violations across 15 barangays
- 🔍 **Advanced Filtering** - Search and filter by status, category, and location

## Tech Stack

- **React 18.3.1** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS v4** - Styling
- **Recharts** - Data visualization
- **Radix UI** - Accessible component primitives
- **Lucide React** - Icons
- **Sonner** - Toast notifications
- **Vite** - Build tool

## Installation & Setup

### Prerequisites
- Node.js 16+ 
- pnpm (recommended) or npm

### Steps

1. **Extract the project files** (if downloaded as ZIP)
   ```bash
   unzip dilg-dashboard.zip
   cd dilg-dashboard
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   # or
   npm install
   ```

3. **Start development server**
   ```bash
   pnpm dev
   # or
   npm run dev
   ```

4. **Open in browser**
   - Navigate to `http://localhost:5173`

## Project Structure

```
src/
├── app/
│   ├── App.tsx                    # Main application component
│   └── components/
│       ├── ViolationStats.tsx     # Statistics cards
│       ├── ReportForm.tsx         # Violation submission form
│       ├── ViolationsTable.tsx    # Filterable data table
│       ├── ViolationCharts.tsx    # Analytics charts
│       ├── MLClassificationPanel.tsx  # ML system dashboard
│       ├── MapView.tsx            # Geographic distribution
│       └── ui/                    # Reusable UI components
├── styles/
│   ├── theme.css                  # Custom CSS and Tailwind config
│   └── fonts.css                  # Font imports
└── imports/                       # Assets and images
```

## Features Detail

### Violation Categories
1. **Illegal Parking** - Unauthorized vehicle parking
2. **Road Obstruction** - Blocked roads and passages
3. **Sidewalk Encroachment** - Blocked pedestrian walkways
4. **Unauthorized Structure** - Illegal constructions
5. **Noise Violation** - Public disturbance

### Covered Barangays (Santa Cruz, Laguna)
- Bagumbayan, Bambang, Bubukal, Calios, Duhat
- Gatid, Jasaan, Labuin, Pagsawitan, Palasan
- Poblacion I, II, III, IV, V

### ML Classification System
- **Algorithm**: Random Forest + CNN Ensemble
- **Accuracy**: 92.3% overall
- **Confidence Scores**: 85-97% per prediction
- **Training Dataset**: 8,472 labeled violations

## Development

### Available Scripts

- `pnpm dev` - Start development server
- `pnpm build` - Build for production
- `pnpm preview` - Preview production build

### Adding New Features

1. **Create new component**: Add to `src/app/components/`
2. **Import in App.tsx**: `import { YourComponent } from "./components/YourComponent"`
3. **Use in tabs**: Add new TabsContent in App.tsx

### Customization

- **Colors**: Edit `/src/styles/theme.css`
- **Mock Data**: Update data arrays in component files
- **Forms**: Modify `/src/app/components/ReportForm.tsx`
- **Charts**: Edit `/src/app/components/ViolationCharts.tsx`

## Research Context

This project is a prototype for the research titled:
**"A Crowdsourced Community Violation Reporting and Machine Learning-Based Classification System Aligned with DILG Road Clearing and Public Order Policies in Santa Cruz, Laguna"**

## License

Created for research and educational purposes.

## Notes

- Currently uses **mock data** for demonstration
- ML classification is **simulated** (not connected to real model)
- File uploads are **frontend-only** (not stored)
- Map visualization is **simplified** (not using real mapping API)

## Future Enhancements

- [ ] Connect to real backend/database
- [ ] Integrate actual ML model API
- [ ] Add real-time notifications
- [ ] Implement user authentication
- [ ] Add admin management panel
- [ ] Connect to mapping API (Google Maps/Mapbox)
- [ ] Add photo storage (cloud storage)
- [ ] Generate PDF reports
