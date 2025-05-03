"use client";
import React from "react";
import Navbar from "@/app/components/Navbar";
import Sidebar from "@/app/components/Sidebar";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { FiAlertCircle, FiClock, FiCheckCircle, FiTrendingUp, FiTrendingDown } from 'react-icons/fi';

const Dashboard = () => {
  // Sample data for charts
  const complaintStatusData = [
    { name: 'Not Processed', value: 24, color: '#EF4444' },
    { name: 'In Progress', value: 15, color: '#F59E0B' },
    { name: 'Resolved', value: 42, color: '#10B981' },
  ];

  const monthlyTrendData = [
    { month: 'Jan', complaints: 12, resolved: 8 },
    { month: 'Feb', complaints: 19, resolved: 14 },
    { month: 'Mar', complaints: 15, resolved: 11 },
    { month: 'Apr', complaints: 24, resolved: 18 },
    { month: 'May', complaints: 18, resolved: 15 },
    { month: 'Jun', complaints: 22, resolved: 19 },
  ];

  const recentComplaints = [
    { id: '#CMP-1254', type: 'Cleanliness', date: '2023-06-15', status: 'Resolved', priority: 'Low' },
    { id: '#CMP-1253', type: 'Food Quality', date: '2023-06-14', status: 'In Progress', priority: 'Medium' },
    { id: '#CMP-1252', type: 'Staff Behavior', date: '2023-06-13', status: 'Pending', priority: 'High' },
    { id: '#CMP-1251', type: 'Facilities', date: '2023-06-12', status: 'Resolved', priority: 'Low' },
  ];

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
                <p className="text-2xl font-bold mt-1">3</p>
                <p className="text-sm text-gray-500 mt-1">2 more than last month</p>
              </div>
            </div>
            
            {/* In Progress Card */}
            <div className="bg-white rounded-lg shadow p-6 flex items-center gap-4">
              <div className="bg-yellow-100 p-4 rounded-full">
                <FiClock className="w-6 h-6 text-yellow-600" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-700">In Progress</h2>
                <p className="text-2xl font-bold mt-1">2</p>
                <p className="text-sm text-gray-500 mt-1">1 being processed now</p>
              </div>
            </div>
            
            {/* Resolved Card */}
            <div className="bg-white rounded-lg shadow p-6 flex items-center gap-4">
              <div className="bg-green-100 p-4 rounded-full">
                <FiCheckCircle className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-700">Resolved</h2>
                <p className="text-2xl font-bold mt-1">15</p>
                <p className="text-sm text-gray-500 mt-1">92% satisfaction rate</p>
              </div>
            </div>
          </div>

          {/* Charts Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            {/* Complaint Status Pie Chart */}
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

            {/* Monthly Trend Bar Chart */}
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
          </div>

          {/* Recent Complaints Table */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-lg font-semibold mb-4">Recent Complaints</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Complaint ID</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {recentComplaints.map((complaint) => (
                    <tr key={complaint.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{complaint.id}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{complaint.type}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{complaint.date}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          complaint.status === 'Resolved' ? 'bg-green-100 text-green-800' : 
                          complaint.status === 'In Progress' ? 'bg-yellow-100 text-yellow-800' : 
                          'bg-red-100 text-red-800'
                        }`}>
                          {complaint.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{complaint.priority}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button className="text-blue-600 hover:text-blue-900">View Details</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
            <button className="bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg shadow flex items-center justify-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              File New Complaint
            </button>
            <button className="bg-white hover:bg-gray-50 border border-gray-300 text-gray-700 py-3 px-4 rounded-lg shadow flex items-center justify-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              View Complaint History
            </button>
            <button className="bg-white hover:bg-gray-50 border border-gray-300 text-gray-700 py-3 px-4 rounded-lg shadow flex items-center justify-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Contact Support
            </button>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;