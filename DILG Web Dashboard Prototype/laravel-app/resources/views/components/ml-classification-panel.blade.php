<div class="bg-white rounded-lg border">
    <div class="border-b p-6">
        <div class="flex items-center justify-between">
            <div>
                <h3 class="text-lg font-semibold">ML Classification System</h3>
                <p class="text-sm text-gray-500">Machine Learning-Based Violation Classification</p>
            </div>
            <svg class="h-8 w-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m7 0a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        </div>
    </div>
    <div class="p-6">
        <div class="grid gap-4 md:grid-cols-4">
            @foreach(['Overall Accuracy' => 92.3, 'Precision' => 90.1, 'Recall' => 88.7, 'F1 Score' => 89.4] as $label => $value)
            <div class="space-y-2">
                <p class="text-sm font-medium text-gray-500">{{ $label }}</p>
                <p class="text-2xl font-bold">{{ number_format($value, 1) }}%</p>
                <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-green-600 h-2 rounded-full" style="width: {{ $value }}%"></div>
                </div>
            </div>
            @endforeach
        </div>
    </div>
</div>

<div class="bg-white rounded-lg border">
    <div class="border-b p-6">
        <h3 class="text-lg font-semibold">Recent Classifications</h3>
        <p class="text-sm text-gray-500">Latest ML predictions and confidence scores</p>
    </div>
    <div class="p-6 space-y-4">
        @foreach([
            ['id' => 'V-2026-001', 'prediction' => 'Illegal Parking', 'confidence' => 94.2, 'features' => ['Vehicle present', 'No parking zone', 'Daytime hours'], 'timestamp' => '2 minutes ago'],
            ['id' => 'V-2026-002', 'prediction' => 'Sidewalk Encroachment', 'confidence' => 89.7, 'features' => ['Sidewalk blocked', 'Commercial items', 'Public space'], 'timestamp' => '15 minutes ago'],
            ['id' => 'V-2026-003', 'prediction' => 'Road Obstruction', 'confidence' => 96.5, 'features' => ['Main road blocked', 'Construction materials', 'No permit visible'], 'timestamp' => '1 hour ago']
        ] as $classification)
        <div class="border rounded-lg p-4">
            <div class="flex items-start justify-between mb-2">
                <div>
                    <p class="font-medium">{{ $classification['id'] }}</p>
                    <p class="text-sm text-gray-500">{{ $classification['timestamp'] }}</p>
                </div>
                <span class="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded">{{ $classification['confidence'] }}%</span>
            </div>
            <p class="text-sm font-medium text-blue-600 mb-2">{{ $classification['prediction'] }}</p>
            <div class="flex flex-wrap gap-2">
                @foreach($classification['features'] as $feature)
                <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">{{ $feature }}</span>
                @endforeach
            </div>
        </div>
        @endforeach
    </div>
</div>
