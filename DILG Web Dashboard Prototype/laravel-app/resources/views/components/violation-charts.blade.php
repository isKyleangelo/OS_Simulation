<div class="grid gap-4 md:grid-cols-2">
    <!-- Violations by Category -->
    <div class="bg-white rounded-lg border p-6">
        <h3 class="text-lg font-semibold mb-4">Violations by Category</h3>
        <p class="text-sm text-gray-500 mb-4">Distribution of violation types</p>
        <canvas id="categoryChart"></canvas>
    </div>

    <!-- Monthly Trend -->
    <div class="bg-white rounded-lg border p-6">
        <h3 class="text-lg font-semibold mb-4">Monthly Trend</h3>
        <p class="text-sm text-gray-500 mb-4">Reports and resolutions over time</p>
        <canvas id="trendChart"></canvas>
    </div>

    <!-- Violations by Barangay -->
    <div class="bg-white rounded-lg border p-6">
        <h3 class="text-lg font-semibold mb-4">Violations by Barangay</h3>
        <p class="text-sm text-gray-500 mb-4">Geographic distribution of reports</p>
        <canvas id="barangayChart"></canvas>
    </div>

    <!-- ML Classification Accuracy -->
    <div class="bg-white rounded-lg border p-6">
        <h3 class="text-lg font-semibold mb-4">ML Classification Accuracy</h3>
        <p class="text-sm text-gray-500 mb-4">Model performance by category</p>
        <canvas id="accuracyChart"></canvas>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    // Category Chart (Pie)
    const categoryCtx = document.getElementById('categoryChart').getContext('2d');
    new Chart(categoryCtx, {
        type: 'doughnut',
        data: {
            labels: ['Illegal Parking', 'Road Obstruction', 'Sidewalk Encroachment', 'Unauthorized Structure', 'Noise Violation'],
            datasets: [{
                data: [847, 632, 521, 489, 358],
                backgroundColor: ['#3b82f6', '#ef4444', '#f59e0b', '#8b5cf6', '#10b981']
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'bottom' } }
        }
    });

    // Trend Chart (Line)
    const trendCtx = document.getElementById('trendChart').getContext('2d');
    new Chart(trendCtx, {
        type: 'line',
        data: {
            labels: ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr'],
            datasets: [
                {
                    label: 'Reports',
                    data: [185, 203, 178, 224, 241, 268, 198],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Resolved',
                    data: [142, 167, 154, 189, 201, 223, 157],
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'bottom' } },
            scales: { y: { beginAtZero: true } }
        }
    });

    // Barangay Chart (Bar)
    const barangayCtx = document.getElementById('barangayChart').getContext('2d');
    new Chart(barangayCtx, {
        type: 'bar',
        data: {
            labels: ['Poblacion I', 'Poblacion II', 'Bambang', 'Pagsawitan', 'Bagumbayan', 'Duhat', 'Gatid', 'Others'],
            datasets: [{
                label: 'Violations',
                data: [342, 298, 276, 243, 221, 198, 176, 593],
                backgroundColor: '#3b82f6'
            }]
        },
        options: {
            responsive: true,
            indexAxis: 'x',
            scales: { y: { beginAtZero: true } }
        }
    });

    // Accuracy Chart (Bar)
    const accuracyCtx = document.getElementById('accuracyChart').getContext('2d');
    new Chart(accuracyCtx, {
        type: 'bar',
        data: {
            labels: ['Illegal Parking', 'Road Obstruction', 'Sidewalk', 'Structure', 'Noise'],
            datasets: [{
                label: 'Accuracy (%)',
                data: [94.2, 96.5, 89.7, 87.3, 91.8],
                backgroundColor: ['#10b981', '#10b981', '#f59e0b', '#f59e0b', '#10b981']
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
</script>
