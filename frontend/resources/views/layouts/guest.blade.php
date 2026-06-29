<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="csrf-token" content="{{ csrf_token() }}">

    <title>{{ config('app.name', 'Educational DevOps') }}</title>

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.bunny.net">
    <link href="https://fonts.bunny.net/css?family=inter:400,500,600,700&display=swap" rel="stylesheet" />

    <!-- Scripts -->
    @vite(['src/main.js', 'src/style.css'])
</head>
<body class="font-sans text-slate-900 antialiased bg-slate-50 relative min-h-screen flex items-center justify-center overflow-hidden">
    <!-- Background Design -->
    <div class="absolute inset-0 z-0">
        <div class="absolute inset-0 bg-gradient-to-br from-primary-50 to-primary-100"></div>
        <div class="absolute top-0 left-1/4 w-96 h-96 bg-primary-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
        <div class="absolute top-0 right-1/4 w-96 h-96 bg-primary-400 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
        <div class="absolute -bottom-32 left-1/2 w-96 h-96 bg-primary-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-4000"></div>
    </div>

    <!-- Page Content -->
    <main class="relative z-10 w-full sm:max-w-md mt-6 px-6 py-8 bg-white/80 backdrop-blur-xl shadow-2xl sm:rounded-2xl border border-white/50">
        <!-- Logo -->
        <div class="flex justify-center mb-8">
            <a href="/" class="flex items-center gap-2" aria-label="Home">
                <div class="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-primary-500/30">
                    ED
                </div>
                <span class="text-2xl font-bold text-slate-800 tracking-tight">Educational</span>
            </a>
        </div>

        @yield('content')
    </main>

    <style>
        .animate-blob {
            animation: blob 7s infinite;
        }
        .animation-delay-2000 {
            animation-delay: 2s;
        }
        .animation-delay-4000 {
            animation-delay: 4s;
        }
        @keyframes blob {
            0% { transform: translate(0px, 0px) scale(1); }
            33% { transform: translate(30px, -50px) scale(1.1); }
            66% { transform: translate(-20px, 20px) scale(0.9); }
            100% { transform: translate(0px, 0px) scale(1); }
        }
    </style>
</body>
</html>
