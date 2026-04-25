import { useState } from "react";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { toast } from "sonner";

export function ReportForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    // Simulate ML classification
    setTimeout(() => {
      const categories = [
        "Illegal Parking",
        "Road Obstruction",
        "Sidewalk Encroachment",
        "Unauthorized Structure",
        "Noise Violation"
      ];
      const randomCategory = categories[Math.floor(Math.random() * categories.length)];
      const confidence = (85 + Math.random() * 12).toFixed(1);

      toast.success(`Report submitted successfully! ML Classification: ${randomCategory} (${confidence}% confidence)`);
      setIsSubmitting(false);
      (e.target as HTMLFormElement).reset();
    }, 1500);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Report a Violation</CardTitle>
        <CardDescription>
          Submit community violation reports for Santa Cruz, Laguna
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="reporter-name">Reporter Name</Label>
              <Input id="reporter-name" placeholder="Your name" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="contact">Contact Number</Label>
              <Input id="contact" type="tel" placeholder="09XX XXX XXXX" required />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="location">Location</Label>
            <Input id="location" placeholder="Street address or landmark in Santa Cruz" required />
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="barangay">Barangay</Label>
              <Select required>
                <SelectTrigger id="barangay">
                  <SelectValue placeholder="Select barangay" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="bagumbayan">Bagumbayan</SelectItem>
                  <SelectItem value="bambang">Bambang</SelectItem>
                  <SelectItem value="bubukal">Bubukal</SelectItem>
                  <SelectItem value="calios">Calios</SelectItem>
                  <SelectItem value="duhat">Duhat</SelectItem>
                  <SelectItem value="gatid">Gatid</SelectItem>
                  <SelectItem value="jasaan">Jasaan</SelectItem>
                  <SelectItem value="labuin">Labuin</SelectItem>
                  <SelectItem value="pagsawitan">Pagsawitan</SelectItem>
                  <SelectItem value="palasan">Palasan</SelectItem>
                  <SelectItem value="poblacion-i">Poblacion I</SelectItem>
                  <SelectItem value="poblacion-ii">Poblacion II</SelectItem>
                  <SelectItem value="poblacion-iii">Poblacion III</SelectItem>
                  <SelectItem value="poblacion-iv">Poblacion IV</SelectItem>
                  <SelectItem value="poblacion-v">Poblacion V</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="priority">Priority Level</Label>
              <Select required>
                <SelectTrigger id="priority">
                  <SelectValue placeholder="Select priority" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="critical">Critical</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Violation Description</Label>
            <Textarea
              id="description"
              placeholder="Describe the violation in detail..."
              rows={4}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="evidence">Upload Evidence (Photo/Video)</Label>
            <Input id="evidence" type="file" accept="image/*,video/*" />
          </div>

          <Button type="submit" className="w-full" disabled={isSubmitting}>
            {isSubmitting ? "Submitting & Classifying..." : "Submit Report"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
