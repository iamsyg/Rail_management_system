"use client";

import React from "react";
import Navbar from "@/app/components/Navbar";
import Sidebar from "@/app/components/Sidebar";

function page() {
  // Sample complaint data with longer complaints
  const complaints = [
    {
      id: 1,
      trainNumber: "12345",
      pnrNumber: "2345123434",
      coach: "B1",
      seatNumber: "12",
      sourceStation: "Delhi",
      destination: "Mumbai",
      complaint: "The seat was completely broken and couldn't recline properly, making the entire journey extremely uncomfortable. The metal frame was protruding and caused damage to my clothing. Additionally, the armrest was loose and kept falling down throughout the trip. I reported this to the train staff, but they were unable to provide a replacement seat or any assistance. This was particularly frustrating as I had booked my ticket well in advance and expected a comfortable journey. I had to endure the discomfort for the entire 16-hour journey, which was unacceptable. I would like a full refund for this ticket as I couldn't use the seat properly. I also suggest that the train staff be trained to handle such complaints more effectively in the future. this is thr best thing that can be done to improve the experience of passengers. I can see this a the best thing that  can be done to improve the experience of passengers. I can see this a the best thing that can be done to improve the experience of passengers. I can see this a the best thing that can be done to improve the experience of passengers. I can see this a the best thing that can be done to improve the experience of passengers. I can see this a the best thing that can be done to improve the experience of passengers.",
      status: "Resolved",
      date: "2023-10-15"
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
      date: "2023-10-18"
    },
    {
      id: 3,
      trainNumber: "54321",
      pnrNumber: "IJKL9012",
      coach: "S3",
      seatNumber: "08",
      sourceStation: "Kolkata Howrah",
      destination: "Patna Junction",
      complaint: "The toilet was extremely unclean, with foul odor emanating throughout the coach. The flush was not working, the sink was clogged, and there was no water available. The door lock was broken, compromising privacy. This condition persisted for the entire 12-hour journey despite requests to clean it at multiple stations where we had longer stops.",
      status: "Pending",
      date: "2023-10-20"
    },
  ];

  return (
    <div>
      <div className="min-h-screen bg-gray-100">
        <div className="fixed top-0 left-0 right-0 z-50">
          <Navbar panelName="Admin" />
        </div>

        <div className="sidebar flex pt-16">
          <div className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-64 z-40">
            <Sidebar panelName="Admin" />
          </div>

          <main className="flex-1 ml-64 p-8 z-10">
            <h1 className="text-2xl font-bold mb-8">Complaint History</h1>
            
            <div className="space-y-6">
              {complaints.map((item) => (
                <div key={item.id} className="bg-white shadow-md rounded-lg p-6 w-full overflow-hidden">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Left Column */}
                    <div className="space-y-3 break-words">
                      <div className="flex flex-col sm:flex-row justify-between pb-2 border-b">
                        <span className="font-medium text-gray-500">Date:</span>
                        <span className="text-right sm:text-left">{item.date}</span>
                      </div>
                      <div className="flex flex-col sm:flex-row justify-between pb-2 border-b">
                        <span className="font-medium text-gray-500">Train Number:</span>
                        <span className="text-right sm:text-left">{item.trainNumber}</span>
                      </div>
                      <div className="flex flex-col sm:flex-row justify-between pb-2 border-b">
                        <span className="font-medium text-gray-500">PNR Number:</span>
                        <span className="text-right sm:text-left">{item.pnrNumber}</span>
                      </div>
                      <div className="flex flex-col sm:flex-row justify-between pb-2 border-b">
                        <span className="font-medium text-gray-500">Coach/Seat:</span>
                        <span className="text-right sm:text-left">{item.coach}/{item.seatNumber}</span>
                      </div>
                    </div>
                    
                    {/* Right Column */}
                    <div className="space-y-3 break-words">
                      <div className="flex flex-col sm:flex-row justify-between pb-2 border-b">
                        <span className="font-medium text-gray-500">Route:</span>
                        <span className="text-right sm:text-left">{item.sourceStation} → {item.destination}</span>
                      </div>
                      <div className="flex flex-col sm:flex-row justify-between pb-2 border-b">
                        <span className="font-medium text-gray-500">Status:</span>
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                          ${item.status === "Resolved" ? "bg-green-100 text-green-800" : 
                            item.status === "In Progress" ? "bg-yellow-100 text-yellow-800" : 
                            "bg-red-100 text-red-800"}`}>
                          {item.status}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  {/* Complaint (full width) with proper text wrapping */}
                  <div className="mt-4 pt-4 border-t">
                    <h3 className="font-medium text-gray-500 mb-2">Complaint:</h3>
                    <p className="text-gray-700 whitespace-normal break-words">
                      {item.complaint}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}

export default page;