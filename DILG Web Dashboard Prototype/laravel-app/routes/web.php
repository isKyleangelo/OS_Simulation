<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\DashboardController;

Route::get('/', [DashboardController::class, 'index'])->name('dashboard');
Route::post('/api/reports', [DashboardController::class, 'submitReport'])->name('submit-report');
Route::get('/api/violations', [DashboardController::class, 'getViolations'])->name('get-violations');
Route::get('/api/analytics', [DashboardController::class, 'getAnalytics'])->name('get-analytics');
