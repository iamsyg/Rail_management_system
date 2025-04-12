"use client";

import React from "react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";
import { useState, useEffect } from "react";

interface FormData {
    email: string;
    password: string;
  }

export default function WithAuthLayout({ children }: { children: React.ReactNode }) {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);


    const [name, setName] = useState("");
    const [formData, setFormData] = useState<FormData>({
        email: '',
        password: '',
      });
      
        useEffect(() => {
            const checkAuth = async () => {
              try {
                const res = await fetch("http://localhost:8080/auth/profile", {
                  method: "GET",
                  credentials: "include",
                  headers: {
                    "Content-Type": "application/json",
                  }
                });
                if (res.ok) {
                  setIsAuthenticated(true);
                } else {
                  setIsAuthenticated(false);
                }
              } catch (error) {
                console.error("Auth check failed:", error);
                setIsAuthenticated(false);
              }
            };
            checkAuth();
          }, []);
        

    if (isAuthenticated === null) return null; // loading

    if (!isAuthenticated) {
        return <>{children}</>; // no layout for unauthenticated
    }

  return (
    <div>
      <Navbar />

      <div className="sidebar flex">
        <Sidebar />
        <div className="children m-4">{children}</div>
      </div>
    </div>
  );
}

