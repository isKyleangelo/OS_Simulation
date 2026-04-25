<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class ViolationReport extends Model
{
    protected $table = 'violation_reports';

    protected $fillable = [
        'report_id',
        'reporter_name',
        'contact',
        'location',
        'barangay',
        'priority',
        'description',
        'category',
        'ml_confidence',
        'status',
        'evidence_path',
    ];

    protected $casts = [
        'ml_confidence' => 'float',
        'created_at' => 'datetime',
        'updated_at' => 'datetime',
    ];
}
