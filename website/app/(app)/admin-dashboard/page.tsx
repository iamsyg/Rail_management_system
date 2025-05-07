"use client";
import React, { useState, useEffect } from 'react';
import Navbar from '@/app/components/Navbar';
import Sidebar from '@/app/components/Sidebar';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#FF6B6B', '#4ECDC4'];

interface Complaint {
  id: string;
  pnrNumber: string;
  trainNumber: string;
  coachNumber: string;
  seatNumber: string;
  sourceStation: string;
  destinationStation: string;
  complaint: string;
  classification: string;
  sentimentScore: number; // 0 to 1 decimal value
  sentiment: 'POSITIVE' | 'NEGATIVE';
  status: 'pending' | 'inProgress' | 'resolved';
  createdAt: string;
  resolution?: string;
}

const AdminDashboard = () => {
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [loading, setLoading] = useState(true);
  const [emergencyData, setEmergencyData] = useState<any[]>([]);
  const [stats, setStats] = useState({
    total: 0,
    pending: 0,
    satisfactionRate: '0%',
    avgSentiment: 0
  });

  // Emergency classifications
  const emergencyClassifications = ['Medical'];

  // Fetch complaints from API
  useEffect(() => {
    const fetchComplaints = async () => {
      try {
        const response = await fetch('http://localhost:8080/complaints/get-all-complaints', {
          method: 'GET',
          credentials: 'include',
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        const fetchedComplaints = data.complaints || [];
        setComplaints(fetchedComplaints);
        
        // Generate emergency alerts
        const emergencies = fetchedComplaints
          .filter((c: Complaint) => 
            emergencyClassifications.some(ec => c.classification.includes(ec)) ||
            c.sentimentScore > 0.95
          )
          .slice(0, 3)
          .map((c: Complaint) => ({
            id: c.id,
            classification: c.classification,
            location: `${c.sourceStation} to ${c.destinationStation}`,
            time: formatTimeAgo(c.createdAt),
            priority: c.sentimentScore > 0.99 ? 'Critical' : 'High',
            sentimentScore: c.sentimentScore,
            complaintId: c.id
          }));
        setEmergencyData(emergencies);
        
        // Calculate statistics
        const total = fetchedComplaints.length;
        const pending = fetchedComplaints.filter((c: Complaint) => c.status !== 'resolved').length;
        const resolved = fetchedComplaints.filter((c: Complaint) => c.status === 'resolved').length;
        const totalSentiment = fetchedComplaints.reduce((sum: number, c: Complaint) => sum + c.sentimentScore, 0);
        
        setStats({
          total,
          pending,
          satisfactionRate: `${total > 0 ? Math.round((resolved / total) * 100) : 0}%`,
          avgSentiment: total > 0 ? parseFloat((totalSentiment / total).toFixed(2)) : 0
        });
        
      } catch (error) {
        console.error('Error fetching complaints:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchComplaints();
  }, []);

  const formatTimeAgo = (dateString: string) => {
    const now = new Date();
    const date = new Date(dateString);
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 60) return `${diffInMinutes} mins ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)} hours ago`;
    return `${Math.floor(diffInMinutes / 1440)} days ago`;
  };

  // Generate problem classification data
  const problemClassificationData = complaints.reduce((acc: {name: string, value: number}[], complaint) => {
    const existingType = acc.find(item => item.name === complaint.classification);
    if (existingType) {
      existingType.value++;
    } else {
      acc.push({ name: complaint.classification, value: 1 });
    }
    return acc;
  }, []).sort((a, b) => b.value - a.value).slice(0, 6);

  // Generate monthly trend data
  const generateMonthlyTrendData = () => {
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const monthlyData: Record<string, { complaints: number; resolved: number }> = {};
    
    complaints.forEach(c => {
      const date = new Date(c.createdAt);
      const monthYear = `${monthNames[date.getMonth()]} ${date.getFullYear()}`;
      
      if (!monthlyData[monthYear]) {
        monthlyData[monthYear] = { complaints: 0, resolved: 0 };
      }
      
      monthlyData[monthYear].complaints++;
      if (c.status === 'resolved') {
        monthlyData[monthYear].resolved++;
      }
    });
    
    return Object.entries(monthlyData)
      .sort((a, b) => {
        const [aMonth, aYear] = a[0].split(' ');
        const [bMonth, bYear] = b[0].split(' ');
        const aIndex = monthNames.indexOf(aMonth) + parseInt(aYear) * 12;
        const bIndex = monthNames.indexOf(bMonth) + parseInt(bYear) * 12;
        return aIndex - bIndex;
      })
      .slice(-6)
      .map(([month, data]) => ({
        month,
        complaints: data.complaints,
        resolved: data.resolved
      }));
  };

  const monthlyTrendData = generateMonthlyTrendData();

  // Sentiment gauge component
  const SentimentGauge = ({ score }: { score: number }) => {
    const percentage = Math.round(score * 100);
    let color = '#FF6B6B';
    let label = 'Negative';
    
    if (percentage > 70) {
      color = '#00C49F';
      label = 'Positive';
    } else if (percentage > 40) {
      color = '#FFBB28';
      label = 'Neutral';
    }
    
    return (
      <div className="flex items-center gap-2">
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div 
            className="h-2.5 rounded-full" 
            style={{ 
              width: `${percentage}%`,
              backgroundColor: color
            }}
          ></div>
        </div>
        <span className="text-xs font-medium" style={{ color }}>
          {label} ({percentage}%)
        </span>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="fixed top-0 left-0 right-0 z-50">
        <Navbar panelName='User' />
      </div>

      <div className="flex pt-16">
        <div className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 bg-gray-800 z-40">
          <Sidebar panelName='User' />
        </div>

        <main className="flex-1 ml-64 p-6 z-10">
          <h1 className="text-2xl font-bold mb-6">Admin Dashboard</h1>
          
          {/* Emergency Alerts Section */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-4">Emergency Alerts</h2>
            {emergencyData.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {emergencyData.map((alert) => (
                  <div 
                    key={alert.id} 
                    className={`p-4 rounded-lg shadow-md border-l-4 ${
                      alert.priority === 'Critical' ? 'bg-red-50 border-red-500' : 'bg-yellow-50 border-yellow-500'
                    }`}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-bold text-lg">{alert.classification}</h3>
                        <p className="text-gray-600">{alert.location}</p>
                      </div>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        alert.priority === 'Critical' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {alert.priority}
                      </span>
                    </div>
                    <div className="mt-2">
                      <SentimentGauge score={alert.sentimentScore} />
                    </div>
                    <p className="text-sm text-gray-500 mt-2">{alert.time}</p>
                    <button className="mt-3 text-sm text-blue-600 hover:text-blue-800 font-medium">
                      View Details →
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                <p className="text-green-800">No emergency alerts currently</p>
              </div>
            )}
          </div>

          {/* Statistics Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-gray-500 text-sm font-medium">Total Complaints</h3>
              <p className="text-2xl font-bold mt-1">{stats.total}</p>
              <p className="text-green-500 text-sm mt-1">↑ 12% from last month</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-gray-500 text-sm font-medium">Pending Resolution</h3>
              <p className="text-2xl font-bold mt-1">{stats.pending}</p>
              <p className="text-red-500 text-sm mt-1">↑ 5% from last week</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-gray-500 text-sm font-medium">Satisfaction Rate</h3>
              <p className="text-2xl font-bold mt-1">{stats.satisfactionRate}</p>
              <p className="text-green-500 text-sm mt-1">↑ 7% from last quarter</p>
            </div>
          </div>

          {/* Sentiment Overview */}
          <div className="bg-white p-4 rounded-lg shadow mb-8">
            <h2 className="text-lg font-semibold mb-4">Overall Sentiment</h2>
            <div className="flex items-center justify-between">
              <div className="w-3/4">
                <SentimentGauge score={stats.avgSentiment} />
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold">{stats.avgSentiment.toFixed(2)}</p>
                <p className="text-sm text-gray-500">Average Score</p>
              </div>
            </div>
          </div>

          {/* Problem Classifications and Trends */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <div className="bg-white p-4 rounded-lg shadow">
              <h2 className="text-lg font-semibold mb-4">Complaint Classifications</h2>
              <div className="h-80">
                <ResponsiveContainer>
                  <PieChart>
                    <Pie
                      data={problemClassificationData.filter(d => d.value > 0)}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    >
                      {problemClassificationData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
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
                    <Bar dataKey="resolved" fill="#82ca9d" name="resolved" />
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
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Classification</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sentiment</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {complaints.slice(0, 5).map((complaint) => (
                    <tr key={complaint.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{complaint.id.slice(0, 8)}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {complaint.classification}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="w-48">
                          <SentimentGauge score={complaint.sentimentScore} />
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          complaint.status === 'resolved' ? 'bg-green-100 text-green-800' : 
                          complaint.status === 'inProgress' ? 'bg-yellow-100 text-yellow-800' : 
                          'bg-red-100 text-red-800'
                        }`}>
                          {complaint.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(complaint.createdAt).toLocaleDateString()}
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
  );
};

export default AdminDashboard;