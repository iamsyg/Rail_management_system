"use client";
import React from 'react';
import Navbar from '@/app/components/Navbar';
import Sidebar from '@/app/components/Sidebar';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

const emergencyData = [
  { id: 1, type: 'Train Breakdown', location: 'Mumbai Central', time: '2 mins ago', priority: 'High' },
  { id: 2, type: 'Medical Emergency', location: 'Delhi Junction', time: '15 mins ago', priority: 'Medium' },
  { id: 3, type: 'Track Obstruction', location: 'Chennai Central', time: '25 mins ago', priority: 'High' },
];

const problemCategoryData = [
  { name: 'Facilities', value: 35 },
  { name: 'Cleanliness', value: 25 },
  { name: 'Staff Behavior', value: 20 },
  { name: 'Food Quality', value: 15 },
  { name: 'Other', value: 5 },
];

const monthlyTrendData = [
  { month: 'Jan', complaints: 40, resolved: 32 },
  { month: 'Feb', complaints: 30, resolved: 28 },
  { month: 'Mar', complaints: 45, resolved: 38 },
  { month: 'Apr', complaints: 50, resolved: 42 },
  { month: 'May', complaints: 35, resolved: 30 },
  { month: 'Jun', complaints: 55, resolved: 48 },
];

const AdminDashboard = () => {
  return (
    <>
    <div className="min-h-screen bg-gray-100">
      {/* Fixed Navbar with highest z-index */}
      <div className="fixed top-0 left-0 right-0 z-50">
        <Navbar panelName='User' />
      </div>

      <div className="flex pt-16"> {/* Add padding-top to account for navbar */}
        {/* Fixed Sidebar */}
        <div className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 bg-gray-800 z-40">
          <Sidebar panelName='User' />
        </div>

        {/* Main content with proper margins */}
        <main className="flex-1 ml-64 p-6 z-10"> {/* Add left margin for sidebar */}
          <h1 className="text-2xl font-bold mb-6">Admin Dashboard</h1>
          
          {/* Emergency Alerts Section */}

          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-4">Emergency Alerts</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {emergencyData.map((alert) => (
                <div 
                  key={alert.id} 
                  className={`p-4 rounded-lg shadow-md ${
                    alert.priority === 'High' ? 'bg-red-50 border-l-4 border-red-500' : 
                    alert.priority === 'Medium' ? 'bg-yellow-50 border-l-4 border-yellow-500' : 
                    'bg-blue-50 border-l-4 border-blue-500'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-bold text-lg">{alert.type}</h3>
                      <p className="text-gray-600">{alert.location}</p>
                    </div>
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      alert.priority === 'High' ? 'bg-red-100 text-red-800' : 
                      alert.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' : 
                      'bg-blue-100 text-blue-800'
                    }`}>
                      {alert.priority}
                    </span>
                  </div>
                  <p className="text-sm text-gray-500 mt-2">{alert.time}</p>
                  <button className="mt-3 text-sm text-blue-600 hover:text-blue-800 font-medium">
                    View Details →
                  </button>
                </div>
              ))}
            </div>
          
          </div>

          {/* Statistics Overview */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-gray-500 text-sm font-medium">Total Complaints</h3>
              <p className="text-2xl font-bold mt-1">1,245</p>
              <p className="text-green-500 text-sm mt-1">↑ 12% from last month</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-gray-500 text-sm font-medium">Pending Resolution</h3>
              <p className="text-2xl font-bold mt-1">187</p>
              <p className="text-red-500 text-sm mt-1">↑ 5% from last week</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-gray-500 text-sm font-medium">Avg. Resolution Time</h3>
              <p className="text-2xl font-bold mt-1">2.4 days</p>
              <p className="text-green-500 text-sm mt-1">↓ 0.8 days from last month</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-gray-500 text-sm font-medium">Satisfaction Rate</h3>
              <p className="text-2xl font-bold mt-1">82%</p>
              <p className="text-green-500 text-sm mt-1">↑ 7% from last quarter</p>
            </div>
          </div>

          {/* Problem Categories Visualization */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <div className="bg-white p-4 rounded-lg shadow">
              <h2 className="text-lg font-semibold mb-4">Complaint Categories</h2>
              <div className="h-80">

                <ResponsiveContainer>
                <PieChart>
                    <Pie
                      data={problemCategoryData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    >
                      {problemCategoryData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                </PieChart>
                </ResponsiveContainer>
        
              </div>
            </div>

            <div className="bg-white p-4 rounded-lg shadow">
              <h2 className="text-lg font-semibold mb-4">Monthly Trends</h2>
              <div className="h-80">
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
                    <Bar dataKey="complaints" fill="#8884d8" name="Complaints" />
                    <Bar dataKey="resolved" fill="#82ca9d" name="Resolved" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Recent Complaints */}
          <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Recent Complaints</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Train No.</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {[1, 2, 3, 4, 5].map((item) => (
                    <tr key={item}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{12340 + item}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {['Facility Issue', 'Cleanliness', 'Staff Behavior', 'Food Quality', 'Other'][item % 5]}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">1234{item}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          item % 3 === 0 ? 'bg-green-100 text-green-800' : 
                          item % 3 === 1 ? 'bg-yellow-100 text-yellow-800' : 
                          'bg-red-100 text-red-800'
                        }`}>
                          {item % 3 === 0 ? 'Resolved' : item % 3 === 1 ? 'In Progress' : 'Pending'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(Date.now() - item * 86400000).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <a href="#" className="text-blue-600 hover:text-blue-900">View</a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </main>
      </div>
    </div>
    </>
  );
};

export default AdminDashboard;