# Google Stitch AI Prompt (Copy-Paste Ready)

```
Design an improved 2D UI/UX for a Chemical Equipment Parameter Visualizer React web application.

APPLICATION PURPOSE:
Data visualization tool for chemical engineers to upload CSV files and view equipment parameters (flowrate, pressure, temperature) through charts, tables, and statistics.

CURRENT COMPONENTS:
1. UploadForm - Drag-and-drop CSV upload
2. DatasetHistory - List of last 5 uploaded datasets (left sidebar)
3. Summary - 4 statistics cards (Total Equipment, Avg Flowrate, Avg Pressure, Avg Temperature)
4. ChartDisplay - 3 charts: Bar chart (flowrate by type), Scatter plot (pressure vs temperature), Pie chart (type distribution)
5. DataTable - Sortable, paginated table with equipment data

CURRENT LAYOUT:
- Header: "Chemical Equipment Parameter Visualizer" title
- Upload section at top
- Two-column grid: Left (History), Right (Summary + Charts + Table)

COLOR SCHEME:
- Primary: Purple-blue gradient (#667eea to #764ba2)
- Success: #48bb78 (green)
- Error: #c53030 (red)
- Info: #4299e1 (blue)
- Background: Light gradient
- Cards: White with shadows

DESIGN REQUIREMENTS:

1. UPLOAD FORM:
   - Large drag-drop zone (200px min-height)
   - Dashed border, color change on hover/drag
   - File name display
   - Gradient upload button
   - Error/success messages

2. SUMMARY CARDS (4-card grid):
   - Card 1: Total Equipment (Blue gradient, icon: factory)
   - Card 2: Avg Flowrate (Green gradient, icon: water drop)
   - Card 3: Avg Pressure (Purple gradient, icon: gauge)
   - Card 4: Avg Temperature (Orange gradient, icon: thermometer)
   - Each: Icon + Label + Large Value + Unit
   - Hover: Lift effect

3. CHARTS SECTION:
   - Grid: 2 columns desktop, 1 mobile
   - Bar chart: Flowrate by equipment type
   - Scatter plot: Pressure vs Temperature
   - Pie chart: Equipment type distribution
   - White cards, rounded corners, 350px height

4. DATA TABLE:
   - White card background
   - Sortable columns
   - Pagination (if >10 rows)
   - Alternating row colors
   - Purple gradient header

5. DATASET HISTORY:
   - Card list (max 5 items)
   - Shows: Filename, item count, upload date
   - Clickable with hover effects

IMPROVEMENTS NEEDED:
- Better spacing/padding system
- Modern card shadows with depth
- Icon integration throughout
- Loading skeleton states
- Friendly empty states
- Responsive breakpoints (mobile, tablet, desktop)
- Consistent color palette
- Clear typography hierarchy
- Smooth 2D animations/transitions
- Better error message displays
- Tooltips on hover

TECHNICAL CONSTRAINTS:
- React 18.2.0
- CSS only (no CSS-in-JS)
- 2D design only (no 3D transforms)
- Modern browsers support
- Mobile-first responsive

DESIGN STYLE:
- Modern dashboard aesthetic
- Professional, scientific data visualization
- Clean and functional
- Card-based layout
- Subtle 2D animations
- Color-coded data types

DELIVERABLES:
1. Desktop mockup (1440x900 or 1920x1080)
2. Tablet mockup (768x1024)
3. Mobile mockup (375x667)
4. Component designs with states (default, hover, active, error)
5. Style guide (colors, typography, spacing)
6. CSS recommendations

Create a comprehensive 2D design system that improves visual appeal, usability, and consistency while maintaining a professional, data-focused interface suitable for chemical engineering professionals.
```
