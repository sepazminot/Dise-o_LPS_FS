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
<body class="font-sans text-slate-900 antialiased bg-slate-50 min-h-screen">
    <!-- Navbar -->
    <nav class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex">
                    <!-- Logo -->
                    <div class="shrink-0 flex items-center">
                        <a href="{{ route('dashboard') }}" class="flex items-center gap-2" aria-label="Dashboard">
                            <div class="w-8 h-8 bg-primary-600 rounded flex items-center justify-center text-white font-bold text-sm shadow-md">
                                ED
                            </div>
                            <span class="font-bold text-slate-800 hidden sm:block">Educational</span>
                        </a>
                    </div>
                </div>

                <div class="flex items-center gap-4">
                    <span class="text-sm font-medium text-slate-600">
                        {{ session('user.full_name', 'User') }} ({{ ucfirst(session('user.role', 'Guest')) }})
                    </span>
                    
                    <form method="POST" action="{{ route('logout') }}">
                        @csrf
                        <button type="submit" class="text-sm font-medium text-slate-500 hover:text-slate-700 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 rounded px-2 py-1">
                            Log Out
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </nav>

    <!-- Page Content -->
    <main class="py-10 max-w-7xl mx-auto sm:px-6 lg:px-8">
        @if (session('status'))
            <div class="mb-4 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg flex items-center" role="alert">
                <span class="block sm:inline">{{ session('status') }}</span>
            </div>
        @endif

        @if ($errors->any())
            <div class="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg" role="alert">
                <ul class="list-disc list-inside text-sm">
                    @foreach ($errors->all() as $error)
                        <li>{{ $error }}</li>
                    @endforeach
                </ul>
            </div>
        @endif

        @yield('content')
    </main>
</body>
</html>
