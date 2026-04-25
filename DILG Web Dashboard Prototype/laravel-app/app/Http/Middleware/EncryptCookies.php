<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Cookie\Middleware\EncryptCookies as Middleware;
use Illuminate\Http\Request;

class EncryptCookies extends Middleware
{
    protected $except = [];
}
