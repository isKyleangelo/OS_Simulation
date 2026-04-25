<div class="bg-white rounded-lg border">
    <div class="border-b p-6">
        <h3 class="text-lg font-semibold">Violation Reports</h3>
        <p class="text-sm text-gray-500">All crowdsourced violation reports with ML classification</p>
    </div>
    <div class="p-6">
        <div class="flex flex-col md:flex-row gap-4 mb-4">
            <div class="relative flex-1">
                <svg class="absolute left-2 top-2.5 h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                <input type="text" id="searchInput" placeholder="Search by ID, location, or barangay..." class="pl-8 w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <select id="statusFilter" class="w-full md:w-[180px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="all">All Status</option>
                <option value="pending">Pending</option>
                <option value="in-progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="rejected">Rejected</option>
            </select>
            <select id="categoryFilter" class="w-full md:w-[200px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="all">All Categories</option>
                <option value="Illegal Parking">Illegal Parking</option>
                <option value="Road Obstruction">Road Obstruction</option>
                <option value="Sidewalk Encroachment">Sidewalk Encroachment</option>
                <option value="Unauthorized Structure">Unauthorized Structure</option>
                <option value="Noise Violation">Noise Violation</option>
            </select>
        </div>

        <div class="rounded-md border overflow-x-auto">
            <table class="w-full text-sm">
                <thead class="border-b bg-gray-50">
                    <tr>
                        <th class="px-4 py-3 text-left font-medium">Report ID</th>
                        <th class="px-4 py-3 text-left font-medium">Date</th>
                        <th class="px-4 py-3 text-left font-medium">Location</th>
                        <th class="px-4 py-3 text-left font-medium">Barangay</th>
                        <th class="px-4 py-3 text-left font-medium">ML Category</th>
                        <th class="px-4 py-3 text-left font-medium">Confidence</th>
                        <th class="px-4 py-3 text-left font-medium">Priority</th>
                        <th class="px-4 py-3 text-left font-medium">Status</th>
                        <th class="px-4 py-3 text-left font-medium">Actions</th>
                    </tr>
                </thead>
                <tbody id="violationsTableBody">
                </tbody>
            </table>
        </div>
    </div>
</div>

<script>
    const violations = [
        {id: 'V-2026-001', date: '2026-04-23', location: 'Maharlika Highway near Public Market', barangay: 'Poblacion I', category: 'Illegal Parking', confidence: 94.2, priority: 'high', status: 'pending'},
        {id: 'V-2026-002', date: '2026-04-22', location: 'Rizal St. corner Santos Ave.', barangay: 'Poblacion II', category: 'Sidewalk Encroachment', confidence: 89.7, priority: 'medium', status: 'in-progress'},
        {id: 'V-2026-003', date: '2026-04-22', location: 'Pagsawitan Road', barangay: 'Pagsawitan', category: 'Road Obstruction', confidence: 96.5, priority: 'critical', status: 'resolved'},
        {id: 'V-2026-004', date: '2026-04-21', location: 'Bagumbayan Elementary School vicinity', barangay: 'Bagumbayan', category: 'Unauthorized Structure', confidence: 87.3, priority: 'medium', status: 'pending'},
        {id: 'V-2026-005', date: '2026-04-21', location: 'Bambang Commercial District', barangay: 'Bambang', category: 'Noise Violation', confidence: 91.8, priority: 'low', status: 'in-progress'},
        {id: 'V-2026-006', date: '2026-04-20', location: 'Duhat Wet Market Area', barangay: 'Duhat', category: 'Illegal Parking', confidence: 93.1, priority: 'high', status: 'resolved'},
        {id: 'V-2026-007', date: '2026-04-20', location: 'Gatid Main Road', barangay: 'Gatid', category: 'Road Obstruction', confidence: 88.9, priority: 'high', status: 'pending'},
        {id: 'V-2026-008', date: '2026-04-19', location: 'Jasaan Chapel vicinity', barangay: 'Jasaan', category: 'Sidewalk Encroachment', confidence: 85.4, priority: 'low', status: 'rejected'}
    ];

    function renderTable() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        const statusFilter = document.getElementById('statusFilter').value;
        const categoryFilter = document.getElementById('categoryFilter').value;

        const filtered = violations.filter(v => {
            const matchesSearch = v.location.toLowerCase().includes(searchTerm) || 
                                 v.id.toLowerCase().includes(searchTerm) ||
                                 v.barangay.toLowerCase().includes(searchTerm);
            const matchesStatus = statusFilter === 'all' || v.status === statusFilter;
            const matchesCategory = categoryFilter === 'all' || v.category === categoryFilter;
            return matchesSearch && matchesStatus && matchesCategory;
        });

        const tbody = document.getElementById('violationsTableBody');
        tbody.innerHTML = filtered.map(v => `
            <tr class="border-b hover:bg-gray-50">
                <td class="px-4 py-3 font-medium">${v.id}</td>
                <td class="px-4 py-3">${v.date}</td>
                <td class="px-4 py-3 max-w-[200px]">
                    <div class="flex items-start gap-2">
                        <svg class="h-4 w-4 text-gray-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/></svg>
                        <span class="text-sm">${v.location}</span>
                    </div>
                </td>
                <td class="px-4 py-3">${v.barangay}</td>
                <td class="px-4 py-3">${v.category}</td>
                <td class="px-4 py-3">
                    <div class="flex items-center gap-2">
                        <div class="w-12 bg-gray-200 rounded-full h-2">
                            <div class="bg-green-600 h-2 rounded-full" style="width: ${v.confidence}%"></div>
                        </div>
                        <span class="text-sm">${v.confidence}%</span>
                    </div>
                </td>
                <td class="px-4 py-3">
                    <span class="px-2 py-1 rounded text-xs font-medium ${getPriorityClass(v.priority)}">${v.priority.toUpperCase()}</span>
                </td>
                <td class="px-4 py-3">
                    <span class="px-2 py-1 rounded text-xs font-medium ${getStatusClass(v.status)}">${v.status.toUpperCase()}</span>
                </td>
                <td class="px-4 py-3">
                    <button class="p-1 hover:bg-gray-100 rounded">
                        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    function getPriorityClass(priority) {
        const classes = {
            'low': 'bg-blue-100 text-blue-800',
            'medium': 'bg-yellow-100 text-yellow-800',
            'high': 'bg-orange-100 text-orange-800',
            'critical': 'bg-red-100 text-red-800'
        };
        return classes[priority] || '';
    }

    function getStatusClass(status) {
        const classes = {
            'pending': 'bg-gray-100 text-gray-800',
            'in-progress': 'bg-blue-100 text-blue-800',
            'resolved': 'bg-green-100 text-green-800',
            'rejected': 'bg-red-100 text-red-800'
        };
        return classes[status] || '';
    }

    document.getElementById('searchInput').addEventListener('input', renderTable);
    document.getElementById('statusFilter').addEventListener('change', renderTable);
    document.getElementById('categoryFilter').addEventListener('change', renderTable);
    renderTable();
</script>
