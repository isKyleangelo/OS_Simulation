import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { ViolationStats } from "./components/ViolationStats";
import { ReportForm } from "./components/ReportForm";
import { ViolationsTable } from "./components/ViolationsTable";
import { ViolationCharts } from "./components/ViolationCharts";
import { MLClassificationPanel } from "./components/MLClassificationPanel";
import { MapView } from "./components/MapView";
import { Toaster } from "./components/ui/sonner";
import { BarChart3, FileText, Map, Brain, AlertTriangle, Home } from "lucide-react";

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Toaster />

      <header className="bg-white border-b sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="h-12 w-12 bg-blue-600 rounded-lg flex items-center justify-center">
                <AlertTriangle className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold">DILG Santa Cruz</h1>
                <p className="text-sm text-muted-foreground">Community Violation Reporting System</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <div className="hidden md:block text-right">
                <p className="text-sm font-medium">Santa Cruz, Laguna</p>
                <p className="text-xs text-muted-foreground">Road Clearing & Public Order</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-2 lg:grid-cols-6 h-auto">
            <TabsTrigger value="overview" className="flex items-center gap-2">
              <Home className="h-4 w-4" />
              Overview
            </TabsTrigger>
            <TabsTrigger value="report" className="flex items-center gap-2">
              <FileText className="h-4 w-4" />
              Report
            </TabsTrigger>
            <TabsTrigger value="violations" className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4" />
              Violations
            </TabsTrigger>
            <TabsTrigger value="analytics" className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              Analytics
            </TabsTrigger>
            <TabsTrigger value="ml" className="flex items-center gap-2">
              <Brain className="h-4 w-4" />
              ML System
            </TabsTrigger>
            <TabsTrigger value="map" className="flex items-center gap-2">
              <Map className="h-4 w-4" />
              Map
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold tracking-tight">Dashboard Overview</h2>
              <p className="text-muted-foreground">
                Crowdsourced violation reporting with ML-based classification for DILG compliance
              </p>
            </div>
            <ViolationStats />
            <div className="grid gap-6 md:grid-cols-2">
              <ViolationsTable />
              <div className="space-y-6">
                <MapView />
              </div>
            </div>
          </TabsContent>

          <TabsContent value="report" className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold tracking-tight">Submit a Violation Report</h2>
              <p className="text-muted-foreground">
                Report road clearing or public order violations in your community
              </p>
            </div>
            <div className="grid gap-6 md:grid-cols-3">
              <div className="md:col-span-2">
                <ReportForm />
              </div>
              <div>
                <MLClassificationPanel />
              </div>
            </div>
          </TabsContent>

          <TabsContent value="violations" className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold tracking-tight">All Violation Reports</h2>
              <p className="text-muted-foreground">
                Browse, filter, and manage community violation reports
              </p>
            </div>
            <ViolationsTable />
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold tracking-tight">Analytics & Insights</h2>
              <p className="text-muted-foreground">
                Data visualization and trends for violation reports
              </p>
            </div>
            <ViolationStats />
            <ViolationCharts />
          </TabsContent>

          <TabsContent value="ml" className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold tracking-tight">ML Classification System</h2>
              <p className="text-muted-foreground">
                Machine learning model performance and real-time classification
              </p>
            </div>
            <MLClassificationPanel />
          </TabsContent>

          <TabsContent value="map" className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold tracking-tight">Geographic Distribution</h2>
              <p className="text-muted-foreground">
                Map view of violation hotspots across Santa Cruz barangays
              </p>
            </div>
            <MapView />
          </TabsContent>
        </Tabs>
      </main>

      <footer className="bg-white border-t mt-12">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm text-muted-foreground">
              Research Project: Crowdsourced Community Violation Reporting System
            </p>
            <p className="text-sm text-muted-foreground">
              DILG Road Clearing & Public Order Policies - Santa Cruz, Laguna
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}