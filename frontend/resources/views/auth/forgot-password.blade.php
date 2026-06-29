@extends('layouts.guest')

@section('content')
<div class="mb-6">
    <h2 class="text-3xl font-extrabold text-slate-900 text-center tracking-tight">Reset password</h2>
    <p class="mt-2 text-center text-sm text-slate-600">
        Forgot your password? No problem. Just let us know your email address and we will email you a password reset link.
    </p>
</div>

<!-- Form -->
<form method="POST" action="{{ route('password.email') }}" class="space-y-5" aria-label="Forgot Password Form">
    @csrf

    @if (session('status'))
        <div class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg flex items-center" role="alert">
            <span class="block sm:inline text-sm">{{ session('status') }}</span>
        </div>
    @endif

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

    <div class="flex items-center justify-between mt-4">
        <a href="{{ route('login') }}" class="text-sm font-medium text-primary-600 hover:text-primary-500 focus:outline-none focus:underline rounded transition-colors">
            Back to login
        </a>

        <button type="submit"
                class="flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-all active:scale-[0.98]">
            Email Password Reset Link
        </button>
    </div>
</form>
@endsection
