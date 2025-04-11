"use client";

import React from "react";

import Navbar from "@/app/components/Navbar";
import Sidebar from "@/app/components/Sidebar";

function Home() {
  return (
    <div>
      <div>
        <Navbar />
      </div>
      <div>
        <Sidebar />
      </div>
    </div>
  );
}

export default Home;
