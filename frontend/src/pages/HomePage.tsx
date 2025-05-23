import React from 'react';
import { Link } from 'react-router-dom';
import { Calendar, Users, TrendingUp, ArrowRight } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/services/api';

export const HomePage: React.FC = () => {
  const { data: events } = useQuery({
    queryKey: ['upcoming-events'],
    queryFn: () => api.getEvents({ limit: 6, status: 'published' }),
  });

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-12">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Welcome to EventHub
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Discover and manage amazing events in your area
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            to="/events"
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition"
          >
            Browse Events
          </Link>
          <Link
            to="/register"
            className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
          >
            Create Account
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="grid md:grid-cols-3 gap-8">
        <div className="text-center p-6">
          <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Calendar className="h-8 w-8 text-primary-600" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Easy Event Management</h3>
          <p className="text-gray-600">
            Create, manage, and promote your events with our intuitive platform
          </p>
        </div>
        
        <div className="text-center p-6">
          <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Users className="h-8 w-8 text-primary-600" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Attendee Tracking</h3>
          <p className="text-gray-600">
            Keep track of registrations and check-ins in real-time
          </p>
        </div>
        
        <div className="text-center p-6">
          <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <TrendingUp className="h-8 w-8 text-primary-600" />
          </div>
          <h3 className="text-lg font-semibold mb-2">Analytics & Insights</h3>
          <p className="text-gray-600">
            Get detailed analytics to understand your event performance
          </p>
        </div>
      </section>

      {/* Upcoming Events */}
      {events?.events && events.events.length > 0 && (
        <section>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-3xl font-bold text-gray-900">Upcoming Events</h2>
            <Link
              to="/events"
              className="text-primary-600 hover:text-primary-700 flex items-center gap-1"
            >
              View all <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
          
          <div className="grid md:grid-cols-3 gap-6">
            {events.events.map((event: any) => (
              <Link
                key={event.id}
                to={`/events/${event.id}`}
                className="bg-white rounded-lg shadow-sm hover:shadow-md transition p-6"
              >
                <h3 className="text-lg font-semibold mb-2">{event.title}</h3>
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                  {event.description}
                </p>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-500">
                    {new Date(event.start_date).toLocaleDateString()}
                  </span>
                  <span className="text-primary-600 font-medium">
                    {event.price === 0 ? 'Free' : `$${event.price}`}
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}
    </div>
  );
};