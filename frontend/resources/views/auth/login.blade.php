@extends('layouts.guest')

@section('content')
<div class="mb-6">
    <h2 class="text-3xl font-extrabold text-slate-900 text-center tracking-tight">Sign in</h2>
    <p class="mt-2 text-center text-sm text-slate-600">
        Or
        <a href="{{ route('register') }}" class="font-medium text-primary-600 hover:text-primary-500 transition-colors focus:outline-none focus:underline rounded">
            create a new account
        </a>
    </p>
</div>

<!-- Form -->
<form method="POST" action="{{ route('login') }}" class="space-y-5" aria-label="Login Form">
    @csrf

    @if ($errors->any())
        <div class="bg-red-50 text-red-600 text-sm p-3 rounded-lg border border-red-100" role="alert">
            <ul class="list-disc list-inside">
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <div>
        <label for="email" class="block text-sm font-medium text-slate-700">Email address</label>
        <div class="mt-1">
            <input id="email" name="email" type="email" autocomplete="email" required autofocus
                   class="appearance-none block w-full px-3 py-2 border border-slate-300 rounded-lg shadow-sm placeholder-slate-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-shadow"
                   value="{{ old('email') }}"
                   aria-required="true"
                   aria-invalid="{{ $errors->has('email') ? 'true' : 'false' }}">
        </div>
    </div>

    <div>
        <label for="password" class="block text-sm font-medium text-slate-700">Password</label>
        <div class="mt-1">
            <input id="password" name="password" type="password" autocomplete="current-password" required
                   class="appearance-none block w-full px-3 py-2 border border-slate-300 rounded-lg shadow-sm placeholder-slate-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-shadow"
                   aria-required="true"
                   aria-invalid="{{ $errors->has('password') ? 'true' : 'false' }}">
        </div>
    </div>

    <div class="flex items-center justify-between">
        <div class="flex items-center">
            <input id="remember" name="remember" type="checkbox"
                   class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-slate-300 rounded cursor-pointer transition-colors">
            <label for="remember" class="ml-2 block text-sm text-slate-700 cursor-pointer">
                Remember me
            </label>
        </div>

        <div class="text-sm">
            <a href="{{ route('password.request') }}" class="font-medium text-primary-600 hover:text-primary-500 focus:outline-none focus:underline rounded transition-colors">
                Forgot your password?
            </a>
        </div>
    </div>

    <div>
        <button type="submit"
                class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-all active:scale-[0.98]">
            Sign in
        </button>
    </div>
</form>
@endsection
