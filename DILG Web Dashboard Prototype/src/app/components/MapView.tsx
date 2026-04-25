import { useState } from "react";
import { Card, CardContent } from "./ui/card";
import { Button } from "./ui/button";

export function MapView() {
  const [viewMode, setViewMode] = useState<"markers" | "heatmap">("markers");
  const [categoryFilter, setCategoryFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");

  const violations = [
    { id: 1, lat: 14.28, lng: 121.42, type: "Illegal Parking", status: "pending", barangay: "Poblacion I" },
    { id: 2, lat: 14.29, lng: 121.41, type: "Road Obstruction", status: "resolved", barangay: "Poblacion II" },
    { id: 3, lat: 14.27, lng: 121.43, type: "Sidewalk Encroachment", status: "pending", barangay: "Pagsawitan" },
    { id: 4, lat: 14.30, lng: 121.40, type: "Unauthorized Structure", status: "pending", barangay: "Bagumbayan" },
    { id: 5, lat: 14.26, lng: 121.44, type: "Noise Violation", status: "resolved", barangay: "Bambang" },
    { id: 6, lat: 14.28, lng: 121.39, type: "Illegal Parking", status: "pending", barangay: "Duhat" },
    { id: 7, lat: 14.31, lng: 121.41, type: "Road Obstruction", status: "resolved", barangay: "Gatid" },
    { id: 8, lat: 14.27, lng: 121.40, type: "Sidewalk Encroachment", status: "pending", barangay: "Poblacion I" },
  ];

  const getStatusColor = (status: string) => {
    return status === "pending" ? "#f59e0b" : "#16a34a";
  };

  const filteredViolations = violations.filter((v) => {
    if (statusFilter !== "all" && v.status !== statusFilter) return false;
    return true;
  });

  return (
    <div className="flex gap-4 h-full">
      {/* Sidebar */}
      <Card className="w-80 flex-shrink-0">
        <CardContent className="p-4 space-y-6">
          {/* View Mode */}
          <div>
            <h3 className="text-sm font-semibold mb-3">View Mode</h3>
            <div className="flex gap-2">
              <Button
                variant={viewMode === "markers" ? "default" : "outline"}
                size="sm"
                onClick={() => setViewMode("markers")}
                className="flex-1"
              >
                Markers
              </Button>
              <Button
                variant={viewMode === "heatmap" ? "default" : "outline"}
                size="sm"
                onClick={() => setViewMode("heatmap")}
                className="flex-1"
              >
                Heatmap
              </Button>
            </div>
          </div>

          {/* Filters */}
          <div>
            <h3 className="text-sm font-semibold mb-3">Filters</h3>
            <div className="space-y-3">
              <div>
                <label className="text-xs font-medium text-muted-foreground">Category</label>
                <select
                  value={categoryFilter}
                  onChange={(e) => setCategoryFilter(e.target.value)}
                  className="w-full mt-1 px-3 py-2 border rounded-md text-sm"
                >
                  <option value="all">All Categories</option>
                  <option value="parking">Illegal Parking</option>
                  <option value="obstruction">Road Obstruction</option>
                  <option value="sidewalk">Sidewalk Encroachment</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-medium text-muted-foreground">Status</label>
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="w-full mt-1 px-3 py-2 border rounded-md text-sm"
                >
                  <option value="all">All Status</option>
                  <option value="pending">Pending</option>
                  <option value="resolved">Resolved</option>
                </select>
              </div>
            </div>
          </div>

          {/* Legend */}
          <div>
            <h3 className="text-sm font-semibold mb-3">Legend</h3>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <div className="h-3 w-3 rounded-full bg-amber-400" />
                <span className="text-sm">Pending</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-3 w-3 rounded-full bg-green-500" />
                <span className="text-sm">Resolved</span>
              </div>
            </div>
          </div>

          {/* Report Count */}
          <div className="text-xs text-muted-foreground">
            Showing {filteredViolations.length} of {violations.length} reports
          </div>
        </CardContent>
      </Card>

      {/* Map Area */}
      <Card className="flex-1">
        <CardContent className="p-0 h-full">
          <div className="relative bg-slate-100 h-full rounded-lg overflow-hidden flex flex-col">
            {/* Search/Location Bar */}
            <div className="bg-white border-b p-4">
              <input
                type="text"
                placeholder="Santa Cruz, Laguna"
                className="w-full px-3 py-2 border rounded-md text-sm"
              />
            </div>

            {/* Map */}
            <div className="flex-1 bg-gradient-to-br from-blue-50 to-slate-100 relative">
              <svg className="w-full h-full">
                {/* Grid */}
                <defs>
                  <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
                    <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#e2e8f0" strokeWidth="0.5" />
                  </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#grid)" />

                {/* Markers */}
                {filteredViolations.map((violation) => {
                  const x = ((violation.lng - 121.38) / 0.07) * 100;
                  const y = ((14.32 - violation.lat) / 0.06) * 100;

                  return (
                    <g key={violation.id} className="cursor-pointer hover:opacity-80">
                      {/* Marker pin */}
                      <circle
                        cx={`${x}%`}
                        cy={`${y}%`}
                        r="14"
                        fill={getStatusColor(violation.status)}
                        opacity="0.9"
                      />
                      <circle
                        cx={`${x}%`}
                        cy={`${y}%`}
                        r="14"
                        fill={getStatusColor(violation.status)}
                        opacity="0.2"
                        className="animate-pulse"
                      />
                    </g>
                  );
                })}
              </svg>
            </div>

            {/* Footer */}
            <div className="bg-white border-t p-2 text-right">
              <span className="text-xs text-muted-foreground">Marker View</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
