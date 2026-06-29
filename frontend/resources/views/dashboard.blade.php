@extends('layouts.app')

@section('content')
<div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
    <div class="border-b border-slate-200 bg-slate-50 px-6 py-5">
        <h3 class="text-lg leading-6 font-medium text-slate-900">
            Dashboard
        </h3>
        <p class="mt-1 text-sm text-slate-500">
            Welcome back to the Educational DevOps platform.
        </p>
    </div>
    
    <div class="px-6 py-5">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- User Info Card -->
            <div class="bg-primary-50 rounded-xl p-5 border border-primary-100 flex flex-col items-center text-center">
                <div class="w-16 h-16 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-2xl font-bold mb-3 shadow-inner">
                    {{ substr(session('user.full_name', 'U'), 0, 1) }}
                </div>
                <h4 class="font-semibold text-slate-900 text-lg">{{ session('user.full_name', 'User') }}</h4>
                <p class="text-primary-600 font-medium mt-1">{{ ucfirst(session('user.role', 'Guest')) }}</p>
                <p class="text-slate-500 text-sm mt-1">{{ session('user.email', 'email@example.com') }}</p>
            </div>

            <!-- Quick Actions -->
            <div class="md:col-span-2">
                <h4 class="font-semibold text-slate-900 text-md mb-4">Quick Links</h4>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    @if(session('user.role') == 'admin')
                        <a href="#" class="group block p-4 bg-white border border-slate-200 rounded-xl hover:border-primary-500 hover:shadow-md transition-all">
                            <div class="font-medium text-slate-900 group-hover:text-primary-600">Manage Users</div>
                            <div class="text-sm text-slate-500 mt-1">Add, edit, or remove users</div>
                        </a>
                        <a href="#" class="group block p-4 bg-white border border-slate-200 rounded-xl hover:border-primary-500 hover:shadow-md transition-all">
                            <div class="font-medium text-slate-900 group-hover:text-primary-600">System Settings</div>
                            <div class="text-sm text-slate-500 mt-1">Configure platform options</div>
                        </a>
                    @elseif(session('user.role') == 'teacher')
                        <a href="#" class="group block p-4 bg-white border border-slate-200 rounded-xl hover:border-primary-500 hover:shadow-md transition-all">
                            <div class="font-medium text-slate-900 group-hover:text-primary-600">My Courses</div>
                            <div class="text-sm text-slate-500 mt-1">Manage your assigned courses</div>
                        </a>
                        <a href="#" class="group block p-4 bg-white border border-slate-200 rounded-xl hover:border-primary-500 hover:shadow-md transition-all">
                            <div class="font-medium text-slate-900 group-hover:text-primary-600">Grade Students</div>
                            <div class="text-sm text-slate-500 mt-1">Input grades and evaluations</div>
                        </a>
                    @else
                        <a href="#" class="group block p-4 bg-white border border-slate-200 rounded-xl hover:border-primary-500 hover:shadow-md transition-all">
                            <div class="font-medium text-slate-900 group-hover:text-primary-600">My Enrollment</div>
                            <div class="text-sm text-slate-500 mt-1">View courses you are enrolled in</div>
                        </a>
                        <a href="#" class="group block p-4 bg-white border border-slate-200 rounded-xl hover:border-primary-500 hover:shadow-md transition-all">
                            <div class="font-medium text-slate-900 group-hover:text-primary-600">Academic Record</div>
                            <div class="text-sm text-slate-500 mt-1">Check your grades and progress</div>
                        </a>
                    @endif
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
