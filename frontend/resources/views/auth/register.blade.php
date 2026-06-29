@extends('layouts.guest')

@section('content')
<div class="mb-6">
    <h2 class="text-3xl font-extrabold text-slate-900 text-center tracking-tight">Create an account</h2>
    <p class="mt-2 text-center text-sm text-slate-600">
        Or
        <a href="{{ route('login') }}" class="font-medium text-primary-600 hover:text-primary-500 transition-colors focus:outline-none focus:underline rounded">
            sign in to your account
        </a>
    </p>
</div>

<!-- Form -->
<form method="POST" action="{{ route('register') }}" class="space-y-4" aria-label="Register Form">
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
        <label for="full_name" class="block text-sm font-medium text-slate-700">Full Name</label>
        <div class="mt-1">
            <input id="full_name" name="full_name" type="text" autocomplete="name" required autofocus
                   class="appearance-none block w-full px-3 py-2 border border-slate-300 rounded-lg shadow-sm placeholder-slate-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-shadow"
                   value="{{ old('full_name') }}"
                   aria-required="true"
                   aria-invalid="{{ $errors->has('full_name') ? 'true' : 'false' }}">
        </div>
    </div>

    <div>
        <label for="email" class="block text-sm font-medium text-slate-700">Email address</label>
        <div class="mt-1">
            <input id="email" name="email" type="email" autocomplete="email" required
                   class="appearance-none block w-full px-3 py-2 border border-slate-300 rounded-lg shadow-sm placeholder-slate-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-shadow"
                   value="{{ old('email') }}"
                   aria-required="true"
                   aria-invalid="{{ $errors->has('email') ? 'true' : 'false' }}">
        </div>
    </div>

    <div>
        <label for="role" class="block text-sm font-medium text-slate-700">Role</label>
        <div class="mt-1">
            <select id="role" name="role" required
                   class="appearance-none block w-full px-3 py-2 border border-slate-300 rounded-lg shadow-sm bg-white focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-shadow"
                   aria-required="true">
                <option value="ROLE_STUDENT" {{ old('role') == 'ROLE_STUDENT' ? 'selected' : '' }}>Student</option>
                <option value="ROLE_TEACHER" {{ old('role') == 'ROLE_TEACHER' ? 'selected' : '' }}>Teacher</option>
                <option value="ROLE_ADMIN" {{ old('role') == 'ROLE_ADMIN' ? 'selected' : '' }}>Admin</option>
            </select>
        </div>
    </div>

    <div>
        <label for="password" class="block text-sm font-medium text-slate-700">Password</label>
        <div class="mt-1">
            <input id="password" name="password" type="password" autocomplete="new-password" required
                   class="appearance-none block w-full px-3 py-2 border border-slate-300 rounded-lg shadow-sm placeholder-slate-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-shadow"
                   aria-required="true"
                   aria-invalid="{{ $errors->has('password') ? 'true' : 'false' }}">
        </div>
    </div>

    <div>
        <label for="password_confirmation" class="block text-sm font-medium text-slate-700">Confirm Password</label>
        <div class="mt-1">
            <input id="password_confirmation" name="password_confirmation" type="password" autocomplete="new-password" required
                   class="appearance-none block w-full px-3 py-2 border border-slate-300 rounded-lg shadow-sm placeholder-slate-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-shadow"
                   aria-required="true">
        </div>
    </div>

    <div class="pt-2">
        <button type="submit"
                class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-all active:scale-[0.98]">
            Sign up
        </button>
    </div>
</form>
@endsection
