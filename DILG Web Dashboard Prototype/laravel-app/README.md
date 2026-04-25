# DILG Web Dashboard - Laravel Edition

A Laravel-based Community Violation Reporting System with ML-based classification for DILG compliance.

## Features

- **Dashboard Overview**: Real-time violation statistics and trends
- **Report Submission**: Easy-to-use form for community members to report violations
- **Violation Tracking**: Browse and filter all submitted violation reports
- **Analytics**: Data visualization with charts and insights
- **ML Classification**: Automatic categorization of violations using machine learning
- **Geographic View**: Map-based visualization of violation hotspots
- **Responsive Design**: Mobile-friendly interface built with Tailwind CSS

## Requirements

- PHP 8.2+
- Composer
- Node.js 16+
- npm or pnpm

## Installation

1. Navigate to the laravel-app directory:
```bash
cd laravel-app
```

2. Install PHP dependencies:
```bash
composer install
```

3. Copy environment file:
```bash
cp .env.example .env
```

4. Generate application key:
```bash
php artisan key:generate
```

5. Install JavaScript dependencies:
```bash
npm install
```

## Development

Start the development server:
```bash
php artisan serve
```

In another terminal, start Vite for asset compilation:
```bash
npm run dev
```

Visit `http://localhost:8000` in your browser.

## Production Build

```bash
npm run build
php artisan serve
```

## Project Structure

- `app/Http/Controllers` - Application controllers
- `resources/views` - Blade templates
- `resources/css` - CSS files and Tailwind configuration
- `resources/js` - JavaScript files
- `routes/web.php` - Web routes
- `database/migrations` - Database schema

## Technologies Used

- **Backend**: Laravel 11
- **Frontend**: Blade templating, Tailwind CSS
- **Charts**: Chart.js
- **Build Tool**: Vite
- **Package Manager**: npm

## License

This project is licensed under the MIT License.
