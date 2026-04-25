<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('violation_reports', function (Blueprint $table) {
            $table->id();
            $table->string('report_id')->unique();
            $table->string('reporter_name');
            $table->string('contact');
            $table->string('location');
            $table->string('barangay');
            $table->string('priority');
            $table->text('description');
            $table->string('category')->nullable();
            $table->decimal('ml_confidence', 5, 2)->nullable();
            $table->enum('status', ['pending', 'in-progress', 'resolved', 'rejected'])->default('pending');
            $table->string('evidence_path')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('violation_reports');
    }
};
