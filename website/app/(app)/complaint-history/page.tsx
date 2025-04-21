"use client";

import React from "react";
import Navbar from "@/app/components/Navbar";
import Sidebar from "@/app/components/Sidebar";

function page() {
  return (
    <div>
      <div className="min-h-screen bg-gray-100">
        <div className="fixed top-0 left-0 right-0 z-50">
          <Navbar panelName="Admin" />+{" "}
        </div>

        <div className="sidebar flex pt-16">
          <div className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 z-40">
            <Sidebar panelName="Admin" />+{" "}
          </div>

          <main className="flex-1 ml-64 p-8 z-10">
            <h1 className="text-2xl font-bold mb-8">Complaint History</h1>
          </main>
        </div>
      </div>
    </div>
  );
}

export default page;
