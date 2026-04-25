import { useState } from "react";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "./ui/table";
import { Eye, MapPin, Search } from "lucide-react";

interface Violation {
  id: string;
  date: string;
  location: string;
  barangay: string;
  category: string;
  mlConfidence: number;
  status: "pending" | "in-progress" | "resolved" | "rejected";
  priority: "low" | "medium" | "high" | "critical";
  reporter: string;
}

const mockViolations: Violation[] = [
  {
    id: "V-2026-001",
    date: "2026-04-23",
    location: "Maharlika Highway near Public Market",
    barangay: "Poblacion I",
    category: "Illegal Parking",
    mlConfidence: 94.2,
    status: "pending",
    priority: "high",
    reporter: "Juan Dela Cruz"
  },
  {
    id: "V-2026-002",
    date: "2026-04-22",
    location: "Rizal St. corner Santos Ave.",
    barangay: "Poblacion II",
    category: "Sidewalk Encroachment",
    mlConfidence: 89.7,
    status: "in-progress",
    priority: "medium",
    reporter: "Maria Santos"
  },
  {
    id: "V-2026-003",
    date: "2026-04-22",
    location: "Pagsawitan Road",
    barangay: "Pagsawitan",
    category: "Road Obstruction",
    mlConfidence: 96.5,
    status: "resolved",
    priority: "critical",
    reporter: "Pedro Reyes"
  },
  {
    id: "V-2026-004",
    date: "2026-04-21",
    location: "Bagumbayan Elementary School vicinity",
    barangay: "Bagumbayan",
    category: "Unauthorized Structure",
    mlConfidence: 87.3,
    status: "pending",
    priority: "medium",
    reporter: "Ana Garcia"
  },
  {
    id: "V-2026-005",
    date: "2026-04-21",
    location: "Bambang Commercial District",
    barangay: "Bambang",
    category: "Noise Violation",
    mlConfidence: 91.8,
    status: "in-progress",
    priority: "low",
    reporter: "Carlos Rivera"
  },
  {
    id: "V-2026-006",
    date: "2026-04-20",
    location: "Duhat Wet Market Area",
    barangay: "Duhat",
    category: "Illegal Parking",
    mlConfidence: 93.1,
    status: "resolved",
    priority: "high",
    reporter: "Lisa Mendoza"
  },
  {
    id: "V-2026-007",
    date: "2026-04-20",
    location: "Gatid Main Road",
    barangay: "Gatid",
    category: "Road Obstruction",
    mlConfidence: 88.9,
    status: "pending",
    priority: "high",
    reporter: "Ramon Cruz"
  },
  {
    id: "V-2026-008",
    date: "2026-04-19",
    location: "Jasaan Chapel vicinity",
    barangay: "Jasaan",
    category: "Sidewalk Encroachment",
    mlConfidence: 85.4,
    status: "rejected",
    priority: "low",
    reporter: "Teresa Lopez"
  }
];

export function ViolationsTable() {
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [categoryFilter, setCategoryFilter] = useState("all");

  const filteredViolations = mockViolations.filter(violation => {
    const matchesSearch = violation.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         violation.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         violation.barangay.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === "all" || violation.status === statusFilter;
    const matchesCategory = categoryFilter === "all" || violation.category === categoryFilter;
    return matchesSearch && matchesStatus && matchesCategory;
  });

  const getStatusBadge = (status: string) => {
    const variants: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
      pending: "secondary",
      "in-progress": "default",
      resolved: "outline",
      rejected: "destructive"
    };
    return <Badge variant={variants[status]}>{status.toUpperCase()}</Badge>;
  };

  const getPriorityBadge = (priority: string) => {
    const colors: Record<string, string> = {
      low: "bg-blue-100 text-blue-800",
      medium: "bg-yellow-100 text-yellow-800",
      high: "bg-orange-100 text-orange-800",
      critical: "bg-red-100 text-red-800"
    };
    return (
      <Badge className={colors[priority]} variant="outline">
        {priority.toUpperCase()}
      </Badge>
    );
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Violation Reports</CardTitle>
        <CardDescription>
          All crowdsourced violation reports with ML classification
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col md:flex-row gap-4 mb-4">
          <div className="relative flex-1">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search by ID, location, or barangay..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-8"
            />
          </div>
          <Select value={statusFilter} onValueChange={setStatusFilter}>
            <SelectTrigger className="w-full md:w-[180px]">
              <SelectValue placeholder="Filter by status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Status</SelectItem>
              <SelectItem value="pending">Pending</SelectItem>
              <SelectItem value="in-progress">In Progress</SelectItem>
              <SelectItem value="resolved">Resolved</SelectItem>
              <SelectItem value="rejected">Rejected</SelectItem>
            </SelectContent>
          </Select>
          <Select value={categoryFilter} onValueChange={setCategoryFilter}>
            <SelectTrigger className="w-full md:w-[200px]">
              <SelectValue placeholder="Filter by category" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Categories</SelectItem>
              <SelectItem value="Illegal Parking">Illegal Parking</SelectItem>
              <SelectItem value="Road Obstruction">Road Obstruction</SelectItem>
              <SelectItem value="Sidewalk Encroachment">Sidewalk Encroachment</SelectItem>
              <SelectItem value="Unauthorized Structure">Unauthorized Structure</SelectItem>
              <SelectItem value="Noise Violation">Noise Violation</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="rounded-md border overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Report ID</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Location</TableHead>
                <TableHead>Barangay</TableHead>
                <TableHead>ML Category</TableHead>
                <TableHead>Confidence</TableHead>
                <TableHead>Priority</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredViolations.map((violation) => (
                <TableRow key={violation.id}>
                  <TableCell className="font-medium">{violation.id}</TableCell>
                  <TableCell>{violation.date}</TableCell>
                  <TableCell className="max-w-[200px]">
                    <div className="flex items-start gap-2">
                      <MapPin className="h-4 w-4 text-muted-foreground mt-0.5 flex-shrink-0" />
                      <span className="text-sm">{violation.location}</span>
                    </div>
                  </TableCell>
                  <TableCell>{violation.barangay}</TableCell>
                  <TableCell>{violation.category}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <div className="w-12 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-green-600 h-2 rounded-full"
                          style={{ width: `${violation.mlConfidence}%` }}
                        />
                      </div>
                      <span className="text-sm">{violation.mlConfidence}%</span>
                    </div>
                  </TableCell>
                  <TableCell>{getPriorityBadge(violation.priority)}</TableCell>
                  <TableCell>{getStatusBadge(violation.status)}</TableCell>
                  <TableCell>
                    <Button variant="ghost" size="sm">
                      <Eye className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
}
