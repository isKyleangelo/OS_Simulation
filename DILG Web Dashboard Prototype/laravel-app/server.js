const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 3000;
const DATA_FILE = path.join(__dirname, 'data', 'reports.json');

// Ensure data directory exists
const dataDir = path.join(__dirname, 'data');
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

// Initialize data file with seed data
const seedData = [
  {
    id: 'V-20260420-0001',
    description: 'Vehicles illegally parked on sidewalk near market',
    location: 'Front of Public Market',
    barangay: 'Poblacion I',
    reporter: 'Maria Santos',
    contact: '09171234567',
    category: 'Illegal Parking',
    mlConfidence: 95,
    status: 'pending',
    date: '2026-04-20T14:30:00'
  },
  {
    id: 'V-20260421-0002',
    description: 'Debris and construction waste blocking main street',
    location: 'Sarao Street Corner',
    barangay: 'Bagumbayan',
    reporter: 'Juan Dela Cruz',
    contact: '09181234567',
    category: 'Road Obstruction',
    mlConfidence: 88,
    status: 'in-progress',
    date: '2026-04-21T09:15:00'
  },
  {
    id: 'V-20260422-0003',
    description: 'Illegal structure encroaching sidewalk',
    location: 'Main Avenue near School',
    barangay: 'Poblacion II',
    reporter: 'Ana Rodriguez',
    contact: '09191234567',
    category: 'Sidewalk Encroachment',
    mlConfidence: 92,
    status: 'resolved',
    date: '2026-04-22T16:45:00'
  },
  {
    id: 'V-20260423-0004',
    description: 'Illegal dumping of construction materials',
    location: 'Vacant lot behind shopping center',
    barangay: 'Bambang',
    reporter: 'Peter Johnson',
    contact: '09201234567',
    category: 'Illegal Dumping',
    mlConfidence: 85,
    status: 'pending',
    date: '2026-04-23T11:20:00'
  },
  {
    id: 'V-20260424-0005',
    description: 'Noise violation from karaoke bar late at night',
    location: 'Zone 4 Commercial Area',
    barangay: 'Poblacion I',
    reporter: 'Rosa Martinez',
    contact: '09211234567',
    category: 'Noise Violation',
    mlConfidence: 78,
    status: 'in-progress',
    date: '2026-04-24T22:10:00'
  }
];

function loadReports() {
  try {
    if (fs.existsSync(DATA_FILE)) {
      const data = fs.readFileSync(DATA_FILE, 'utf8');
      return JSON.parse(data);
    }
  } catch (err) {
    console.error('Error loading data:', err.message);
  }
  return seedData;
}

function saveReports(reports) {
  try {
    fs.writeFileSync(DATA_FILE, JSON.stringify(reports, null, 2), 'utf8');
  } catch (err) {
    console.error('Error saving data:', err.message);
  }
}

function generateViolationId() {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const random = Math.floor(Math.random() * 10000);
  return `V-${year}${month}${day}-${String(random).padStart(4, '0')}`;
}

function classifyViolation(description) {
  const keywords = {
    'Illegal Parking': ['park', 'vehicle', 'car', 'motorcycle', 'bike'],
    'Road Obstruction': ['debris', 'obstacle', 'block', 'obstruct', 'waste', 'trash'],
    'Sidewalk Encroachment': ['sidewalk', 'encroach', 'vendor', 'stall', 'occupy'],
    'Unauthorized Structure': ['structure', 'building', 'construct', 'permit', 'temporary'],
    'Noise Violation': ['noise', 'sound', 'loud', 'music', 'horn', 'disturbance'],
    'Illegal Dumping': ['dump', 'dumping', 'garbage', 'rubbish', 'litter']
  };
  
  const descLower = description.toLowerCase();
  let category = 'Other Violation';
  let maxMatches = 0;
  
  for (const [cat, words] of Object.entries(keywords)) {
    const matches = words.filter(w => descLower.includes(w)).length;
    if (matches > maxMatches) {
      maxMatches = matches;
      category = cat;
    }
  }
  
  const confidence = (85 + maxMatches * 3 + Math.random() * 8).toFixed(1);
  return { category, confidence: parseFloat(confidence) };
}

let reports = loadReports();

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;

  // Get all violations
  if (pathname === '/api/violations' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(reports));
    return;
  }

  // Get statistics
  if (pathname === '/api/statistics' && req.method === 'GET') {
    const resolved = reports.filter(r => r.status === 'resolved').length;
    const totalReports = reports.length;
    const avgConfidence = totalReports > 0 ? (reports.reduce((sum, r) => sum + r.mlConfidence, 0) / totalReports).toFixed(1) : 0;
    const resolutionRate = totalReports > 0 ? ((resolved / totalReports) * 100).toFixed(1) : 0;
    
    const stats = {
      totalReports: totalReports,
      resolved: resolved,
      pending: reports.filter(r => r.status === 'pending').length,
      inProgress: reports.filter(r => r.status === 'in-progress').length,
      thisMonth: reports.filter(r => new Date(r.date).getMonth() === new Date().getMonth()).length,
      avgConfidence: parseFloat(avgConfidence),
      resolutionRate: parseFloat(resolutionRate)
    };
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(stats));
    return;
  }

  // Submit new report
  if (pathname === '/api/reports' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      try {
        const formData = JSON.parse(body);
        const classification = classifyViolation(formData.description);
        const newReport = {
          id: generateViolationId(),
          date: new Date().toISOString().split('T')[0],
          reporter: formData.reporter,
          contact: formData.contact,
          location: formData.location,
          barangay: formData.barangay,
          category: classification.category,
          description: formData.description,
          mlConfidence: classification.confidence,
          status: 'pending',
          priority: formData.priority.toLowerCase()
        };
        reports.unshift(newReport);
        saveReports(reports);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({success: true, data: newReport}));
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({success: false, error: 'Invalid request'}));
      }
    });
    return;
  }

  // Update report status
  if (pathname.startsWith('/api/reports/') && req.method === 'PUT') {
    const id = pathname.split('/')[3];
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      try {
        const { status } = JSON.parse(body);
        const report = reports.find(r => r.id === id);
        if (report) {
          report.status = status;
          saveReports(reports);
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({success: true, data: report}));
        } else {
          res.writeHead(404, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({success: false, error: 'Report not found'}));
        }
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({success: false, error: 'Invalid request'}));
      }
    });
    return;
  }

  // Serve HTML file for root
  if (pathname === '/' || pathname === '') {
    const filePath = path.join(__dirname, 'public', 'index.php');
    fs.readFile(filePath, 'utf8', (err, data) => {
      if (err) {
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end('<h1>404 - File not found</h1>');
        return;
      }
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(data);
    });
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/html' });
  res.end('<h1>404 - Not Found</h1>');
});

server.listen(PORT, () => {
  console.log(`[DILG Dashboard] Server is running at http://localhost:${PORT}`);
  console.log(`[DILG Dashboard] Open your browser and navigate to: http://localhost:${PORT}`);
});

