"use client";

import React, { useState } from "react";
import Navbar from "@/app/components/Navbar";
import Sidebar from "@/app/components/Sidebar";
import { FiChevronDown, FiChevronUp, FiSearch, FiFilter } from "react-icons/fi";
import { motion, AnimatePresence } from "framer-motion";

function page() {
  const [expandedId, setExpandedId] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  // Sample complaint data
  const complaints = [
    {
      id: 1,
      trainNumber: "12345",
      pnrNumber: "ABCD1234",
      coach: "B1",
      seatNumber: "12",
      sourceStation: "Delhi",
      destination: "Mumbai",
      complaint: "The seat was completely broken and couldn't recline properly, making the entire journey extremely uncomfortable. The metal frame was protruding and caused damage to my clothing. Additionally, the armrest was loose and kept falling down throughout the trip.",
      status: "Resolved",
      date: "2023-10-15",
      resolution: "Compensation of ₹500 credited to account. Seat repaired for next journey."
    },
    {
      id: 2,
      trainNumber: "67890",
      pnrNumber: "EFGH5678",
      coach: "A2",
      seatNumber: "24",
      sourceStation: "Chennai Central",
      destination: "Bangalore City Junction",
      complaint: "The air conditioning was not working properly throughout the journey. Despite multiple complaints to the attendant, the temperature remained uncomfortably high. The vents were blowing warm air and some were dripping water, creating puddles in the aisle. This made the overnight journey particularly difficult as sleep was impossible in the heat.",
      status: "In Progress",
      date: "2023-10-18",
      assignedTo: "Maintenance Team B"
    },
    {
      id: 3,
      trainNumber: "54321",
      pnrNumber: "IJKL9012",
      coach: "S3",
      seatNumber: "08",
      sourceStation: "Kolkata Howrah",
      destination: "Patna Junction",
      complaint: "The toilet was extremely unclean, with foul odor emanating throughout the coach. The flush was not working, the sink was clogged, and there was no water available. The door lock was broken, compromising privacy. This condition persisted for the entire 12-hour journey despite requests to clean it at multiple stations where we had longer stops. I had to use the toilet at a station instead. This was unacceptable. I expect a full refund for this inconvenience. I will not be using this service again. I will also be reporting this to the railway authorities. This is  bery bad thing i have to this because this is not the first time i have faced this issue.",
      status: "Pending",
      date: "2023-10-20"
    },
  ];

  const toggleExpand = (id: any) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const filteredComplaints = complaints.filter(complaint => {
    const matchesSearch = complaint.pnrNumber.toLowerCase().includes(searchTerm.toLowerCase()) || 
                         complaint.trainNumber.includes(searchTerm) ||
                         complaint.sourceStation.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         complaint.destination.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = statusFilter === "all" || complaint.status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });

  return (
    <div>
      <div className="min-h-screen bg-gray-50">
        <div className="fixed top-0 left-0 right-0 z-50">
          <Navbar panelName="Admin" />
        </div>

        <div className="sidebar flex pt-16">
          <div className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 z-40">
            <Sidebar panelName="Admin" />
          </div>

          <main className="flex-1 ml-64 p-8 z-10">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
              <h1 className="text-2xl md:text-3xl font-bold text-gray-800">Complaint History</h1>
              <div className="flex flex-col sm:flex-row w-full md:w-auto gap-3">
                <div className="relative flex-1">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <FiSearch className="text-gray-400" />
                  </div>
                  <input
                    type="text"
                    placeholder="Search complaints..."
                    className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
                <select
                  className="border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <option value="all">All Statuses</option>
                  <option value="Resolved">Resolved</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Pending">Pending</option>
                </select>
              </div>
            </div>
            
            {filteredComplaints.length === 0 ? (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="bg-white rounded-xl shadow-sm p-8 text-center"
              >
                <p className="text-gray-500 text-lg">No complaints found matching your criteria</p>
              </motion.div>
            ) : (
              <div className="space-y-4">
                {filteredComplaints.map((item) => (
                  <motion.div 
                    key={item.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                    className={`bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden border-l-4 ${
                      item.status === "Resolved" ? "border-green-500" :
                      item.status === "In Progress" ? "border-yellow-500" :
                      "border-red-500"
                    }`}
                  >
                    <motion.div 
                      className="p-6 cursor-pointer"
                      onClick={() => toggleExpand(item.id)}
                      whileTap={{ scale: 0.98 }}
                    >
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="text-lg font-semibold text-gray-800">
                            {item.sourceStation} → {item.destination}
                          </h3>
                          <p className="text-sm text-gray-500 mt-1">
                            {item.date} • Train: {item.trainNumber} • PNR: {item.pnrNumber}
                          </p>
                        </div>
                        <div className="flex items-center space-x-4">
                          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            item.status === "Resolved" ? "bg-green-100 text-green-800" : 
                            item.status === "In Progress" ? "bg-yellow-100 text-yellow-800" : 
                            "bg-red-100 text-red-800"
                          }`}>
                            {item.status}
                          </span>
                          {expandedId === item.id ? (
                            <FiChevronUp className="text-gray-500 transition-transform duration-300" />
                          ) : (
                            <FiChevronDown className="text-gray-500 transition-transform duration-300" />
                          )}
                        </div>
                      </div>
                    </motion.div>

                    <AnimatePresence>
                      {expandedId === item.id && (
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
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-4">
                              <div className="space-y-3">
                                <div>
                                  <h4 className="text-sm font-medium text-gray-500">Journey Details</h4>
                                  <p className="mt-1 text-gray-700">
                                    <span className="font-medium">Coach/Seat:</span> {item.coach}/{item.seatNumber}<br />
                                    <span className="font-medium">Date:</span> {item.date}<br />
                                    <span className="font-medium">PNR:</span> {item.pnrNumber}
                                  </p>
                                </div>
                              </div>
                              
                              <div className="space-y-3">
                                <div>
                                  <h4 className="text-sm font-medium text-gray-500">Complaint</h4>
                                  <p className="mt-1 text-gray-700 whitespace-pre-line">
                                    {item.complaint}
                                  </p>
                                </div>
                              </div>
                              
                              <div className="space-y-3">
                                {item.status === "Resolved" && item.resolution && (
                                  <motion.div 
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ delay: 0.2 }}
                                    className="bg-green-50 p-3 rounded-lg"
                                  >
                                    <h4 className="text-sm font-medium text-green-800">Resolution</h4>
                                    <p className="mt-1 text-green-700">{item.resolution}</p>
                                  </motion.div>
                                )}
                                {item.status === "In Progress" && item.assignedTo && (
                                  <motion.div 
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ delay: 0.2 }}
                                    className="bg-yellow-50 p-3 rounded-lg"
                                  >
                                    <h4 className="text-sm font-medium text-yellow-800">Assigned To</h4>
                                    <p className="mt-1 text-yellow-700">{item.assignedTo}</p>
                                  </motion.div>
                                )}
                                {item.status === "Pending" && (
                                  <motion.div 
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ delay: 0.2 }}
                                    className="bg-red-50 p-3 rounded-lg"
                                  >
                                    <h4 className="text-sm font-medium text-red-800">Action Required</h4>
                                    <p className="mt-1 text-red-700">Awaiting assignment to team</p>
                                  </motion.div>
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
    </div>
  );
}

export default page;