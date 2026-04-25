import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const categoryData = [
  { name: "Illegal Parking", value: 847, color: "#3b82f6" },
  { name: "Road Obstruction", value: 632, color: "#ef4444" },
  { name: "Sidewalk Encroachment", value: 521, color: "#f59e0b" },
  { name: "Unauthorized Structure", value: 489, color: "#8b5cf6" },
  { name: "Noise Violation", value: 358, color: "#10b981" },
];

const trendData = [
  { month: "Oct", reports: 185, resolved: 142 },
  { month: "Nov", reports: 203, resolved: 167 },
  { month: "Dec", reports: 178, resolved: 154 },
  { month: "Jan", reports: 224, resolved: 189 },
  { month: "Feb", reports: 241, resolved: 201 },
  { month: "Mar", reports: 268, resolved: 223 },
  { month: "Apr", reports: 198, resolved: 157 },
];

const barangayData = [
  { barangay: "Poblacion I", violations: 342 },
  { barangay: "Poblacion II", violations: 298 },
  { barangay: "Bambang", violations: 276 },
  { barangay: "Pagsawitan", violations: 243 },
  { barangay: "Bagumbayan", violations: 221 },
  { barangay: "Duhat", violations: 198 },
  { barangay: "Gatid", violations: 176 },
  { barangay: "Others", violations: 593 },
];

const mlAccuracyData = [
  { category: "Illegal Parking", accuracy: 94.2 },
  { category: "Road Obstruction", accuracy: 96.5 },
  { category: "Sidewalk", accuracy: 89.7 },
  { category: "Structure", accuracy: 87.3 },
  { category: "Noise", accuracy: 91.8 },
];

export function ViolationCharts() {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Violations by Category</CardTitle>
          <CardDescription>Distribution of violation types</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`pie-cell-${entry.name}-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Monthly Trend</CardTitle>
          <CardDescription>Reports and resolutions over time</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="reports" stroke="#3b82f6" strokeWidth={2} />
              <Line type="monotone" dataKey="resolved" stroke="#10b981" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Violations by Barangay</CardTitle>
          <CardDescription>Geographic distribution of reports</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={barangayData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="barangay" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="violations" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>ML Classification Accuracy</CardTitle>
          <CardDescription>Model performance by category</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={mlAccuracyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="category" angle={-45} textAnchor="end" height={100} />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Bar dataKey="accuracy" fill="#10b981">
                {mlAccuracyData.map((entry, index) => (
                  <Cell key={`bar-cell-${entry.category}-${index}`} fill={entry.accuracy > 90 ? "#10b981" : "#f59e0b"} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
