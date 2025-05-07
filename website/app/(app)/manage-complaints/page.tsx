"use client";

import React, { useState, useEffect } from "react";
import Navbar from "@/app/components/Navbar";
import Sidebar from "@/app/components/Sidebar";
import { FiSearch, FiCheck, FiClock, FiAlertCircle, FiChevronDown, FiChevronUp } from "react-icons/fi";
import { motion, AnimatePresence } from "framer-motion";

type ComplaintStatus = "pending" | "inProgress" | "Resolved";
type DateRangeFilter = "all" | "7days" | "30days";

interface Complaint {
  id: string;
  pnrNumber: string;
  trainNumber: string;
  coachNumber: string;
  seatNumber: string;
  sourceStation: string;
  destinationStation: string;
  complaint: string;
  classification: string; // Added classification field
  status: ComplaintStatus;
  createdAt: string;
  resolution?: string;
}

interface Filters {
  status: ComplaintStatus | "all";
  dateRange: DateRangeFilter;
  search: string;
  classification: string; // Added classification filter
}

const ManageComplaints: React.FC = () => {
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [filters, setFilters] = useState<Filters>({
    status: "all",
    dateRange: "all",
    search: "",
    classification: "all" // Initialize classification filter
  });
  const [resolutionNotes, setResolutionNotes] = useState<Record<string, string>>({});
  const [uniqueClassifications, setUniqueClassifications] = useState<string[]>([]);

  // Fetch complaints from API
  useEffect(() => {
    const fetchComplaints = async () => {
      try {
        const response = await fetch("http://localhost:8080/complaints/get-all-complaints", {
          method: "GET",
          credentials: "include",
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        setComplaints(data.complaints || []);

        // Extract unique classifications
        const classifications = Array.from(
          new Set(data.complaints.map((c: Complaint) => c.classification))
        ) as string[];
        setUniqueClassifications(classifications);
      } catch (error) {
        console.error("Error fetching complaints:", error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchComplaints();
  }, []);

  const filteredComplaints = complaints.filter(complaint => {
    // Status filter
    if (filters.status !== "all" && complaint.status !== filters.status) return false;
    
    // Date range filter
    if (filters.dateRange !== "all") {
      const diffDays = Math.floor(
        (new Date().getTime() - new Date(complaint.createdAt).getTime()) / (1000 * 60 * 60 * 24)
      );
      if (filters.dateRange === "7days" && diffDays > 7) return false;
      if (filters.dateRange === "30days" && diffDays > 30) return false;
    }
    
    // Search filter
    if (filters.search) {
      const searchTerm = filters.search.toLowerCase();
      return (
        complaint.pnrNumber.toLowerCase().includes(searchTerm) ||
        complaint.trainNumber.toLowerCase().includes(searchTerm) ||
        complaint.sourceStation.toLowerCase().includes(searchTerm) ||
        complaint.destinationStation.toLowerCase().includes(searchTerm) ||
        complaint.complaint.toLowerCase().includes(searchTerm)
      );
    }
    
    // Classification filter
    if (filters.classification !== "all" && complaint.classification !== filters.classification) {
      return false;
    }
    
    return true;
  });

  const updateComplaint = async (id: string, newStatus?: ComplaintStatus) => {
    try {
      const payload: Partial<Complaint> = {};
  
      if (newStatus) {
        payload.status = newStatus;
      }
  
      if (resolutionNotes[id]?.trim()) {
        payload.resolution = resolutionNotes[id].trim();
      }
  
      const response = await fetch(`http://localhost:8080/complaints/update/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
        credentials: "include",
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      setComplaints(prev =>
        prev.map(c =>
          c.id === id ? { ...c, ...payload } : c
        )
      );
  
      if (payload.resolution) {
        setResolutionNotes(prev => ({ ...prev, [id]: "" }));
      }
    } catch (error) {
      console.error("Error updating complaint:", error);
    }
  };

  const toggleExpand = (id: string) => {
    setExpandedId(prev => prev === id ? null : id);
  };

  const StatusBadge: React.FC<{ status: ComplaintStatus }> = ({ status }) => {
    const statusConfig = {
      pending: { color: "bg-red-100 text-red-800", icon: <FiAlertCircle className="mr-1" /> },
      "inProgress": { color: "bg-yellow-100 text-yellow-800", icon: <FiClock className="mr-1" /> },
      Resolved: { color: "bg-green-100 text-green-800", icon: <FiCheck className="mr-1" /> }
    };
    
    return (
      <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ${statusConfig[status].color}`}>
        {statusConfig[status].icon}
        {status}
      </span>
    );
  };

  const ClassificationBadge: React.FC<{ classification: string }> = ({ classification }) => {
    return (
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-800">
        {classification}
      </span>
    );
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="fixed top-0 left-0 right-0 z-50">
        <Navbar panelName="User" />
      </div>

      <div className="flex pt-16">
        <div className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 z-40">
          <Sidebar panelName="User" />
        </div>

        <main className="flex-1 ml-64 p-8 z-10">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800">Manage Complaints</h1>
            
            <div className="flex flex-col sm:flex-row w-full md:w-auto gap-3">
              <div className="relative flex-1">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiSearch className="text-gray-400" />
                </div>
                <input
                  type="text"
                  placeholder="Search complaints..."
                  className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  value={filters.search}
                  onChange={(e) => setFilters(prev => ({...prev, search: e.target.value}))}
                />
              </div>
              
              <div className="flex gap-3">
                <select
                  className="border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  value={filters.status}
                  onChange={(e) => setFilters(prev => ({
                    ...prev, 
                    status: e.target.value as ComplaintStatus | "all"
                  }))}
                >
                  <option value="all">All Statuses</option>
                  <option value="pending">pending</option>
                  <option value="inProgress">inProgress</option>
                  <option value="Resolved">Resolved</option>
                </select>
                
                <select
                  className="border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  value={filters.classification}
                  onChange={(e) => setFilters(prev => ({
                    ...prev, 
                    classification: e.target.value
                  }))}
                >
                  <option value="all">All Classifications</option>
                  {uniqueClassifications.map((classification) => (
                    <option key={classification} value={classification}>
                      {classification}
                    </option>
                  ))}
                </select>
                
                <select
                  className="border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  value={filters.dateRange}
                  onChange={(e) => setFilters(prev => ({
                    ...prev, 
                    dateRange: e.target.value as DateRangeFilter
                  }))}
                >
                  <option value="all">All Time</option>
                  <option value="7days">Last 7 Days</option>
                  <option value="30days">Last 30 Days</option>
                </select>
              </div>
            </div>
          </div>

          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
            </div>
          ) : filteredComplaints.length === 0 ? (
            <div className="bg-white rounded-xl shadow-sm p-8 text-center">
              <p className="text-gray-500 text-lg">No complaints found matching your criteria</p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredComplaints.map((complaint) => (
                <motion.div 
                  key={complaint.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  className="bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden"
                >
                  <div 
                    className="p-6 cursor-pointer flex justify-between items-center"
                    onClick={() => toggleExpand(complaint.id)}
                  >
                    <div>
                      <h3 className="text-lg font-semibold text-gray-800">
                        {complaint.sourceStation} → {complaint.destinationStation}
                      </h3>
                      <div className="flex flex-wrap gap-2 mt-2 items-center">
                        <span className="text-sm text-gray-500">
                          {formatDate(complaint.createdAt)} • 
                          Train: {complaint.trainNumber} • 
                          PNR: {complaint.pnrNumber}
                        </span>
                        <ClassificationBadge classification={complaint.classification} />
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-4">
                      <StatusBadge status={complaint.status} />
                      {expandedId === complaint.id ? (
                        <FiChevronUp className="text-gray-500 transition-transform" />
                      ) : (
                        <FiChevronDown className="text-gray-500 transition-transform" />
                      )}
                    </div>
                  </div>

                  <AnimatePresence>
                    {expandedId === complaint.id && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ 
                          height: "auto",
                          opacity: 1,
                          transition: {
                            height: { duration: 0.3 },
                            opacity: { duration: 0.2, delay: 0.1 }
                          }
                        }}
                        exit={{ 
                          height: 0,
                          opacity: 0,
                          transition: {
                            height: { duration: 0.2 },
                            opacity: { duration: 0.1 }
                          }
                        }}
                        className="overflow-hidden"
                      >
                        <div className="px-6 pb-6 border-t border-gray-100">
                          <div className="grid grid-cols-1 md:grid-cols-12 gap-6 mt-4">
                            <div className="md:col-span-3 space-y-4">
                              <div>
                                <h4 className="text-sm font-medium text-gray-500 mb-2">Journey Details</h4>
                                <div className="space-y-2 text-sm">
                                  <p><span className="font-medium">Coach/Seat:</span> {complaint.coachNumber}/{complaint.seatNumber}</p>
                                  <p><span className="font-medium">Date:</span> {formatDate(complaint.createdAt)}</p>
                                  <p><span className="font-medium">PNR:</span> {complaint.pnrNumber}</p>
                                  <p><span className="font-medium">Classification:</span> {complaint.classification}</p>
                                </div>
                              </div>
                            </div>
                            
                            <div className="md:col-span-5 space-y-4">
                              <div>
                                <h4 className="text-sm font-medium text-gray-500 mb-2">Complaint</h4>
                                <p className="text-gray-700 whitespace-pre-line">{complaint.complaint}</p>
                              </div>
                            </div>
                            
                            <div className="md:col-span-4 space-y-4">
                              <div>
                                <h4 className="text-sm font-medium text-gray-500 mb-2">Actions</h4>
                                <div className="flex flex-wrap gap-2">
                                  <button
                                    onClick={() => updateComplaint(complaint.id, "inProgress")}
                                    disabled={complaint.status === "inProgress"}
                                    className={`px-3 py-1 rounded text-xs font-medium ${
                                      complaint.status === "inProgress" 
                                        ? "bg-gray-100 text-gray-500 cursor-not-allowed" 
                                        : "bg-yellow-100 text-yellow-800 hover:bg-yellow-200"
                                    }`}
                                  >
                                    Mark inProgress
                                  </button>
                                  <button
                                    onClick={() => updateComplaint(complaint.id, "Resolved")}
                                    disabled={complaint.status === "Resolved"}
                                    className={`px-3 py-1 rounded text-xs font-medium ${
                                      complaint.status === "Resolved" 
                                        ? "bg-gray-100 text-gray-500 cursor-not-allowed" 
                                        : "bg-green-100 text-green-800 hover:bg-green-200"
                                    }`}
                                  >
                                    Mark Resolved
                                  </button>
                                </div>
                              </div>
                              
                              {complaint.status === "Resolved" && complaint.resolution ? (
                                <div className="bg-green-50 p-3 rounded-lg">
                                  <h4 className="text-sm font-medium text-green-800 mb-1">Resolution Notes</h4>
                                  <p className="text-green-700 text-sm">{complaint.resolution}</p>
                                </div>
                              ) : (
                                <div className="mt-4">
                                  <h4 className="text-sm font-medium text-gray-500 mb-2">
                                    {complaint.status === "Resolved" ? "Add Additional Notes" : "Add Resolution Notes"}
                                  </h4>
                                  <textarea
                                    className="w-full border rounded-lg p-2 text-sm focus:ring-2 focus:ring-blue-500"
                                    rows={3}
                                    placeholder="Enter resolution details..."
                                    value={resolutionNotes[complaint.id] || ""}
                                    onChange={(e) => setResolutionNotes(prev => ({
                                      ...prev,
                                      [complaint.id]: e.target.value
                                    }))}
                                  />
                                  <button 
                                    className="mt-2 px-3 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium hover:bg-blue-200"
                                    onClick={() => updateComplaint(complaint.id)}
                                  >
                                    Save Notes
                                  </button>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </motion.div>
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default ManageComplaints;