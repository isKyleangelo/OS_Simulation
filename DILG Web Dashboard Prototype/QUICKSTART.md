# DILG Web Dashboard - Laravel Complete Guide

## ✅ Conversion Complete

Your React/Vite project has been fully converted to Laravel while maintaining:
- ✅ All content and data
- ✅ All animations and interactions  
- ✅ Tailwind CSS styling
- ✅ Responsive design
- ✅ All features

**No watermarks** - completely clean application

---

## 📁 What Was Created

A complete Laravel application in the `laravel-app/` folder with:

### Backend Files
- `app/Http/Controllers/DashboardController.php` - Main controller
- `app/Models/ViolationReport.php` - Database model
- `app/Providers/AppServiceProvider.php` - Service provider
- `routes/web.php` - Web routes
- `config/app.php` - Application configuration
- Database migrations

### Frontend Files
- `resources/views/layouts/app.blade.php` - Main layout
- `resources/views/dashboard.blade.php` - Dashboard page
- `resources/views/components/` - Individual components:
  - `report-form.blade.php`
  - `violations-table.blade.php`
  - `violation-charts.blade.php`
  - `ml-classification-panel.blade.php`
  - `map-view.blade.php`
  - `violation-stats.blade.php`

### Styling
- `resources/css/app.css` - Custom styles
- `resources/css/tailwind.css` - Tailwind directives
- `tailwind.config.js` - Tailwind configuration
- `postcss.config.js` - PostCSS configuration

### Build Configuration
- `vite.config.js` - Vite bundler configuration
- `package.json` - JavaScript dependencies
- `composer.json` - PHP dependencies
- `.env.example` - Environment file template

---

## 🚀 Getting Started

### Step 1: Navigate to the Laravel Project
```bash
cd laravel-app
```

### Step 2: Install Dependencies
```bash
# Install PHP dependencies
composer install

# Install JavaScript dependencies
npm install
```

### Step 3: Configure Environment
```bash
# Copy environment file
cp .env.example .env

# Generate application key
php artisan key:generate
```

### Step 4: Run Database Migrations
```bash
php artisan migrate
```

### Step 5: Start Development Servers

**Terminal 1 - Start Laravel Server:**
```bash
php artisan serve
```

**Terminal 2 - Start Vite Development Server:**
```bash
npm run dev
```

### Step 6: Access the Application
Open your browser and navigate to:
```
http://localhost:8000
```

---

## 📦 Available Commands

### Development
```bash
npm run dev       # Start Vite development server
npm run build     # Build assets for production
php artisan serve # Start Laravel development server
```

### Database
```bash
php artisan migrate      # Run migrations
php artisan migrate:reset # Reset database
php artisan tinker       # Access Laravel interactive shell
```

### Utility
```bash
php artisan list                    # List all available commands
php artisan make:controller Name    # Create new controller
php artisan make:model Name         # Create new model
```

---

## 🎨 Features

### Dashboard Overview
- Real-time violation statistics
- Key metrics (Total Reports, Resolved, Pending, This Month)
- Visual charts and analytics

### Report Submission
- Easy-to-use form for submitting violations
- Barangay selection (all Santa Cruz barangays)
- Priority levels (Low, Medium, High, Critical)
- Evidence upload support
- Automatic ML classification simulation

### Violations Management
- Searchable table of all violation reports
- Filter by status (Pending, In Progress, Resolved, Rejected)
- Filter by violation category
- ML confidence scores
- Priority indicators

### Analytics
- Pie chart: Violations by category
- Line chart: Monthly trends
- Bar chart: Violations by barangay
- Bar chart: ML classification accuracy

### ML Classification Panel
- Model performance metrics
  - Overall Accuracy: 92.3%
  - Precision: 90.1%
  - Recall: 88.7%
  - F1 Score: 89.4%
- Recent classifications with confidence scores
- Feature detection display

### Geographic View
- Map placeholder with barangay distribution
- Violation density indicators
- High/Medium/Low density zones

---

## 🔧 Customization

### Add a New Page
1. Create a Blade template in `resources/views/pages/`
2. Add a route in `routes/web.php`
3. Create a controller method if needed

### Add a New API Endpoint
1. Create a method in `DashboardController.php`
2. Define route in `routes/web.php`
3. Return JSON response

### Modify Styling
- Edit `resources/css/app.css` for custom styles
- Modify `tailwind.config.js` for Tailwind configuration
- All changes auto-reload during development

### Update Database
1. Create migration: `php artisan make:migration migration_name`
2. Define table structure
3. Run: `php artisan migrate`

---

## 📊 Database Schema

### violation_reports Table
```sql
- id (primary key)
- report_id (unique, e.g., V-2026-001)
- reporter_name
- contact
- location
- barangay
- priority (low, medium, high, critical)
- description (text)
- category (nullable)
- ml_confidence (decimal)
- status (pending, in-progress, resolved, rejected)
- evidence_path (nullable)
- timestamps (created_at, updated_at)
```

---

## 🔒 Security Features

- ✅ CSRF protection enabled
- ✅ Input validation on all forms
- ✅ Encrypted environment variables
- ✅ Secure headers configured
- ✅ XSS protection

---

## 📱 Responsive Design

The application is fully responsive and works on:
- ✅ Desktop (1024px+)
- ✅ Tablet (768px - 1024px)
- ✅ Mobile (320px - 768px)

---

## 🌐 Browser Support

Works on all modern browsers:
- Chrome/Chromium
- Firefox
- Safari
- Edge

---

## 📝 Notes

- **Data Persistence**: Currently uses SQLite. To use MySQL/PostgreSQL, update `.env` and change database configuration
- **Authentication**: Not included by default. Add with: `php artisan ui:auth`
- **Mail**: Configure in `.env` to enable email notifications
- **Storage**: File uploads stored in `storage/app/`

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use different port
php artisan serve --port=8001
```

### Permission Issues
```bash
# Fix storage and bootstrap permissions
chmod -R 775 storage bootstrap/cache
```

### Database Error
```bash
# Clear database and re-migrate
php artisan migrate:reset
php artisan migrate
```

### Missing Dependencies
```bash
# Reinstall all dependencies
composer install --no-cache
npm install --force
```

---

## 📚 Resources

- [Laravel Documentation](https://laravel.com/docs)
- [Blade Template Syntax](https://laravel.com/docs/11.x/blade)
- [Tailwind CSS](https://tailwindcss.com)
- [Vite Documentation](https://vitejs.dev)
- [Chart.js Documentation](https://www.chartjs.org)

---

## 🎉 You're All Set!

Your Laravel application is ready to use. Start the development servers and begin building!

For any questions or issues, refer to the resources above or the documentation files included in the project.

**Happy coding!** 🚀
