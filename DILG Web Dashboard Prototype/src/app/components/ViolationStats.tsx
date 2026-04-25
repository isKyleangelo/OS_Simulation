import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { AlertTriangle, CheckCircle, Clock, TrendingUp } from "lucide-react";

export function ViolationStats() {
  const stats = [
    {
      title: "Total Reports",
      value: "2,847",
      change: "+12.5%",
      icon: AlertTriangle,
      color: "text-blue-600",
    },
    {
      title: "Resolved",
      value: "2,103",
      change: "+8.2%",
      icon: CheckCircle,
      color: "text-green-600",
    },
    {
      title: "Pending",
      value: "544",
      change: "-5.1%",
      icon: Clock,
      color: "text-yellow-600",
    },
    {
      title: "This Month",
      value: "198",
      change: "+23.4%",
      icon: TrendingUp,
      color: "text-purple-600",
    },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => (
        <Card key={stat.title}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
            <stat.icon className={`h-4 w-4 ${stat.color}`} />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stat.value}</div>
            <p className="text-xs text-muted-foreground">
              <span className={stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}>
                {stat.change}
              </span>{' '}
              from last month
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
