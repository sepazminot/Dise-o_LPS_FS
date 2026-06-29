import { test, expect } from '@playwright/test';

test.describe('Auth Flow E2E Tests', () => {

  test('login exitoso', async ({ page }) => {
    await page.goto('/login');
    
    // Fill credentials
    await page.fill('input[name="email"]', 'student@example.com');
    await page.fill('input[name="password"]', 'password123');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Expect redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h3:has-text("Dashboard")')).toBeVisible();
    await expect(page.locator('text=Test Student')).toBeVisible();
  });

  test('credenciales inválidas', async ({ page }) => {
    await page.goto('/login');
    
    // Fill wrong credentials
    await page.fill('input[name="email"]', 'wrong@example.com');
    await page.fill('input[name="password"]', 'wrongpassword');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Expect to stay on login and see error
    await expect(page).toHaveURL('/login');
    await expect(page.locator('text=Invalid credentials')).toBeVisible();
  });

  test('role-based redirect - Admin', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('input[name="email"]', 'admin@example.com');
    await page.fill('input[name="password"]', 'password123');
    
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL('/dashboard');
    // Admin specific UI checks
    await expect(page.locator('text=Manage Users')).toBeVisible();
    await expect(page.locator('text=System Settings')).toBeVisible();
  });
  
  test('role-based redirect - Teacher', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('input[name="email"]', 'teacher@example.com');
    await page.fill('input[name="password"]', 'password123');
    
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL('/dashboard');
    // Teacher specific UI checks
    await expect(page.locator('text=My Courses')).toBeVisible();
    await expect(page.locator('text=Grade Students')).toBeVisible();
  });

  test('token expiración', async ({ page }) => {
    // 1. Login first
    await page.goto('/login');
    await page.fill('input[name="email"]', 'student@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/dashboard');
    
    // 2. Simulate token expiration via our mock route
    await page.goto('/simulate-expire');
    
    // 3. The dashboard route should detect expiration and redirect to login
    await expect(page).toHaveURL('/login');
    await expect(page.locator('text=Session expired')).toBeVisible();
  });

});
