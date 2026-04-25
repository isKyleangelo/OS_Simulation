<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
    @foreach([
        ['title' => 'Total Reports', 'value' => '2,847', 'change' => '+12.5%', 'icon' => 'alert', 'color' => 'text-blue-600'],
        ['title' => 'Resolved', 'value' => '2,103', 'change' => '+8.2%', 'icon' => 'check', 'color' => 'text-green-600'],
        ['title' => 'Pending', 'value' => '544', 'change' => '-5.1%', 'icon' => 'clock', 'color' => 'text-yellow-600'],
        ['title' => 'This Month', 'value' => '198', 'change' => '+23.4%', 'icon' => 'trending', 'color' => 'text-purple-600']
    ] as $stat)
    <div class="bg-white rounded-lg border p-6">
        <div class="flex flex-row items-center justify-between space-y-0 pb-2">
            <h3 class="text-sm font-medium text-gray-700">{{ $stat['title'] }}</h3>
            @if($stat['icon'] === 'alert')
                <svg class="h-4 w-4 {{ $stat['color'] }}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4v2m0 4v2M7.17 3.17A7 7 0 0017.83 16.83a7 7 0 01-9.66 0z"/></svg>
            @elseif($stat['icon'] === 'check')
                <svg class="h-4 w-4 {{ $stat['color'] }}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            @elseif($stat['icon'] === 'clock')
                <svg class="h-4 w-4 {{ $stat['color'] }}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            @else
                <svg class="h-4 w-4 {{ $stat['color'] }}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3v-8"/></svg>
            @endif
        </div>
        <div class="text-2xl font-bold">{{ $stat['value'] }}</div>
        <p class="text-xs text-gray-500">
            <span class="{{ str_starts_with($stat['change'], '+') ? 'text-green-600' : 'text-red-600' }}">
                {{ $stat['change'] }}
            </span>
            from last month
        </p>
    </div>
    @endforeach
</div>
