"use client";

import React from "react";
import Navbar from "@/app/components/Navbar";
import Sidebar from "@/app/components/Sidebar";

function page() {
  return (
    <div>
      <div>
        <Navbar />

        <div className="sidebar flex">
          <Sidebar />

          <div className="content m-4">
            <h1>Dashboard</h1>
          </div>
        </div>
      </div>
    </div>
  );
}

export default page;
