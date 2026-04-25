<?php

namespace App\Http\Controllers;

class DashboardController extends Controller
{
    /**
     * Show the dashboard
     */
    public function index()
    {
        return view('dashboard');
    }

    /**
     * Submit a violation report
     */
    public function submitReport()
    {
        $validated = request()->validate([
            'reporter_name' => 'required|string|max:255',
            'contact' => 'required|string|max:20',
            'location' => 'required|string|max:255',
            'barangay' => 'required|string',
            'priority' => 'required|in:low,medium,high,critical',
            'description' => 'required|string',
            'evidence' => 'nullable|file|mimes:jpg,jpeg,png,mp4,mov|max:102400'
        ]);

        // Process the report
        // You would typically save to database here

        return response()->json([
            'success' => true,
            'message' => 'Report submitted successfully',
            'id' => 'V-' . date('Y') . '-' . str_pad(rand(1, 999), 3, '0', STR_PAD_LEFT)
        ]);
    }

    /**
     * Get all violation reports
     */
    public function getViolations()
    {
        // Mock data
        $violations = [
            [
                'id' => 'V-2026-001',
                'date' => '2026-04-23',
                'location' => 'Maharlika Highway near Public Market',
                'barangay' => 'Poblacion I',
                'category' => 'Illegal Parking',
                'mlConfidence' => 94.2,
                'status' => 'pending',
                'priority' => 'high',
            ],
            // ... add more as needed
        ];

        return response()->json($violations);
    }

    /**
     * Get analytics data
     */
    public function getAnalytics()
    {
        return response()->json([
            'totalReports' => 2847,
            'resolved' => 2103,
            'pending' => 544,
            'thisMonth' => 198,
            'monthlyTrend' => [
                ['month' => 'Oct', 'reports' => 185, 'resolved' => 142],
                ['month' => 'Nov', 'reports' => 203, 'resolved' => 167],
                // ... more data
            ]
        ]);
    }
}
