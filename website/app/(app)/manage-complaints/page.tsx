// "use client";

// import React, { useState, useEffect } from "react";
// import Navbar from "@/app/components/Navbar";
// import Sidebar from "@/app/components/Sidebar";
// import { FiSearch, FiEdit, FiCheck, FiX, FiClock, FiAlertCircle, FiChevronDown, FiChevronUp } from "react-icons/fi";
// import { motion, AnimatePresence } from "framer-motion";

// // Type definitions
// type ComplaintStatus = "Pending" | "In Progress" | "Resolved";
// type DateRangeFilter = "all" | "7days" | "30days";

// interface Complaint {
//   _id: string;
//   pnrNumber: string;
//   trainNumber: string;
//   coachNumber: string;
//   seatNumber: string;
//   sourceStation: string;
//   destinationStation: string;
//   complaint: string;
//   status: ComplaintStatus;
//   createdAt: string;
//   resolutionNotes?: string;
//   assignedTo?: string;
// }

// interface Filters {
//   status: ComplaintStatus | "all";
//   dateRange: DateRangeFilter;
//   search: string;
// }

// const ManageComplaints: React.FC = () => {
//   const [complaints, setComplaints] = useState<Complaint[]>([]);
//   const [loading, setLoading] = useState<boolean>(true);
//   const [expandedId, setExpandedId] = useState<string | null>(null);
//   const [filters, setFilters] = useState<Filters>({
//     status: "all",
//     dateRange: "all",
//     search: ""
//   });
//   const [resolutionNotes, setResolutionNotes] = useState<{ [key: string]: string }>({});

//   // Fetch complaints from API
//   useEffect(() => {
//     const fetchComplaints = async () => {
//       try {
//         const response = await fetch("http://localhost:8080/complaints/get-complaints", {
//           method: "GET",
//           credentials: "include",
//         });
//         const data = await response.json();
//         setComplaints(data.complaints);
//       } catch (error) {
//         console.error("Error fetching complaints:", error);
//       } finally {
//         setLoading(false);
//       }
//     };
//     fetchComplaints();
//   }, []);

//   // Filter complaints based on filters
//   const filteredComplaints = complaints.filter(complaint => {
//     // Status filter
//     if (filters.status !== "all" && complaint.status !== filters.status) {
//       return false;
//     }
    
//     // Date range filter
//     if (filters.dateRange !== "all") {
//       const complaintDate = new Date(complaint.createdAt);
//       const now = new Date();
//       const diffDays = Math.floor((now.getTime() - complaintDate.getTime()) / (1000 * 60 * 60 * 24));
      
//       if (filters.dateRange === "7days" && diffDays > 7) return false;
//       if (filters.dateRange === "30days" && diffDays > 30) return false;
//     }
    
//     // Search filter
//     if (filters.search) {
//       const searchTerm = filters.search.toLowerCase();
//       return (
//         complaint.pnrNumber.toLowerCase().includes(searchTerm) ||
//         complaint.trainNumber.toLowerCase().includes(searchTerm) ||
//         complaint.sourceStation.toLowerCase().includes(searchTerm) ||
//         complaint.destinationStation.toLowerCase().includes(searchTerm) ||
//         complaint.complaint.toLowerCase().includes(searchTerm)
//       );
//     }
    
//     return true;
//   });

//   // Handle status update
//   const updateStatus = async (id: string, newStatus: ComplaintStatus) => {
//     try {
//       const response = await fetch(`http://localhost:8080/complaints/update-status/${id}`, {
//         method: "PUT",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ status: newStatus }),
//         credentials: "include",
//       });
      
//       if (response.ok) {
//         setComplaints(complaints.map(c => 
//           c._id === id ? { ...c, status: newStatus } : c
//         ));
//       }
//     } catch (error) {
//       console.error("Error updating status:", error);
//     }
//   };

//   // Save resolution notes
//   const saveResolutionNotes = async (id: string) => {
//     try {
//       const response = await fetch(`http://localhost:8080/complaints/add-resolution/${id}`, {
//         method: "PUT",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ resolutionNotes: resolutionNotes[id] }),
//         credentials: "include",
//       });
      
//       if (response.ok) {
//         setComplaints(complaints.map(c => 
//           c._id === id ? { ...c, resolutionNotes: resolutionNotes[id] } : c
//         ));
//         // Clear the notes input after saving
//         setResolutionNotes(prev => ({ ...prev, [id]: "" }));
//       }
//     } catch (error) {
//       console.error("Error saving resolution notes:", error);
//     }
//   };

//   // Toggle complaint expansion
//   const toggleExpand = (id: string) => {
//     setExpandedId(expandedId === id ? null : id);
//   };

//   // Status badge component
//   const StatusBadge: React.FC<{ status: ComplaintStatus }> = ({ status }) => {
//     const statusConfig = {
//       Pending: { 
//         color: "bg-red-100 text-red-800", 
//         icon: <FiAlertCircle className="mr-1" /> 
//       },
//       "In Progress": { 
//         color: "bg-yellow-100 text-yellow-800", 
//         icon: <FiClock className="mr-1" /> 
//       },
//       Resolved: { 
//         color: "bg-green-100 text-green-800", 
//         icon: <FiCheck className="mr-1" /> 
//       }
//     };
    
//     return (
//       <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ${statusConfig[status].color}`}>
//         {statusConfig[status].icon}
//         {status}
//       </span>
//     );
//   };

//   return (
//     <div className="min-h-screen bg-gray-50">
//       <div className="fixed top-0 left-0 right-0 z-50">
//         <Navbar panelName="Admin" />
//       </div>

//       <div className="flex pt-16">
//         <div className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 z-40">
//           <Sidebar panelName="Admin" />
//         </div>

//         <main className="flex-1 ml-64 p-8 z-10">
//           <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
//             <h1 className="text-2xl md:text-3xl font-bold text-gray-800">Manage Complaints</h1>
            
//             <div className="flex flex-col sm:flex-row w-full md:w-auto gap-3">
//               <div className="relative flex-1">
//                 <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
//                   <FiSearch className="text-gray-400" />
//                 </div>
//                 <input
//                   type="text"
//                   placeholder="Search complaints..."
//                   className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
//                   value={filters.search}
//                   onChange={(e) => setFilters({...filters, search: e.target.value})}
//                 />
//               </div>
              
//               <div className="flex gap-3">
//                 <select
//                   className="border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
//                   value={filters.status}
//                   onChange={(e) => setFilters({
//                     ...filters, 
//                     status: e.target.value as ComplaintStatus | "all"
//                   })}
//                 >
//                   <option value="all">All Statuses</option>
//                   <option value="Pending">Pending</option>
//                   <option value="In Progress">In Progress</option>
//                   <option value="Resolved">Resolved</option>
//                 </select>
                
//                 <select
//                   className="border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
//                   value={filters.dateRange}
//                   onChange={(e) => setFilters({
//                     ...filters, 
//                     dateRange: e.target.value as DateRangeFilter
//                   })}
//                 >
//                   <option value="all">All Time</option>
//                   <option value="7days">Last 7 Days</option>
//                   <option value="30days">Last 30 Days</option>
//                 </select>
//               </div>
//             </div>
//           </div>

//           {loading ? (
//             <div className="flex justify-center items-center h-64">
//               <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
//             </div>
//           ) : filteredComplaints.length === 0 ? (
//             <div className="bg-white rounded-xl shadow-sm p-8 text-center">
//               <p className="text-gray-500 text-lg">No complaints found matching your criteria</p>
//             </div>
//           ) : (
//             <div className="space-y-4">
//               {filteredComplaints.map((complaint) => (
//                 <motion.div 
//                   key={complaint._id}
//                   initial={{ opacity: 0, y: 20 }}
//                   animate={{ opacity: 1, y: 0 }}
//                   transition={{ duration: 0.3 }}
//                   className="bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden"
//                 >
//                   <div 
//                     className="p-6 cursor-pointer flex justify-between items-center"
//                     onClick={() => toggleExpand(complaint._id)}
//                   >
//                     <div>
//                       <h3 className="text-lg font-semibold text-gray-800">
//                         {complaint.sourceStation} → {complaint.destinationStation}
//                       </h3>
//                       <div className="flex flex-wrap gap-2 mt-2 items-center">
//                         <span className="text-sm text-gray-500">
//                           {new Date(complaint.createdAt).toLocaleDateString()} • 
//                           Train: {complaint.trainNumber} • 
//                           PNR: {complaint.pnrNumber}
//                         </span>
//                       </div>
//                     </div>
                    
//                     <div className="flex items-center gap-4">
//                       <StatusBadge status={complaint.status} />
//                       {expandedId === complaint._id ? (
//                         <FiChevronUp className="text-gray-500" />
//                       ) : (
//                         <FiChevronDown className="text-gray-500" />
//                       )}
//                     </div>
//                   </div>

//                   <AnimatePresence>
//                     {expandedId === complaint._id && (
//                       <motion.div
//                         initial={{ height: 0, opacity: 0 }}
//                         animate={{ 
//                           height: "auto",
//                           opacity: 1,
//                           transition: {
//                             height: { duration: 0.3 },
//                             opacity: { duration: 0.2, delay: 0.1 }
//                           }
//                         }}
//                         exit={{ 
//                           height: 0,
//                           opacity: 0,
//                           transition: {
//                             height: { duration: 0.2 },
//                             opacity: { duration: 0.1 }
//                           }
//                         }}
//                         className="overflow-hidden"
//                       >
//                         <div className="px-6 pb-6 border-t border-gray-100">
//                           <div className="grid grid-cols-1 md:grid-cols-12 gap-6 mt-4">
//                             {/* Journey Details */}
//                             <div className="md:col-span-3 space-y-4">
//                               <div>
//                                 <h4 className="text-sm font-medium text-gray-500 mb-2">Journey Details</h4>
//                                 <div className="space-y-2 text-sm">
//                                   <p><span className="font-medium">Coach/Seat:</span> {complaint.coachNumber}/{complaint.seatNumber}</p>
//                                   <p><span className="font-medium">Date:</span> {new Date(complaint.createdAt).toLocaleDateString()}</p>
//                                   <p><span className="font-medium">PNR:</span> {complaint.pnrNumber}</p>
//                                 </div>
//                               </div>
//                             </div>
                            
//                             {/* Complaint Details */}
//                             <div className="md:col-span-5 space-y-4">
//                               <div>
//                                 <h4 className="text-sm font-medium text-gray-500 mb-2">Complaint</h4>
//                                 <p className="text-gray-700 whitespace-pre-line">{complaint.complaint}</p>
//                               </div>
//                             </div>
                            
//                             {/* Admin Actions */}
//                             <div className="md:col-span-4 space-y-4">
//                               <div>
//                                 <h4 className="text-sm font-medium text-gray-500 mb-2">Actions</h4>
//                                 <div className="flex flex-wrap gap-2">
//                                   <button
//                                     onClick={() => updateStatus(complaint._id, "In Progress")}
//                                     disabled={complaint.status === "In Progress"}
//                                     className={`px-3 py-1 rounded text-xs font-medium ${
//                                       complaint.status === "In Progress" 
//                                         ? "bg-gray-100 text-gray-500 cursor-not-allowed" 
//                                         : "bg-yellow-100 text-yellow-800 hover:bg-yellow-200"
//                                     }`}
//                                   >
//                                     Mark In Progress
//                                   </button>
//                                   <button
//                                     onClick={() => updateStatus(complaint._id, "Resolved")}
//                                     disabled={complaint.status === "Resolved"}
//                                     className={`px-3 py-1 rounded text-xs font-medium ${
//                                       complaint.status === "Resolved" 
//                                         ? "bg-gray-100 text-gray-500 cursor-not-allowed" 
//                                         : "bg-green-100 text-green-800 hover:bg-green-200"
//                                     }`}
//                                   >
//                                     Mark Resolved
//                                   </button>
//                                   {complaint.status === "Resolved" && (
//                                     <button
//                                       onClick={() => updateStatus(complaint._id, "Pending")}
//                                       className="px-3 py-1 rounded text-xs font-medium bg-red-100 text-red-800 hover:bg-red-200"
//                                     >
//                                       Reopen
//                                     </button>
//                                   )}
//                                 </div>
//                               </div>
                              
//                               {/* Resolution Notes (for resolved complaints) */}
//                               {complaint.status === "Resolved" && complaint.resolutionNotes && (
//                                 <div className="bg-green-50 p-3 rounded-lg">
//                                   <h4 className="text-sm font-medium text-green-800 mb-1">Resolution Notes</h4>
//                                   <p className="text-green-700 text-sm">{complaint.resolutionNotes}</p>
//                                 </div>
//                               )}
                              
//                               {/* Add Resolution Notes */}
//                               {complaint.status !== "Resolved" && (
//                                 <div className="mt-4">
//                                   <h4 className="text-sm font-medium text-gray-500 mb-2">Add Resolution Notes</h4>
//                                   <textarea
//                                     className="w-full border rounded-lg p-2 text-sm focus:ring-2 focus:ring-blue-500"
//                                     rows={3}
//                                     placeholder="Enter resolution details..."
//                                     value={resolutionNotes[complaint._id] || ""}
//                                     onChange={(e) => setResolutionNotes({
//                                       ...resolutionNotes,
//                                       [complaint._id]: e.target.value
//                                     })}
//                                   />
//                                   <button 
//                                     className="mt-2 px-3 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium hover:bg-blue-200"
//                                     onClick={() => saveResolutionNotes(complaint._id)}
//                                   >
//                                     Save Notes
//                                   </button>
//                                 </div>
//                               )}
//                             </div>
//                           </div>
//                         </div>
//                       </motion.div>
//                     )}
//                   </AnimatePresence>
//                 </motion.div>
//               ))}
//             </div>
//           )}
//         </main>
//       </div>
//     </div>
//   );
// };

// export default ManageComplaints;



"use client";

import React, { useState } from "react";
import Navbar from "@/app/components/Navbar";
import Sidebar from "@/app/components/Sidebar";
import { FiSearch, FiEdit, FiCheck, FiX, FiClock, FiAlertCircle, FiChevronDown, FiChevronUp } from "react-icons/fi";
import { motion, AnimatePresence } from "framer-motion";

// Type definitions
type ComplaintStatus = "Pending" | "In Progress" | "Resolved";
type DateRangeFilter = "all" | "7days" | "30days";

interface Complaint {
  _id: string;
  pnrNumber: string;
  trainNumber: string;
  coachNumber: string;
  seatNumber: string;
  sourceStation: string;
  destinationStation: string;
  complaint: string;
  status: ComplaintStatus;
  createdAt: string;
  resolutionNotes?: string;
  assignedTo?: string;
}

interface Filters {
  status: ComplaintStatus | "all";
  dateRange: DateRangeFilter;
  search: string;
}

const ManageComplaints: React.FC = () => {
  // Sample data
  const sampleComplaints: Complaint[] = [
    {
      _id: "1",
      pnrNumber: "PNR12345",
      trainNumber: "12345",
      coachNumber: "B1",
      seatNumber: "12",
      sourceStation: "Delhi",
      destinationStation: "Mumbai",
      complaint: "The seat was broken and couldn't recline properly. The metal frame was protruding and caused damage to my clothing. The armrest was loose and kept falling down throughout the trip.",
      status: "Pending",
      createdAt: "2023-06-15T10:30:00Z",
    },
    {
      _id: "2",
      pnrNumber: "PNR67890",
      trainNumber: "67890",
      coachNumber: "A2",
      seatNumber: "24",
      sourceStation: "Chennai",
      destinationStation: "Bangalore",
      complaint: "The air conditioning was not working properly throughout the journey. The vents were blowing warm air and some were dripping water, creating puddles in the aisle.",
      status: "In Progress",
      createdAt: "2023-06-18T08:15:00Z",
      assignedTo: "Maintenance Team B",
    },
    {
      _id: "3",
      pnrNumber: "PNR54321",
      trainNumber: "54321",
      coachNumber: "S3",
      seatNumber: "08",
      sourceStation: "Kolkata",
      destinationStation: "Patna",
      complaint: "The toilet was extremely unclean with foul odor. The flush was not working, the sink was clogged, and there was no water available. The door lock was broken, compromising privacy.",
      status: "Resolved",
      createdAt: "2023-06-20T14:45:00Z",
      resolutionNotes: "Compensation of ₹500 provided. Toilet facilities repaired and deep cleaned.",
    },
    {
      _id: "4",
      pnrNumber: "PNR98765",
      trainNumber: "98765",
      coachNumber: "C2",
      seatNumber: "15",
      sourceStation: "Hyderabad",
      destinationStation: "Pune",
      complaint: "The charging points were not working in my coach. I had important work to do during the journey but couldn't charge my laptop.",
      status: "In Progress",
      createdAt: "2023-06-22T16:20:00Z",
      assignedTo: "Electrical Team A",
    },
    {
      _id: "5",
      pnrNumber: "PNR24680",
      trainNumber: "24680",
      coachNumber: "D1",
      seatNumber: "30",
      sourceStation: "Jaipur",
      destinationStation: "Ahmedabad",
      complaint: "The food served was stale and caused stomach discomfort. The pantry staff was unresponsive when I complained about the quality.",
      status: "Pending",
      createdAt: "2023-06-24T12:10:00Z",
    },
  ];

  const [complaints, setComplaints] = useState<Complaint[]>(sampleComplaints);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [filters, setFilters] = useState<Filters>({
    status: "all",
    dateRange: "all",
    search: ""
  });
  const [resolutionNotes, setResolutionNotes] = useState<{ [key: string]: string }>({});

  // Filter complaints based on filters
  const filteredComplaints = complaints.filter(complaint => {
    // Status filter
    if (filters.status !== "all" && complaint.status !== filters.status) {
      return false;
    }
    
    // Date range filter
    if (filters.dateRange !== "all") {
      const complaintDate = new Date(complaint.createdAt);
      const now = new Date();
      const diffDays = Math.floor((now.getTime() - complaintDate.getTime()) / (1000 * 60 * 60 * 24));
      
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
    
    return true;
  });

  // Handle status update
  const updateStatus = (id: string, newStatus: ComplaintStatus) => {
    setComplaints(complaints.map(c => 
      c._id === id ? { ...c, status: newStatus } : c
    ));
  };

  // Save resolution notes
  const saveResolutionNotes = (id: string) => {
    setComplaints(complaints.map(c => 
      c._id === id ? { ...c, resolutionNotes: resolutionNotes[id] } : c
    ));
    // Clear the notes input after saving
    setResolutionNotes(prev => ({ ...prev, [id]: "" }));
  };

  // Toggle complaint expansion
  const toggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  // Status badge component
  const StatusBadge: React.FC<{ status: ComplaintStatus }> = ({ status }) => {
    const statusConfig = {
      Pending: { 
        color: "bg-red-100 text-red-800", 
        icon: <FiAlertCircle className="mr-1" /> 
      },
      "In Progress": { 
        color: "bg-yellow-100 text-yellow-800", 
        icon: <FiClock className="mr-1" /> 
      },
      Resolved: { 
        color: "bg-green-100 text-green-800", 
        icon: <FiCheck className="mr-1" /> 
      }
    };
    
    return (
      <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ${statusConfig[status].color}`}>
        {statusConfig[status].icon}
        {status}
      </span>
    );
  };

  // Format date for display
  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
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
                  onChange={(e) => setFilters({...filters, search: e.target.value})}
                />
              </div>
              
              <div className="flex gap-3">
                <select
                  className="border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  value={filters.status}
                  onChange={(e) => setFilters({
                    ...filters, 
                    status: e.target.value as ComplaintStatus | "all"
                  })}
                >
                  <option value="all">All Statuses</option>
                  <option value="Pending">Pending</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Resolved">Resolved</option>
                </select>
                
                <select
                  className="border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  value={filters.dateRange}
                  onChange={(e) => setFilters({
                    ...filters, 
                    dateRange: e.target.value as DateRangeFilter
                  })}
                >
                  <option value="all">All Time</option>
                  <option value="7days">Last 7 Days</option>
                  <option value="30days">Last 30 Days</option>
                </select>
              </div>
            </div>
          </div>

          {filteredComplaints.length === 0 ? (
            <div className="bg-white rounded-xl shadow-sm p-8 text-center">
              <p className="text-gray-500 text-lg">No complaints found matching your criteria</p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredComplaints.map((complaint) => (
                <motion.div 
                  key={complaint._id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  className="bg-white rounded-xl shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden"
                >
                  <div 
                    className="p-6 cursor-pointer flex justify-between items-center"
                    onClick={() => toggleExpand(complaint._id)}
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
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-4">
                      <StatusBadge status={complaint.status} />
                      {expandedId === complaint._id ? (
                        <FiChevronUp className="text-gray-500" />
                      ) : (
                        <FiChevronDown className="text-gray-500" />
                      )}
                    </div>
                  </div>

                  <AnimatePresence>
                    {expandedId === complaint._id && (
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
                            {/* Journey Details */}
                            <div className="md:col-span-3 space-y-4">
                              <div>
                                <h4 className="text-sm font-medium text-gray-500 mb-2">Journey Details</h4>
                                <div className="space-y-2 text-sm">
                                  <p><span className="font-medium">Coach/Seat:</span> {complaint.coachNumber}/{complaint.seatNumber}</p>
                                  <p><span className="font-medium">Date:</span> {formatDate(complaint.createdAt)}</p>
                                  <p><span className="font-medium">PNR:</span> {complaint.pnrNumber}</p>
                                </div>
                              </div>
                            </div>
                            
                            {/* Complaint Details */}
                            <div className="md:col-span-5 space-y-4">
                              <div>
                                <h4 className="text-sm font-medium text-gray-500 mb-2">Complaint</h4>
                                <p className="text-gray-700 whitespace-pre-line">{complaint.complaint}</p>
                              </div>
                            </div>
                            
                            {/* Admin Actions */}
                            <div className="md:col-span-4 space-y-4">
                              <div>
                                <h4 className="text-sm font-medium text-gray-500 mb-2">Actions</h4>
                                <div className="flex flex-wrap gap-2">
                                  <button
                                    onClick={() => updateStatus(complaint._id, "In Progress")}
                                    disabled={complaint.status === "In Progress"}
                                    className={`px-3 py-1 rounded text-xs font-medium ${
                                      complaint.status === "In Progress" 
                                        ? "bg-gray-100 text-gray-500 cursor-not-allowed" 
                                        : "bg-yellow-100 text-yellow-800 hover:bg-yellow-200"
                                    }`}
                                  >
                                    Mark In Progress
                                  </button>
                                  <button
                                    onClick={() => updateStatus(complaint._id, "Resolved")}
                                    disabled={complaint.status === "Resolved"}
                                    className={`px-3 py-1 rounded text-xs font-medium ${
                                      complaint.status === "Resolved" 
                                        ? "bg-gray-100 text-gray-500 cursor-not-allowed" 
                                        : "bg-green-100 text-green-800 hover:bg-green-200"
                                    }`}
                                  >
                                    Mark Resolved
                                  </button>
                                  {complaint.status === "Resolved" && (
                                    <button
                                      onClick={() => updateStatus(complaint._id, "Pending")}
                                      className="px-3 py-1 rounded text-xs font-medium bg-red-100 text-red-800 hover:bg-red-200"
                                    >
                                      Reopen
                                    </button>
                                  )}
                                </div>
                              </div>
                              
                              {/* Resolution Notes (for resolved complaints) */}
                              {complaint.status === "Resolved" && complaint.resolutionNotes && (
                                <div className="bg-green-50 p-3 rounded-lg">
                                  <h4 className="text-sm font-medium text-green-800 mb-1">Resolution Notes</h4>
                                  <p className="text-green-700 text-sm">{complaint.resolutionNotes}</p>
                                </div>
                              )}
                              
                              {/* Add Resolution Notes */}
                              {complaint.status !== "Resolved" && (
                                <div className="mt-4">
                                  <h4 className="text-sm font-medium text-gray-500 mb-2">Add Resolution Notes</h4>
                                  <textarea
                                    className="w-full border rounded-lg p-2 text-sm focus:ring-2 focus:ring-blue-500"
                                    rows={3}
                                    placeholder="Enter resolution details..."
                                    value={resolutionNotes[complaint._id] || ""}
                                    onChange={(e) => setResolutionNotes({
                                      ...resolutionNotes,
                                      [complaint._id]: e.target.value
                                    })}
                                  />
                                  <button 
                                    className="mt-2 px-3 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium hover:bg-blue-200"
                                    onClick={() => saveResolutionNotes(complaint._id)}
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