"use client";
import React, { useState, useEffect } from "react";
import Navbar from "@/app/components/Navbar";
import Sidebar from "@/app/components/Sidebar";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { FiAlertCircle, FiClock, FiCheckCircle } from 'react-icons/fi';

interface Complaint {
  id: string;
  classification: string;
  date: string;
  status: 'Pending' | 'In Progress' | 'Resolved';
  priority: string;
}

const Dashboard = () => {
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch complaints from API
  useEffect(() => {
    const fetchComplaints = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/complaints/get-complaints`, {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setComplaints(data.complaints || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch complaints');
        console.error('Error fetching complaints:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchComplaints();
  }, []);

  // Calculate statistics
  const pendingCount = complaints.filter(c => c.status === 'Pending').length;
  const inProgressCount = complaints.filter(c => c.status === 'In Progress').length;
  const resolvedCount = complaints.filter(c => c.status === 'Resolved').length;

  // Prepare chart data
  const complaintStatusData = [
    { name: 'Pending', value: pendingCount, color: '#EF4444' },
    { name: 'In Progress', value: inProgressCount, color: '#F59E0B' },
    { name: 'Resolved', value: resolvedCount, color: '#10B981' },
  ];

  // Group by month
  const monthlyTrendData = complaints.reduce((acc, complaint) => {
    const date = new Date(complaint.date);
    const month = date.toLocaleString('default', { month: 'short' });
    const existingMonth = acc.find(item => item.month === month);
    
    if (existingMonth) {
      existingMonth.complaints++;
      if (complaint.status === 'Resolved') existingMonth.resolved++;
    } else {
      acc.push({
        month,
        complaints: 1,
        resolved: complaint.status === 'Resolved' ? 1 : 0
      });
    }
    return acc;
  }, [] as { month: string; complaints: number; resolved: number }[]).slice(-6);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-red-600">Error Loading Data</h2>
          <p className="text-gray-700 mt-2">{error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Fixed Navbar */}
      <div className="fixed top-0 left-0 right-0 z-50">
        <Navbar panelName="Admin" />
      </div>

      <div className="flex pt-16">
        {/* Fixed Sidebar */}
        <div className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 z-40">
          <Sidebar panelName="Admin" />
        </div>

        {/* Main content */}
        <main className="flex-1 ml-64 p-8 z-10">
          <h1 className="text-2xl font-bold mb-8">User Dashboard</h1>
          
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {/* Pending Complaints Card */}
            <div className="bg-white rounded-lg shadow p-6 flex items-center gap-4">
              <div className="bg-red-100 p-4 rounded-full">
                <FiAlertCircle className="w-6 h-6 text-red-600" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-700">Pending Complaints</h2>
                <p className="text-2xl font-bold mt-1">{pendingCount}</p>
              </div>
            </div>
            
            {/* In Progress Card */}
            <div className="bg-white rounded-lg shadow p-6 flex items-center gap-4">
              <div className="bg-yellow-100 p-4 rounded-full">
                <FiClock className="w-6 h-6 text-yellow-600" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-700">In Progress</h2>
                <p className="text-2xl font-bold mt-1">{inProgressCount}</p>
              </div>
            </div>
            
            {/* Resolved Card */}
            <div className="bg-white rounded-lg shadow p-6 flex items-center gap-4">
              <div className="bg-green-100 p-4 rounded-full">
                <FiCheckCircle className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-700">Resolved</h2>
                <p className="text-2xl font-bold mt-1">{resolvedCount}</p>
              </div>
            </div>
          </div>

          {/* Charts Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            {/* Complaint Status Pie Chart */}
            {complaints.length > 0 && (
              <div className="bg-white p-6 rounded-lg shadow">
                <h2 className="text-lg font-semibold mb-4">Your Complaint Status</h2>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={complaintStatusData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      >
                        {complaintStatusData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {/* Monthly Trend Bar Chart */}
            {monthlyTrendData.length > 0 && (
              <div className="bg-white p-6 rounded-lg shadow">
                <h2 className="text-lg font-semibold mb-4">Monthly Complaint Trend</h2>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={monthlyTrendData}
                      margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                      }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="complaints" fill="#8884d8" name="Your Complaints" />
                      <Bar dataKey="resolved" fill="#82ca9d" name="Resolved" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}
          </div>

          {/* Recent Complaints Table */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-lg font-semibold mb-4">Recent Complaints</h2>
            {complaints.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Complaint ID</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Classification</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {complaints.slice(0, 5).map((complaint) => (
                      <tr key={complaint.id}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#{complaint.id.slice(0, 8)}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{complaint.classification}</td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            complaint.status === 'Resolved' ? 'bg-green-100 text-green-800' : 
                            complaint.status === 'In Progress' ? 'bg-yellow-100 text-yellow-800' : 
                            'bg-red-100 text-red-800'
                          }`}>
                            {complaint.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <button className="text-blue-600 hover:text-blue-900">View Details</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-500">No complaints found</p>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;