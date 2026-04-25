<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>DILG Dashboard - Violation Reporting System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { height: 100%; width: 100%; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; color: #1e293b; }
        body { display: flex; overflow: hidden; }
        
        /* LOGIN PAGE STYLES */
        .login-page { display: flex; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #1e40af 100%); align-items: center; justify-content: center; z-index: 500; }
        .login-page.hidden { display: none; }
        .login-box { background: white; padding: 3rem; border-radius: 1.25rem; box-shadow: 0 25px 50px rgba(0,0,0,0.3); max-width: 450px; width: 90%; }
        .login-logo { width: 3.5rem; height: 3.5rem; background: linear-gradient(135deg, #1e3a8a, #3b82f6); border-radius: 0.75rem; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 1.75rem; margin: 0 auto 1.5rem; }
        .login-title { text-align: center; margin-bottom: 0.5rem; font-size: 1.75rem; font-weight: 700; color: #1e293b; }
        .login-subtitle { text-align: center; color: #64748b; margin-bottom: 2rem; font-size: 0.95rem; }
        .login-form { display: flex; flex-direction: column; gap: 1rem; }
        .login-form-group { display: flex; flex-direction: column; gap: 0.5rem; }
        .login-form-group label { font-weight: 600; color: #1e293b; font-size: 0.875rem; }
        .login-form-group input { padding: 0.875rem; border: 2px solid #e2e8f0; border-radius: 0.5rem; font-size: 0.95rem; transition: all 0.3s; }
        .login-form-group input:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
        .login-remember { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: #64748b; }
        .login-btn { padding: 0.875rem 1.5rem; background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; border: none; border-radius: 0.5rem; font-weight: 600; cursor: pointer; transition: all 0.3s; margin-top: 0.5rem; }
        .login-btn:hover { box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4); transform: translateY(-2px); }
        .login-message { padding: 0.875rem; border-radius: 0.5rem; margin-bottom: 1rem; text-align: center; font-size: 0.875rem; display: none; }
        .login-message.show { display: block; }
        .login-message.error { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
        .login-message.success { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
        .login-demo { margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #e2e8f0; text-align: center; }
        .login-demo-text { font-size: 0.8rem; color: #64748b; margin-bottom: 1rem; }
        .login-demo-btn { background: #f1f5f9; border: 1px solid #cbd5e1; color: #1e293b; padding: 0.5rem 1rem; border-radius: 0.375rem; font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.3s; }
        .login-demo-btn:hover { background: #e2e8f0; }
        
        /* DASHBOARD STYLES */
        .dashboard-page { display: none; width: 100%; }
        .dashboard-page.visible { display: flex; width: 100%; }
        
        .sidebar { width: 280px; background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); color: white; height: 100vh; position: fixed; left: 0; top: 0; display: flex; flex-direction: column; box-shadow: 2px 0 12px rgba(0,0,0,0.15); z-index: 100; }
        .sidebar-header { padding: 2rem 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; gap: 1rem; }
        .sidebar-logo { width: 2.5rem; height: 2.5rem; background: white; border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #1e3a8a; font-size: 1.25rem; }
        .sidebar-title { flex: 1; }
        .sidebar-title h1 { font-size: 1.1rem; font-weight: 700; }
        .sidebar-title p { font-size: 0.75rem; opacity: 0.8; margin-top: 0.25rem; }
        .sidebar-menu { flex: 1; padding: 1.5rem 0; overflow-y: auto; }
        .sidebar-menu-item { padding: 1rem 1.5rem; cursor: pointer; border-left: 4px solid transparent; transition: all 0.3s ease; display: flex; align-items: center; gap: 1rem; font-weight: 500; }
        .sidebar-menu-item:hover { background: rgba(255,255,255,0.1); }
        .sidebar-menu-item.active { background: rgba(255,255,255,0.15); border-left-color: white; }
        .sidebar-icon { width: 1.25rem; height: 1.25rem; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
        .sidebar-footer { padding: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1); font-size: 0.75rem; opacity: 0.7; }
        .logout-btn { width: 100%; background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3); padding: 0.75rem; border-radius: 0.375rem; cursor: pointer; font-size: 0.8rem; font-weight: 600; transition: all 0.3s; margin-top: 1rem; }
        .logout-btn:hover { background: rgba(255,255,255,0.3); }
        
        .main-container { margin-left: 280px; flex: 1; display: flex; flex-direction: column; height: 100vh; overflow: hidden; width: calc(100% - 280px); }
        
        header { background: white; padding: 1.5rem 2rem; border-bottom: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.08); display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; }
        .header-left { display: flex; align-items: center; gap: 1rem; }
        .breadcrumb { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: #64748b; }
        .breadcrumb strong { color: #1e293b; font-weight: 600; }
        .header-right { display: flex; align-items: center; gap: 1.5rem; }
        .user-info { display: flex; align-items: center; gap: 1rem; }
        .avatar { width: 2.5rem; height: 2.5rem; background: linear-gradient(135deg, #3b82f6, #2563eb); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 1rem; }
        
        main { flex: 1; overflow-y: auto; overflow-x: hidden; padding: 2rem; display: flex; flex-direction: column; max-width: 100%; }
        
        .content-section { display: none; flex-direction: column; width: 100%; flex: 1; overflow: hidden; }
        .content-section.active { display: flex; animation: fadeIn 0.3s ease-out; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        
        .page-title { font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e293b; flex-shrink: 0; }
        .page-subtitle { color: #64748b; margin-bottom: 1.5rem; font-size: 0.95rem; flex-shrink: 0; }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; width: 100%; flex-shrink: 0; max-width: 100%; }
        .card { background: white; padding: 1.5rem; border-radius: 0.75rem; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); display: flex; flex-direction: column; width: 100%; max-width: 100%; box-sizing: border-box; }
        .card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); transition: all 0.3s ease; }
        
        .content-section > .card { flex-shrink: 0; }
        .content-section > .card:not(:last-child) { margin-bottom: 1.5rem; }
        .content-section > .card:last-child { flex: 1; overflow-y: auto; }
        
        .stat-card { background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); border-left: 4px solid #3b82f6; }
        .stat-label { font-size: 0.875rem; color: #64748b; font-weight: 500; margin-bottom: 0.5rem; }
        .stat-value { font-size: 2rem; font-weight: 700; color: #1e293b; margin-bottom: 0.5rem; }
        .stat-change { font-size: 0.8rem; color: #059669; font-weight: 600; }
        .stat-card.success { border-left-color: #10b981; }
        .stat-card.warning { border-left-color: #f59e0b; }
        .stat-card.danger { border-left-color: #ef4444; }
        
        .table-container { background: white; border-radius: 0.75rem; border: 1px solid #e2e8f0; overflow: auto; display: flex; flex-direction: column; flex: 1; width: 100%; max-width: 100%; box-sizing: border-box; }
        table { width: 100%; border-collapse: collapse; }
        thead { display: table; width: 100%; background: #f8fafc; }
        th { background: #f8fafc; padding: 1rem 1.25rem; text-align: left; font-weight: 600; font-size: 0.75rem; color: #64748b; border-bottom: 2px solid #e2e8f0; cursor: pointer; user-select: none; text-transform: uppercase; letter-spacing: 0.5px; }
        th:hover { background: #f1f5f9; }
        td { padding: 1.25rem; border-bottom: 1px solid #e2e8f0; vertical-align: middle; }
        tr:hover { background: #f9fafb; }
        tr:last-child td { border-bottom: none; }
        tbody tr { transition: background-color 0.2s ease; }
        
        .badge { display: inline-block; padding: 0.375rem 0.75rem; border-radius: 0.375rem; font-size: 0.75rem; font-weight: 600; }
        .badge-pending { background: #fef3c7; color: #92400e; }
        .badge-progress { background: #fee2e2; color: #991b1b; }
        .badge-resolved { background: #dcfce7; color: #166534; }
        .badge-primary { background: #dbeafe; color: #164e63; }
        
        .form-group { margin-bottom: 1.5rem; }
        label { display: block; font-weight: 600; margin-bottom: 0.5rem; color: #1e293b; font-size: 0.875rem; }
        input, select, textarea { width: 100%; padding: 0.75rem; border: 1px solid #cbd5e1; border-radius: 0.5rem; font-family: inherit; font-size: 0.875rem; transition: border-color 0.3s; }
        input:focus, select:focus, textarea:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
        
        .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
        
        button { background: #3b82f6; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 0.5rem; cursor: pointer; font-weight: 600; font-size: 0.875rem; transition: all 0.3s; }
        button:hover { background: #2563eb; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
        button:disabled { background: #cbd5e1; cursor: not-allowed; }
        .btn-secondary { background: #6b7280; }
        .btn-secondary:hover { background: #4b5563; }
        .btn-danger { background: #ef4444; }
        .btn-danger:hover { background: #dc2626; }
        .btn-success { background: #10b981; }
        .btn-success:hover { background: #059669; }
        
        .filters { background: white; padding: 1.5rem; border-radius: 0.75rem; border: 1px solid #e2e8f0; margin-bottom: 1.5rem; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; width: 100%; flex-shrink: 0; box-sizing: border-box; max-width: 100%; }
        
        .modal { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.5); z-index: 200; align-items: center; justify-content: center; }
        .modal.active { display: flex; }
        .modal-content { background: white; padding: 2rem; border-radius: 0.75rem; max-width: 600px; width: 90%; max-height: 90vh; overflow-y: auto; box-shadow: 0 25px 50px rgba(0,0,0,0.25); }
        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 1rem; }
        .modal-close { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #64748b; }
        
        .alert { padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 1rem; }
        .alert-success { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
        .alert-error { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
        
        #violationsContainer { flex: 1; display: flex; flex-direction: column; width: 100%; overflow: auto; max-width: 100%; box-sizing: border-box; }
        #recentViolationsContainer { flex: 1; display: flex; flex-direction: column; width: 100%; overflow: auto; max-width: 100%; box-sizing: border-box; }
        #barangayDistribution { flex: 1; display: flex; align-items: center; justify-content: center; width: 100%; overflow: auto; max-width: 100%; box-sizing: border-box; }
        #categoryBreakdown { flex: 1; display: flex; align-items: center; justify-content: center; width: 100%; overflow: auto; max-width: 100%; box-sizing: border-box; }
        
        .empty-state { text-align: center; padding: 2rem; color: #64748b; display: flex; align-items: center; justify-content: center; flex: 1; width: 100%; max-width: 100%; box-sizing: border-box; }
        .empty-state-icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.5; }
    </style>
</head>
<body>
    <!-- LOGIN PAGE -->
    <div id="loginPage" class="login-page">
        <div class="login-box">
            <div class="login-logo">D</div>
            <h2 class="login-title">DILG Santa Cruz</h2>
            <p class="login-subtitle">Violation Reporting System</p>
            
            <div id="loginMsg" class="login-message"></div>
            
            <form class="login-form" onsubmit="handleLogin(event)">
                <div class="login-form-group">
                    <label>Username</label>
                    <input type="text" id="loginUsername" placeholder="Enter username" autofocus required />
                </div>
                <div class="login-form-group">
                    <label>Password</label>
                    <input type="password" id="loginPassword" placeholder="Enter password" required />
                </div>
                <div class="login-remember">
                    <input type="checkbox" id="rememberMe" />
                    <label for="rememberMe">Remember me</label>
                </div>
                <button type="submit" class="login-btn">Sign In</button>
            </form>
            
            <div class="login-demo">
                <div class="login-demo-text">Demo: username <strong>admin</strong>, password <strong>admin123</strong></div>
                <button type="button" class="login-demo-btn" onclick="fillDemo()">Auto-fill</button>
            </div>
        </div>
    </div>
    
    <!-- DASHBOARD PAGE -->
    <div id="dashboardPage" class="dashboard-page">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <div class="sidebar-logo">D</div>
                <div class="sidebar-title">
                    <h1>DILG</h1>
                    <p>Santa Cruz</p>
                </div>
            </div>
            
            <nav class="sidebar-menu">
                <div class="sidebar-menu-item active" data-page="dashboard">
                    <div class="sidebar-icon">≡</div>
                    <span>Dashboard</span>
                </div>
                <div class="sidebar-menu-item" data-page="reports">
                    <div class="sidebar-icon">📋</div>
                    <span>Reports</span>
                </div>
                <div class="sidebar-menu-item" data-page="gismap">
                    <div class="sidebar-icon">🗺️</div>
                    <span>GIS Map</span>
                </div>
                <div class="sidebar-menu-item" data-page="analytics">
                    <div class="sidebar-icon">📊</div>
                    <span>Analytics</span>
                </div>
            </nav>
            
            <div class="sidebar-footer">
                Violation Reporting System v1.0
                <button type="button" class="logout-btn" onclick="logout()">Sign Out</button>
            </div>
        </aside>
        
        <!-- Main Container -->
        <div class="main-container">
            <!-- Header -->
            <header>
                <div class="header-left">
                    <div class="breadcrumb">
                        <strong id="pageTitle">Dashboard</strong>
                    </div>
                </div>
                <div class="header-right">
                    <div class="user-info">
                        <div>
                            <div style="font-weight: 600; font-size: 0.875rem;" id="userName">Administrator</div>
                            <div style="font-size: 0.75rem; color: #64748b;">DILG Operations</div>
                        </div>
                        <div class="avatar" id="userAvatar">A</div>
                    </div>
                </div>
            </header>
            
            <!-- Main Content -->
            <main>
                <!-- Dashboard Section -->
                <section id="dashboard" class="content-section active">
                    <h2 class="page-title">Dashboard</h2>
                    <p class="page-subtitle">Monitor violation reports and system status</p>
                    
                    <div class="grid">
                        <div class="card stat-card">
                            <div class="stat-label">Total Reports</div>
                            <div class="stat-value" id="totalReports">0</div>
                            <div class="stat-change">All submissions</div>
                        </div>
                        <div class="card stat-card success">
                            <div class="stat-label">Resolved</div>
                            <div class="stat-value" id="resolvedCount">0</div>
                            <div class="stat-change" id="resolvedPercent">0% complete</div>
                        </div>
                        <div class="card stat-card warning">
                            <div class="stat-label">Pending</div>
                            <div class="stat-value" id="pendingCount">0</div>
                            <div class="stat-change">Awaiting action</div>
                        </div>
                        <div class="card stat-card danger">
                            <div class="stat-label">In Progress</div>
                            <div class="stat-value" id="inProgressCount">0</div>
                            <div class="stat-change">Being addressed</div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h3 style="margin-bottom: 1.5rem; font-size: 1.125rem; font-weight: 700;">Recent Violation Reports</h3>
                        <div id="recentViolationsContainer">
                            <div class="empty-state"><p>Loading reports...</p></div>
                        </div>
                    </div>
                </section>
                
                <!-- Reports Section -->
                <section id="reports" class="content-section">
                    <h2 class="page-title">Reports Overview</h2>
                    <p class="page-subtitle">Submit new reports and manage existing violations</p>
                    
                    <div class="card" style="margin-bottom: 2rem;">
                        <h3 style="margin-bottom: 1.5rem; font-size: 1.125rem; font-weight: 700;">Submit New Violation Report</h3>
                        <div id="formMessage"></div>
                        <form id="reportForm" onsubmit="handleSubmit(event)">
                            <div class="form-row">
                                <div class="form-group">
                                    <label>Reporter Name</label>
                                    <input type="text" name="reporter" placeholder="Full name" required />
                                </div>
                                <div class="form-group">
                                    <label>Contact Number</label>
                                    <input type="tel" name="contact" placeholder="09XX XXX XXXX" required />
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label>Location</label>
                                <input type="text" name="location" placeholder="Street address or landmark" required />
                            </div>
                            
                            <div class="form-row">
                                <div class="form-group">
                                    <label>Barangay</label>
                                    <select name="barangay" required>
                                        <option value="">Select barangay</option>
                                        <option>Bagumbayan</option>
                                        <option>Bambang</option>
                                        <option>Poblacion I</option>
                                        <option>Poblacion II</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label>Priority Level</label>
                                    <select name="priority" required>
                                        <option value="">Select priority</option>
                                        <option>Low</option>
                                        <option>Medium</option>
                                        <option>High</option>
                                        <option>Critical</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div class="form-group">
                                <label>Violation Description</label>
                                <textarea name="description" rows="4" placeholder="Describe the violation in detail..." required></textarea>
                            </div>
                            
                            <button type="submit" style="width: 100%;">Submit Report</button>
                        </form>
                    </div>
                    
                    <div class="card">
                        <h3 style="margin-bottom: 2rem; font-size: 1.25rem; font-weight: 700;">All Violation Reports</h3>
                        
                        <div style="margin-bottom: 2rem;">
                            <h4 style="margin-bottom: 1rem; font-size: 0.95rem; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 0.5rem;">
                                <span style="font-size: 1.2rem;">⊕</span> Filters
                            </h4>
                            <div class="filters" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                                <input type="text" id="searchInput" placeholder="Search reports..." style="grid-column: 1 / -1;" />
                                <select id="categoryFilter">
                                    <option value="">All Categories</option>
                                    <option>Illegal Parking</option>
                                    <option>Road Obstruction</option>
                                    <option>Sidewalk Encroachment</option>
                                    <option>Unauthorized Structure</option>
                                    <option>Noise Violation</option>
                                    <option>Illegal Dumping</option>
                                </select>
                                <select id="statusFilter">
                                    <option value="">All Status</option>
                                    <option value="pending">Pending</option>
                                    <option value="in-progress">In Progress</option>
                                    <option value="resolved">Resolved</option>
                                </select>
                                <select id="barangayFilter">
                                    <option value="">All Barangays</option>
                                    <option>Bagumbayan</option>
                                    <option>Bambang</option>
                                    <option>Poblacion I</option>
                                    <option>Poblacion II</option>
                                </select>
                            </div>
                        </div>
                        
                        <div style="margin-bottom: 1.5rem; font-size: 0.9rem; color: #64748b; font-weight: 500;">
                            <span id="reportCounter">Showing 0 of 0 reports</span>
                        </div>
                        
                        <div id="violationsContainer">
                            <div class="empty-state"><p>Loading reports...</p></div>
                        </div>
                    </div>
                </section>
                
                <!-- GIS Map Section -->
                <section id="gismap" class="content-section">
                    <h2 class="page-title">GIS Map</h2>
                    <p class="page-subtitle">Geographic distribution of violation reports</p>
                    
                    <div class="card">
                        <div style="height: 500px; background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 100%); border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; color: #64748b; font-weight: 500;">
                            Interactive Map View - Integration Ready
                        </div>
                    </div>
                    
                    <div class="grid" style="margin-top: 1.5rem;">
                        <div class="card">
                            <h3 style="margin-bottom: 1rem; font-size: 1rem; font-weight: 700;">Barangay Distribution</h3>
                            <div id="barangayDistribution"></div>
                        </div>
                    </div>
                </section>
                
                <!-- Analytics Section -->
                <section id="analytics" class="content-section">
                    <h2 class="page-title">Analytics</h2>
                    <p class="page-subtitle">Detailed insights and performance metrics</p>
                    
                    <div class="grid">
                        <div class="card stat-card">
                            <div class="stat-label">Average ML Confidence</div>
                            <div class="stat-value" id="avgConfidence">0%</div>
                            <div class="stat-change">Classification accuracy</div>
                        </div>
                        <div class="card stat-card success">
                            <div class="stat-label">Most Common Violation</div>
                            <div class="stat-value" style="font-size: 1.25rem;" id="mostCommon">N/A</div>
                            <div class="stat-change" id="mostCommonCount">0 reports</div>
                        </div>
                        <div class="card stat-card warning">
                            <div class="stat-label">Busiest Barangay</div>
                            <div class="stat-value" style="font-size: 1.25rem;" id="busiestBarangay">N/A</div>
                            <div class="stat-change" id="busiestBarangayCount">0 reports</div>
                        </div>
                        <div class="card stat-card danger">
                            <div class="stat-label">Resolution Rate</div>
                            <div class="stat-value" id="resolutionRate">0%</div>
                            <div class="stat-change" id="resolutionText">0 of 0</div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h3 style="margin-bottom: 1.5rem; font-size: 1.125rem; font-weight: 700;">Violations by Category</h3>
                        <div id="categoryBreakdown"></div>
                    </div>
                </section>
            </main>
        </div>
    </div>
    
    <!-- Details Modal -->
    <div id="detailsModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 style="font-size: 1.25rem; font-weight: 700;">Report Details</h2>
                <button type="button" class="modal-close" onclick="closeModal()">&times;</button>
            </div>
            <div id="reportDetails"></div>
        </div>
    </div>

    <script>
        let allReports = [];
        let filteredReports = [];
        
        // LOGIN SYSTEM
        const USERS = { 'admin': 'admin123', 'user': 'user123', 'officer': 'officer123' };
        
        function handleLogin(event) {
            event.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;
            const msgEl = document.getElementById('loginMsg');
            
            if (USERS[username] === password) {
                localStorage.setItem('dilgUser', JSON.stringify({ username: username, time: new Date() }));
                if (document.getElementById('rememberMe').checked) localStorage.setItem('dilgRemember', '1');
                msgEl.textContent = 'Success! Redirecting...';
                msgEl.className = 'login-message show success';
                setTimeout(showDashboard, 800);
            } else {
                msgEl.textContent = 'Invalid username or password';
                msgEl.className = 'login-message show error';
                document.getElementById('loginPassword').value = '';
            }
        }
        
        function fillDemo() {
            document.getElementById('loginUsername').value = 'admin';
            document.getElementById('loginPassword').value = 'admin123';
            document.getElementById('loginUsername').focus();
        }
        
        function showDashboard() {
            document.getElementById('loginPage').classList.add('hidden');
            document.getElementById('dashboardPage').classList.add('visible');
            const user = JSON.parse(localStorage.getItem('dilgUser') || '{}');
            document.getElementById('userName').textContent = user.username || 'User';
            document.getElementById('userAvatar').textContent = (user.username || 'U')[0].toUpperCase();
            loadDashboardData();
        }
        
        function logout() {
            if (confirm('Sign out?')) {
                localStorage.removeItem('dilgUser');
                localStorage.removeItem('dilgRemember');
                document.getElementById('dashboardPage').classList.remove('visible');
                document.getElementById('loginPage').classList.remove('hidden');
                document.getElementById('loginUsername').value = '';
                document.getElementById('loginPassword').value = '';
                document.getElementById('loginUsername').focus();
            }
        }
        
        // AUTO-LOGIN
        window.addEventListener('load', () => {
            if (localStorage.getItem('dilgUser')) {
                showDashboard();
            }
        });
        
        // DASHBOARD CODE
        document.addEventListener('DOMContentLoaded', () => {
            setupNavigation();
            setupSearchFilters();
            setInterval(refreshData, 30000);
        });
        
        function setupNavigation() {
            document.querySelectorAll('.sidebar-menu-item').forEach(item => {
                item.addEventListener('click', () => {
                    const page = item.dataset.page;
                    navigateToPage(page);
                });
            });
        }
        
        function navigateToPage(page) {
            document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
            document.querySelectorAll('.sidebar-menu-item').forEach(i => i.classList.remove('active'));
            document.getElementById(page).classList.add('active');
            document.querySelector(`[data-page="${page}"]`).classList.add('active');
            const titles = { dashboard: 'Dashboard', reports: 'Reports', gismap: 'GIS Map', analytics: 'Analytics' };
            document.getElementById('pageTitle').textContent = titles[page];
        }
        
        function loadDashboardData() {
            fetch('/api/violations')
                .then(res => res.json())
                .then(data => { allReports = data; filteredReports = [...allReports]; updateDashboard(); updateReportsList(); })
                .catch(err => console.error('Error:', err));
        }
        
        function refreshData() { loadDashboardData(); }
        
        function updateDashboard() {
            fetch('/api/statistics')
                .then(res => res.json())
                .then(stats => {
                    document.getElementById('totalReports').textContent = stats.totalReports || 0;
                    document.getElementById('resolvedCount').textContent = stats.resolved || 0;
                    const resolvedPercent = stats.totalReports > 0 ? ((stats.resolved / stats.totalReports) * 100).toFixed(1) : 0;
                    document.getElementById('resolvedPercent').textContent = resolvedPercent + '% complete';
                    document.getElementById('pendingCount').textContent = stats.pending || 0;
                    document.getElementById('inProgressCount').textContent = stats.inProgress || 0;
                    document.getElementById('avgConfidence').textContent = (stats.avgConfidence || 0) + '%';
                    document.getElementById('resolutionRate').textContent = (stats.resolutionRate || 0) + '%';
                    document.getElementById('resolutionText').textContent = (stats.resolved || 0) + ' of ' + (stats.totalReports || 0);
                    updateRecentViolations();
                    updateAnalytics();
                });
        }
        
        function updateRecentViolations() {
            const recent = allReports.slice(0, 10);
            const container = document.getElementById('recentViolationsContainer');
            if (recent.length === 0) { container.innerHTML = '<div class="empty-state"><p>No reports</p></div>'; return; }
            let html = '<div class="table-container"><table><thead><tr><th>Report ID</th><th>Location</th><th>Category</th><th>Status</th><th>Date</th></tr></thead><tbody>';
            recent.forEach(report => {
                html += `<tr><td><strong>${report.id}</strong></td><td>${report.location}</td><td>${report.category}</td><td>${getStatusBadge(report.status)}</td><td>${report.date}</td></tr>`;
            });
            html += '</tbody></table></div>';
            container.innerHTML = html;
        }
        
        function updateReportsList() { renderViolationsTable(); }
        
        function setupSearchFilters() {
            [document.getElementById('searchInput'), document.getElementById('statusFilter'), document.getElementById('categoryFilter'), document.getElementById('barangayFilter')].forEach(el => {
                if (el) { el.addEventListener('input', filterViolations); el.addEventListener('change', filterViolations); }
            });
        }
        
        function filterViolations() {
            const searchTerm = (document.getElementById('searchInput')?.value || '').toLowerCase();
            const statusFilter = document.getElementById('statusFilter')?.value || '';
            const categoryFilter = document.getElementById('categoryFilter')?.value || '';
            const barangayFilter = document.getElementById('barangayFilter')?.value || '';
            filteredReports = allReports.filter(report => {
                const matchesSearch = !searchTerm || report.id.toLowerCase().includes(searchTerm) || report.location.toLowerCase().includes(searchTerm) || report.reporter.toLowerCase().includes(searchTerm) || report.description.toLowerCase().includes(searchTerm);
                const matchesStatus = !statusFilter || report.status === statusFilter;
                const matchesCategory = !categoryFilter || report.category === categoryFilter;
                const matchesBarangay = !barangayFilter || report.barangay === barangayFilter;
                return matchesSearch && matchesStatus && matchesCategory && matchesBarangay;
            });
            renderViolationsTable();
        }
        
        function renderViolationsTable() {
            const container = document.getElementById('violationsContainer');
            const counterEl = document.getElementById('reportCounter');
            
            if (filteredReports.length === 0) { 
                container.innerHTML = '<div class="empty-state"><p>No reports match</p></div>';
                counterEl.textContent = `Showing 0 of ${allReports.length} reports`;
                return; 
            }
            
            counterEl.textContent = `Showing ${filteredReports.length} of ${allReports.length} reports`;
            
            let html = '<div class="table-container"><table><thead><tr><th>REPORT</th><th>CATEGORY</th><th>BARANGAY</th><th>DATE</th><th>STATUS</th><th>ACTIONS</th></tr></thead><tbody>';
            filteredReports.forEach(report => {
                const dateObj = new Date(report.date);
                const formattedDate = dateObj.toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' });
                const formattedTime = dateObj.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
                
                html += `<tr>
                    <td>
                        <div style="font-weight: 500; color: #1e293b; line-height: 1.4;">${report.description}</div>
                        <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.25rem;">ID: ${report.id} • ${report.mlConfidence}% confidence</div>
                    </td>
                    <td><span class="badge badge-primary">${report.category}</span></td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <span style="font-size: 1rem;">📍</span>
                            <span>${report.barangay}</span>
                        </div>
                    </td>
                    <td>
                        <div style="font-size: 0.9rem;">${formattedDate}</div>
                        <div style="font-size: 0.8rem; color: #64748b;">${formattedTime}</div>
                    </td>
                    <td>${getStatusBadge(report.status)}</td>
                    <td><button class="btn-secondary" style="padding:0.5rem 1rem; font-size: 0.9rem; display: flex; align-items: center; gap: 0.4rem;" onclick="showReportDetails('${report.id}')"><span style="font-size: 1rem;">👁️</span> View</button></td>
                </tr>`;
            });
            html += '</tbody></table></div>';
            container.innerHTML = html;
        }
        
        function getStatusBadge(status) {
            const badges = { 'pending': '<span class="badge badge-pending">PENDING</span>', 'in-progress': '<span class="badge badge-progress">IN PROGRESS</span>', 'resolved': '<span class="badge badge-resolved">RESOLVED</span>' };
            return badges[status] || '<span class="badge badge-primary">UNKNOWN</span>';
        }
        
        function showReportDetails(reportId) {
            const report = allReports.find(r => r.id === reportId);
            if (!report) return;
            const details = `<div><p><strong>ID:</strong> ${report.id}</p><p><strong>Date:</strong> ${report.date}</p><p><strong>Reporter:</strong> ${report.reporter}</p><p><strong>Contact:</strong> ${report.contact}</p><p><strong>Location:</strong> ${report.location}</p><p><strong>Barangay:</strong> ${report.barangay}</p><p><strong>Category:</strong> ${report.category}</p><p><strong>Priority:</strong> ${report.priority.toUpperCase()}</p><p><strong>ML Confidence:</strong> ${report.mlConfidence}%</p><p><strong>Status:</strong> ${getStatusBadge(report.status)}</p><p style="margin-top:1rem"><strong>Description:</strong></p><p style="background:#f8fafc; padding:1rem; border-radius:0.5rem; margin-top:0.5rem; border-left:4px solid #3b82f6">${report.description}</p></div><div style="display:flex; gap:1rem; margin-top:1.5rem"><button class="btn-secondary" onclick="updateReportStatus('${report.id}','in-progress')" style="flex:1">Mark In Progress</button><button class="btn-success" onclick="updateReportStatus('${report.id}','resolved')" style="flex:1">Mark Resolved</button></div>`;
            document.getElementById('reportDetails').innerHTML = details;
            document.getElementById('detailsModal').classList.add('active');
        }
        
        function updateReportStatus(reportId, newStatus) {
            fetch(`/api/reports/${reportId}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify({status:newStatus})})
                .then(res => res.json())
                .then(data => { if(data.success) { closeModal(); loadDashboardData(); alert('Status updated'); } else { alert('Failed'); } })
                .catch(err => alert('Error: '+err.message));
        }
        
        function closeModal() { document.getElementById('detailsModal').classList.remove('active'); }
        
        function handleSubmit(event) {
            event.preventDefault();
            const form = event.target;
            const submitBtn = form.querySelector('button');
            const msgDiv = document.getElementById('formMessage');
            const formData = {
                reporter: form.querySelector('input[name="reporter"]').value,
                contact: form.querySelector('input[name="contact"]').value,
                location: form.querySelector('input[name="location"]').value,
                barangay: form.querySelector('select[name="barangay"]').value,
                priority: form.querySelector('select[name="priority"]').value,
                description: form.querySelector('textarea[name="description"]').value
            };
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
            fetch('/api/reports', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(formData)})
                .then(res => res.json())
                .then(data => {
                    if(data.success) {
                        msgDiv.innerHTML = `<div class="alert alert-success"><strong>Success!</strong> Report ${data.data.id} - ${data.data.category} (${data.data.mlConfidence}%)</div>`;
                        form.reset();
                        loadDashboardData();
                        setTimeout(() => msgDiv.innerHTML = '', 5000);
                    } else {
                        msgDiv.innerHTML = '<div class="alert alert-error"><strong>Error!</strong> Failed to submit.</div>';
                    }
                })
                .catch(err => msgDiv.innerHTML = '<div class="alert alert-error"><strong>Error!</strong> '+err.message+'</div>')
                .finally(() => { submitBtn.disabled = false; submitBtn.textContent = 'Submit Report'; });
        }
        
        function updateAnalytics() {
            if (allReports.length === 0) {
                document.getElementById('mostCommon').textContent = 'N/A';
                document.getElementById('mostCommonCount').textContent = '0 reports';
                document.getElementById('busiestBarangay').textContent = 'N/A';
                document.getElementById('busiestBarangayCount').textContent = '0 reports';
                document.getElementById('categoryBreakdown').innerHTML = '<div class="empty-state"><p>No data available</p></div>';
                document.getElementById('barangayDistribution').innerHTML = '<div class="empty-state"><p>No data available</p></div>';
                return;
            }
            
            const categories = {};
            allReports.forEach(report => { categories[report.category] = (categories[report.category] || 0) + 1; });
            document.getElementById('mostCommon').textContent = Object.entries(categories).sort((a,b) => b[1]-a[1])[0]?.[0] || 'N/A';
            document.getElementById('mostCommonCount').textContent = (Object.entries(categories).sort((a,b) => b[1]-a[1])[0]?.[1] || 0) + ' reports';
            const barangays = {};
            allReports.forEach(r => { barangays[r.barangay] = (barangays[r.barangay] || 0) + 1; });
            document.getElementById('busiestBarangay').textContent = Object.entries(barangays).sort((a,b) => b[1]-a[1])[0]?.[0] || 'N/A';
            document.getElementById('busiestBarangayCount').textContent = (Object.entries(barangays).sort((a,b) => b[1]-a[1])[0]?.[1] || 0) + ' reports';
            let categoryHtml = '<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:1rem">';
            Object.entries(categories).forEach(([category, count]) => {
                const percentage = ((count / allReports.length) * 100).toFixed(1);
                categoryHtml += `<div style="background:linear-gradient(135deg,#f0f9ff,#e0f2fe); padding:1rem; border-radius:0.5rem; border-left:4px solid #3b82f6"><p style="margin-bottom:0.5rem; font-weight:600">${category}</p><p style="font-size:1.5rem; font-weight:700; color:#3b82f6; margin-bottom:0.25rem">${count}</p><p style="font-size:0.75rem; color:#64748b">${percentage}% of total</p></div>`;
            });
            categoryHtml += '</div>';
            document.getElementById('categoryBreakdown').innerHTML = categoryHtml;
            let barangayHtml = '<div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:1rem">';
            Object.entries(barangays).forEach(([barangay, count]) => {
                barangayHtml += `<div style="background:#f8fafc; padding:1rem; border-radius:0.5rem; text-align:center; border:1px solid #e2e8f0"><p style="font-weight:600; margin-bottom:0.5rem">${barangay}</p><p style="font-size:1.5rem; font-weight:700; color:#3b82f6">${count}</p></div>`;
            });
            barangayHtml += '</div>';
            document.getElementById('barangayDistribution').innerHTML = barangayHtml;
        }
        
        document.getElementById('detailsModal').addEventListener('click', (e) => {
            if (e.target.id === 'detailsModal') closeModal();
        });
    </script>
</body>
</html>
