"use client";
import React from "react";
import Navbar from "@/app/components/Navbar";
import Sidebar from "@/app/components/Sidebar";

function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Fixed Navbar with highest z-index */}
      <div className="fixed top-0 left-0 right-0 z-50">
        <Navbar panelName="Admin" />
      </div>

      <div className="flex pt-16"> {/* Add padding-top to account for navbar */}
        {/* Fixed Sidebar */}
        <div className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 z-40">
          <Sidebar panelName="Admin"/>
        </div>

        {/* Main content with proper margins */}
        <main className="flex-1 ml-64 p-8 z-10"> {/* Add left margin for sidebar */}
          <h1 className="text-2xl font-bold mb-8">Dashboard</h1>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Not Processed Card */}
            <div className="bg-white rounded-lg shadow p-6 flex items-center gap-4">
              <div className="bg-red-100 p-4 rounded-full">
                <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-700">Complaints not processed</h2>
                <p className="text-2xl font-bold mt-1">24</p>
              </div>
            </div>
            
            {/* In Process Card */}
            <div className="bg-white rounded-lg shadow p-6 flex items-center gap-4">
              <div className="bg-yellow-100 p-4 rounded-full">
                <svg className="w-8 h-8 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-700">Status in process</h2>
                <p className="text-2xl font-bold mt-1">15</p>
              </div>
            </div>
            
            {/* Closed Card */}
            <div className="bg-white rounded-lg shadow p-6 flex items-center gap-4">
              <div className="bg-green-100 p-4 rounded-full">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <h2 className="text-lg font-semibold text-gray-700">Complaints closed</h2>
                <p className="text-2xl font-bold mt-1">42</p>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default Dashboard;