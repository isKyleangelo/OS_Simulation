import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Progress } from "./ui/progress";
import { Brain, CheckCircle, TrendingUp } from "lucide-react";

export function MLClassificationPanel() {
  const recentClassifications = [
    {
      id: "V-2026-001",
      prediction: "Illegal Parking",
      confidence: 94.2,
      features: ["Vehicle present", "No parking zone", "Daytime hours"],
      timestamp: "2 minutes ago"
    },
    {
      id: "V-2026-002",
      prediction: "Sidewalk Encroachment",
      confidence: 89.7,
      features: ["Sidewalk blocked", "Commercial items", "Public space"],
      timestamp: "15 minutes ago"
    },
    {
      id: "V-2026-003",
      prediction: "Road Obstruction",
      confidence: 96.5,
      features: ["Main road blocked", "Construction materials", "No permit visible"],
      timestamp: "1 hour ago"
    }
  ];

  const modelMetrics = [
    { label: "Overall Accuracy", value: 92.3 },
    { label: "Precision", value: 90.1 },
    { label: "Recall", value: 88.7 },
    { label: "F1 Score", value: 89.4 }
  ];

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>ML Classification System</CardTitle>
              <CardDescription>
                Machine Learning-Based Violation Classification
              </CardDescription>
            </div>
            <Brain className="h-8 w-8 text-purple-600" />
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-4">
            {modelMetrics.map((metric) => (
              <div key={metric.label} className="space-y-2">
                <p className="text-sm font-medium text-muted-foreground">{metric.label}</p>
                <p className="text-2xl font-bold">{metric.value}%</p>
                <Progress value={metric.value} className="h-2" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Recent Classifications</CardTitle>
          <CardDescription>Latest ML predictions and confidence scores</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentClassifications.map((classification) => (
              <div key={classification.id} className="border rounded-lg p-4 space-y-3">
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-medium">{classification.id}</span>
                      <Badge variant="outline">{classification.prediction}</Badge>
                    </div>
                    <p className="text-sm text-muted-foreground">{classification.timestamp}</p>
                  </div>
                  <CheckCircle className="h-5 w-5 text-green-600" />
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Confidence Score</span>
                    <span className="text-sm font-bold">{classification.confidence}%</span>
                  </div>
                  <Progress value={classification.confidence} className="h-2" />
                </div>

                <div className="space-y-2">
                  <span className="text-sm font-medium">Key Features Detected:</span>
                  <div className="flex flex-wrap gap-2">
                    {classification.features.map((feature, idx) => (
                      <Badge key={idx} variant="secondary" className="text-xs">
                        {feature}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Model Information</CardTitle>
          <CardDescription>Classification algorithm details</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex justify-between">
            <span className="text-sm font-medium">Algorithm:</span>
            <span className="text-sm">Random Forest + CNN Ensemble</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm font-medium">Training Dataset:</span>
            <span className="text-sm">8,472 labeled violations</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm font-medium">Last Updated:</span>
            <span className="text-sm">April 15, 2026</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm font-medium">Categories:</span>
            <span className="text-sm">5 violation types</span>
          </div>
          <div className="flex items-center gap-2 pt-2">
            <TrendingUp className="h-4 w-4 text-green-600" />
            <span className="text-sm text-green-600 font-medium">
              Accuracy improved 4.2% this month
            </span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
