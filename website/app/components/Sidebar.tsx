"use client";
import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { FiHome, FiSettings, FiAlertTriangle, FiList, FiUsers, FiBarChart2, FiLogOut } from "react-icons/fi";

interface SidebarProps {
  panelName: "User" | "Admin";
}

const Sidebar = ({ panelName }: SidebarProps) => {
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(true);
  const pathname = usePathname();

  useEffect(() => {
    // Simulate fetching user data
    const fetchUser = async () => {
      try {
        // Replace with actual API call
        await new Promise(resolve => setTimeout(resolve, 500));
        setName("Swayam Gupta");
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, []);

  const isActive = (path: string) => pathname === path;

  const userLinks = [
    { href: "/dashboard", label: "Dashboard", icon: <FiHome /> },
    { href: "/account-settings", label: "Account Settings", icon: <FiSettings /> },
    { href: "/complaints", label: "File Complaint", icon: <FiAlertTriangle /> },
    { href: "/complaint-history", label: "Complaint History", icon: <FiList /> },
  ];

  const adminLinks = [
    { href: "/admin-dashboard", label: "Dashboard", icon: <FiHome /> },
    { href: "/admin/complaints", label: "Manage Complaints", icon: <FiAlertTriangle /> },
    { href: "/admin/users", label: "User Management", icon: <FiUsers /> },
    { href: "/admin/reports", label: "Reports", icon: <FiBarChart2 /> },
  ];

  const links = panelName === "Admin" ? userLinks : adminLinks;

  return (
    <div className="hidden md:flex flex-col w-64 min-h-screen bg-gray-800 text-white fixed left-0 overflow-y-auto">
      {/* Sidebar Header */}
      <div className="p-4 border-b border-gray-700">
        
        {loading ? (
          <div className="animate-pulse h-6 w-3/4 bg-gray-600 mt-2 rounded"></div>
        ) : (
          <h1 className="text-xl text-gray-300 mt-1">Welcome, {name}</h1>
        )}
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 overflow-y-auto p-2">
        <ul className="space-y-1">
          {links.map((link) => (
            <li key={link.href}>
              <Link
                href={link.href}
                className={`flex items-center p-3 rounded-lg transition-colors ${
                  isActive(link.href)
                    ? "bg-blue-600 text-white"
                    : "hover:bg-gray-700 text-gray-300"
                }`}
              >
                <span className="mr-3">{link.icon}</span>
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;