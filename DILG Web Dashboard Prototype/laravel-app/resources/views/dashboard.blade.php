@extends('layouts.app')

@section('content')
<div class="space-y-6" id="dashboard">
    <!-- Tab Navigation -->
    <nav class="flex flex-wrap gap-2 mb-6 border-b">
        <button class="tab-btn active px-4 py-3 font-medium border-b-2 border-blue-600 text-blue-600" data-tab="overview">
            <svg class="inline h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-3m0 0l7-4 7 4M5 9v10a1 1 0 001 1h12a1 1 0 001-1V9m-9 16l-7-4m0 0V5m7 4l7-4"/></svg>
            Overview
        </button>
        <button class="tab-btn px-4 py-3 font-medium border-b-2 border-transparent hover:border-gray-300 text-gray-600" data-tab="report">
            <svg class="inline h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            Report
        </button>
        <button class="tab-btn px-4 py-3 font-medium border-b-2 border-transparent hover:border-gray-300 text-gray-600" data-tab="violations">
            <svg class="inline h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4v.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            Violations
        </button>
        <button class="tab-btn px-4 py-3 font-medium border-b-2 border-transparent hover:border-gray-300 text-gray-600" data-tab="analytics">
            <svg class="inline h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/></svg>
            Analytics
        </button>
        <button class="tab-btn px-4 py-3 font-medium border-b-2 border-transparent hover:border-gray-300 text-gray-600" data-tab="ml">
            <svg class="inline h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            ML System
        </button>
        <button class="tab-btn px-4 py-3 font-medium border-b-2 border-transparent hover:border-gray-300 text-gray-600" data-tab="map">
            <svg class="inline h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 003 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6 3m-6-3v-13m6 3l5.447-2.724A1 1 0 0021 5.618v10.764a1 1 0 01-1.447.894L15 13m0 5v-13"/></svg>
            Map
        </button>
    </nav>

    <!-- Overview Tab -->
    <div id="overview" class="tab-content space-y-6">
        <div>
            <h2 class="text-3xl font-bold tracking-tight">Dashboard Overview</h2>
            <p class="text-gray-500">
                Crowdsourced violation reporting with ML-based classification for DILG compliance
            </p>
        </div>
        @include('components.violation-stats')
        <div class="grid gap-6 md:grid-cols-2">
            @include('components.violations-table')
            <div class="space-y-6">
                @include('components.map-view')
            </div>
        </div>
    </div>

    <!-- Report Tab -->
    <div id="report" class="tab-content space-y-6 hidden">
        <div>
            <h2 class="text-3xl font-bold tracking-tight">Submit a Violation Report</h2>
            <p class="text-gray-500">
                Report road clearing or public order violations in your community
            </p>
        </div>
        <div class="grid gap-6 md:grid-cols-3">
            <div class="md:col-span-2">
                @include('components.report-form')
            </div>
            <div>
                @include('components.ml-classification-panel')
            </div>
        </div>
    </div>

    <!-- Violations Tab -->
    <div id="violations" class="tab-content space-y-6 hidden">
        <div>
            <h2 class="text-3xl font-bold tracking-tight">All Violation Reports</h2>
            <p class="text-gray-500">
                Browse, filter, and manage community violation reports
            </p>
        </div>
        @include('components.violations-table')
    </div>

    <!-- Analytics Tab -->
    <div id="analytics" class="tab-content space-y-6 hidden">
        <div>
            <h2 class="text-3xl font-bold tracking-tight">Analytics & Insights</h2>
            <p class="text-gray-500">
                Data visualization and trends for violation reports
            </p>
        </div>
        @include('components.violation-stats')
        @include('components.violation-charts')
    </div>

    <!-- ML Tab -->
    <div id="ml" class="tab-content space-y-6 hidden">
        <div>
            <h2 class="text-3xl font-bold tracking-tight">ML Classification System</h2>
            <p class="text-gray-500">
                Machine learning model performance and real-time classification
            </p>
        </div>
        @include('components.ml-classification-panel')
    </div>

    <!-- Map Tab -->
    <div id="map" class="tab-content space-y-6 hidden">
        <div>
            <h2 class="text-3xl font-bold tracking-tight">Geographic Distribution</h2>
            <p class="text-gray-500">
                Map view of violation hotspots across Santa Cruz barangays
            </p>
        </div>
        @include('components.map-view')
    </div>
</div>

<script>
    document.querySelectorAll('.tab-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const tabName = e.currentTarget.dataset.tab;
            
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.add('hidden');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.remove('hidden');
            
            // Update button styles
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('border-blue-600', 'text-blue-600');
                btn.classList.add('border-transparent', 'text-gray-600');
            });
            e.currentTarget.classList.add('border-blue-600', 'text-blue-600');
            e.currentTarget.classList.remove('border-transparent', 'text-gray-600');
        });
    });
</script>
@endsection
