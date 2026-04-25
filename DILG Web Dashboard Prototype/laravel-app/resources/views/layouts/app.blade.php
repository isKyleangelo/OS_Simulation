<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>{{ config('app.name') }} - Community Violation Reporting System</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    <div id="app">
        <header class="bg-white border-b sticky top-0 z-50">
            <div class="container mx-auto px-4 py-4">
                <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="h-12 w-12 bg-blue-600 rounded-lg flex items-center justify-center">
                            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4v2m0 4v2M7.17 3.17A7 7 0 0017.83 16.83a7 7 0 01-9.66 0z"/>
                            </svg>
                        </div>
                        <div>
                            <h1 class="text-xl font-bold">DILG Santa Cruz</h1>
                            <p class="text-sm text-gray-500">Community Violation Reporting System</p>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <div class="hidden md:block text-right">
                            <p class="text-sm font-medium">Santa Cruz, Laguna</p>
                            <p class="text-xs text-gray-500">Road Clearing & Public Order</p>
                        </div>
                    </div>
                </div>
            </div>
        </header>

        <main class="container mx-auto px-4 py-6">
            @yield('content')
        </main>

        <footer class="bg-white border-t mt-12">
            <div class="container mx-auto px-4 py-6">
                <div class="flex flex-col md:flex-row items-center justify-between gap-4">
                    <p class="text-sm text-gray-500">
                        Research Project: Crowdsourced Community Violation Reporting System
                    </p>
                    <p class="text-sm text-gray-500">
                        DILG Road Clearing & Public Order Policies - Santa Cruz, Laguna
                    </p>
                </div>
            </div>
        </footer>
    </div>
</body>
</html>
