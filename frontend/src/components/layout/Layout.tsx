import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
import { Calendar, Home, LogIn, LogOut, User, LayoutDashboard } from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuthStore();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <Link to="/" className="flex items-center">
                <Calendar className="h-8 w-8 text-primary-600" />
                <span className="ml-2 text-xl font-semibold">EventHub</span>
              </Link>
              
              <div className="ml-10 flex items-center space-x-4">
                <Link
                  to="/"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    isActive('/') 
                      ? 'bg-primary-100 text-primary-700' 
                      : 'text-gray-700 hover:text-gray-900'
                  }`}
                >
                  <Home className="h-4 w-4 inline mr-1" />
                  Home
                </Link>
                
                <Link
                  to="/events"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    isActive('/events') 
                      ? 'bg-primary-100 text-primary-700' 
                      : 'text-gray-700 hover:text-gray-900'
                  }`}
                >
                  <Calendar className="h-4 w-4 inline mr-1" />
                  Events
                </Link>
                
                {user?.role === 'admin' && (
                  <Link
                    to="/admin"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                      location.pathname.startsWith('/admin') 
                        ? 'bg-primary-100 text-primary-700' 
                        : 'text-gray-700 hover:text-gray-900'
                    }`}
                  >
                    <LayoutDashboard className="h-4 w-4 inline mr-1" />
                    Admin
                  </Link>
                )}
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {user ? (
                <>
                  <Link
                    to="/profile"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                      isActive('/profile') 
                        ? 'bg-primary-100 text-primary-700' 
                        : 'text-gray-700 hover:text-gray-900'
                    }`}
                  >
                    <User className="h-4 w-4 inline mr-1" />
                    {user.username}
                  </Link>
                  
                  <button
                    onClick={logout}
                    className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900"
                  >
                    <LogOut className="h-4 w-4 inline mr-1" />
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                      isActive('/login') 
                        ? 'bg-primary-100 text-primary-700' 
                        : 'text-gray-700 hover:text-gray-900'
                    }`}
                  >
                    <LogIn className="h-4 w-4 inline mr-1" />
                    Login
                  </Link>
                  
                  <Link
                    to="/register"
                    className="px-4 py-2 rounded-md text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
      
      <footer className="bg-white mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-sm text-gray-500">
            © 2024 EventHub. Built by Claude Sonnet 4.
          </p>
        </div>
      </footer>
    </div>
  );
};