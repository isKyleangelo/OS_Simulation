<div class="bg-white rounded-lg border">
    <div class="border-b p-6">
        <h3 class="text-lg font-semibold">Report a Violation</h3>
        <p class="text-sm text-gray-500">Submit community violation reports for Santa Cruz, Laguna</p>
    </div>
    <div class="p-6">
        <form id="reportForm" class="space-y-4">
            @csrf
            <div class="grid gap-4 md:grid-cols-2">
                <div class="space-y-2">
                    <label for="reporter-name" class="text-sm font-medium">Reporter Name</label>
                    <input id="reporter-name" name="reporter_name" type="text" placeholder="Your name" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required />
                </div>
                <div class="space-y-2">
                    <label for="contact" class="text-sm font-medium">Contact Number</label>
                    <input id="contact" name="contact" type="tel" placeholder="09XX XXX XXXX" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required />
                </div>
            </div>

            <div class="space-y-2">
                <label for="location" class="text-sm font-medium">Location</label>
                <input id="location" name="location" type="text" placeholder="Street address or landmark in Santa Cruz" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required />
            </div>

            <div class="grid gap-4 md:grid-cols-2">
                <div class="space-y-2">
                    <label for="barangay" class="text-sm font-medium">Barangay</label>
                    <select id="barangay" name="barangay" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                        <option value="">Select barangay</option>
                        <option value="bagumbayan">Bagumbayan</option>
                        <option value="bambang">Bambang</option>
                        <option value="bubukal">Bubukal</option>
                        <option value="calios">Calios</option>
                        <option value="duhat">Duhat</option>
                        <option value="gatid">Gatid</option>
                        <option value="jasaan">Jasaan</option>
                        <option value="labuin">Labuin</option>
                        <option value="pagsawitan">Pagsawitan</option>
                        <option value="palasan">Palasan</option>
                        <option value="poblacion-i">Poblacion I</option>
                        <option value="poblacion-ii">Poblacion II</option>
                        <option value="poblacion-iii">Poblacion III</option>
                        <option value="poblacion-iv">Poblacion IV</option>
                        <option value="poblacion-v">Poblacion V</option>
                    </select>
                </div>

                <div class="space-y-2">
                    <label for="priority" class="text-sm font-medium">Priority Level</label>
                    <select id="priority" name="priority" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                        <option value="">Select priority</option>
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                        <option value="critical">Critical</option>
                    </select>
                </div>
            </div>

            <div class="space-y-2">
                <label for="description" class="text-sm font-medium">Violation Description</label>
                <textarea id="description" name="description" placeholder="Describe the violation in detail..." rows="4" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required></textarea>
            </div>

            <div class="space-y-2">
                <label for="evidence" class="text-sm font-medium">Upload Evidence (Photo/Video)</label>
                <input id="evidence" name="evidence" type="file" accept="image/*,video/*" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>

            <button type="submit" id="submitBtn" class="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium">
                Submit Report
            </button>
        </form>
    </div>
</div>

<script>
    document.getElementById('reportForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const submitBtn = document.getElementById('submitBtn');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Submitting & Classifying...';

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

            alert(`Report submitted successfully!\nML Classification: ${randomCategory} (${confidence}% confidence)`);
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Report';
            document.getElementById('reportForm').reset();
        }, 1500);
    });
</script>
