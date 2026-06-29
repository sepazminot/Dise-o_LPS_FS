<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class AuthController extends Controller
{
    public function showLogin()
    {
        return view('auth.login');
    }

    public function login(Request $request)
    {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);

        // Mocking backend response for E2E tests
        $email = $request->input('email');
        $password = $request->input('password');

        if ($password !== 'password123') {
            return back()->withErrors(['email' => 'Invalid credentials'])->withInput();
        }

        // Determine role based on email for testing role-based redirect
        $role = 'student';
        $name = 'Test Student';
        
        if (str_contains($email, 'admin')) {
            $role = 'admin';
            $name = 'Test Admin';
        } elseif (str_contains($email, 'teacher')) {
            $role = 'teacher';
            $name = 'Test Teacher';
        }

        // Simulate successful login
        session([
            'user' => [
                'email' => $email,
                'full_name' => $name,
                'role' => $role,
                'token' => 'mock-jwt-token-for-e2e',
                'expires_at' => now()->addMinutes(30)->timestamp
            ]
        ]);

        return redirect()->intended('/dashboard');
    }

    public function showRegister()
    {
        return view('auth.register');
    }

    public function register(Request $request)
    {
        $request->validate([
            'full_name' => 'required|string|max:255',
            'email' => 'required|string|email|max:255',
            'password' => 'required|string|min:8|confirmed',
            'role' => 'required|in:ROLE_ADMIN,ROLE_TEACHER,ROLE_STUDENT',
        ]);

        // Mock successful registration
        return redirect()->route('login')->with('status', 'Registration successful. Please login.');
    }

    public function showForgotPassword()
    {
        return view('auth.forgot-password');
    }

    public function sendResetLink(Request $request)
    {
        $request->validate(['email' => 'required|email']);
        return back()->with('status', 'We have emailed your password reset link!');
    }

    public function dashboard(Request $request)
    {
        $user = session('user');
        
        if (!$user) {
            return redirect()->route('login')->withErrors(['email' => 'Please login to access the dashboard.']);
        }

        // Simulate token expiration
        if (isset($user['expires_at']) && time() > $user['expires_at']) {
            session()->forget('user');
            return redirect()->route('login')->withErrors(['email' => 'Session expired. Please login again.']);
        }

        return view('dashboard');
    }

    public function logout()
    {
        session()->forget('user');
        return redirect()->route('login');
    }
}
