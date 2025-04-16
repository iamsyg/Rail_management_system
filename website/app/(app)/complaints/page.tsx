"use client";

import React, { useState, FormEvent } from 'react';
import Navbar from "@/app/components/Navbar";
import Sidebar from "@/app/components/Sidebar";

interface ComplaintFormData {
  trainNumber: string;
  pnrNumber: string;
  coachNumber: string;
  seatNumber: string;
  sourceStation: string;
  destinationStation: string;
  complaint: string;
}

interface FormErrors {
  trainNumber?: string;
  pnrNumber?: string;
  coachNumber?: string;
  seatNumber?: string;
  sourceStation?: string;
  destinationStation?: string;
  complaint?: string;
}

function getCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  if (match) return match[2];
  return null;
}

export default function ComplaintPage() {
  const [formData, setFormData] = useState<ComplaintFormData>({
    trainNumber: '',
    pnrNumber: '',
    coachNumber: '',
    seatNumber: '',
    sourceStation: '',
    destinationStation: '',
    complaint: ''
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [submitSuccess, setSubmitSuccess] = useState<boolean>(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};
  
    if (!formData.trainNumber.trim()) newErrors.trainNumber = 'Train number is required';
    else if (isNaN(Number(formData.trainNumber))) newErrors.trainNumber = 'Train number must be a number';
  
    if (!formData.pnrNumber.trim()) newErrors.pnrNumber = 'PNR is required';
    else if (formData.pnrNumber.length !== 10) newErrors.pnrNumber = 'PNR must be 10 characters';
    else if (isNaN(Number(formData.pnrNumber))) newErrors.pnrNumber = 'PNR must be numeric';
  
    if (!formData.coachNumber.trim()) newErrors.coachNumber = 'Coach number is required';
  
    if (!formData.seatNumber.trim()) newErrors.seatNumber = 'Seat number is required';
    else if (isNaN(Number(formData.seatNumber))) newErrors.seatNumber = 'Seat number must be a number';
  
    if (!formData.sourceStation.trim()) newErrors.sourceStation = 'Source station is required';
    if (!formData.destinationStation.trim()) newErrors.destinationStation = 'Destination station is required';
    if (!formData.complaint.trim()) newErrors.complaint = 'Complaint description is required';
  
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };  

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSubmitSuccess(false);
    
    if (validateForm()) {
      setIsSubmitting(true);
      try {
        // Simulate API call
        const response = await fetch("http://localhost:8080/complaints/", {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": getCookie("csrf_access_token") || " "  // your helper to read cookies
          },
          body: JSON.stringify(formData)
        });

        if(response.ok){
          const data = await response.json();
          console.log(data);
        } else {
          const errorData = await response.json();
          throw new Error(errorData.message || 'An unexpected error occurred');
        }
        
        console.log('Complaint submitted:', formData);
        setSubmitSuccess(true);
        setFormData({
          trainNumber: '',
          pnrNumber: '',
          coachNumber: '',
          seatNumber: '',
          sourceStation: '',
          destinationStation: '',
          complaint: ''
        });
      } catch (error: any) {
        console.error('Error submitting complaint:', error, error.message);
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  // Sample station data - replace with your actual station list
  const stations = [
    { value: '', label: 'Select station' },
    { value: 'DEL', label: 'Delhi (DEL)' },
    { value: 'MUM', label: 'Mumbai (MUM)' },
    { value: 'CHE', label: 'Chennai (CHE)' },
    { value: 'KOL', label: 'Kolkata (KOL)' },
    { value: 'BAN', label: 'Bangalore (BAN)' },
    { value: 'HYD', label: 'Hyderabad (HYD)' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="flex">
        <Sidebar />
        
        <main className="flex-1 p-8">
          <div className="max-w-6xl mx-auto">
            <h1 className="text-2xl font-bold mb-6">File a Train Complaint</h1>
            
            {submitSuccess && (
              <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
                Your complaint has been submitted successfully! We'll get back to you soon.
              </div>
            )}
            
            <div className="flex flex-col lg:flex-row gap-8">
              {/* Complaint Form - Takes 2/3 width on larger screens */}
              <div className="lg:w-2/3">
                <form onSubmit={handleSubmit} className="bg-white shadow rounded-lg p-6 h-full">
                  <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label htmlFor="trainNumber" className="block text-sm font-medium text-gray-700 mb-1">
                          Train Number *
                        </label>
                        <input
                          type="number"
                          id="trainNumber"
                          name="trainNumber"
                          value={formData.trainNumber}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.trainNumber ? 'border-red-500' : 'border-gray-300'}`}
                          placeholder="Enter train number"
                          required
                        />
                        {errors.trainNumber && <p className="mt-1 text-sm text-red-600">{errors.trainNumber}</p>}
                      </div>

                      <div>
                        <label htmlFor="pnrNumber" className="block text-sm font-medium text-gray-700 mb-1">
                          PNR Number *
                        </label>
                        <input
                          type="number"
                          id="pnrNumber"
                          name="pnrNumber"
                          value={formData.pnrNumber}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.pnrNumber ? 'border-red-500' : 'border-gray-300'}`}
                          placeholder="Enter 10-digit PNR"
                          max={9999999999}
                          required
                        />
                        {errors.pnrNumber && <p className="mt-1 text-sm text-red-600">{errors.pnrNumber}</p>}
                      </div>

                      <div>
                        <label htmlFor="coachNumber" className="block text-sm font-medium text-gray-700 mb-1">
                          Coach Number *
                        </label>
                        <input
                          type="text"
                          id="coachNumber"
                          name="coachNumber"
                          value={formData.coachNumber}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.coachNumber ? 'border-red-500' : 'border-gray-300'}`}
                          placeholder="Enter coach number (e.g., A1, B2)"
                          required
                        />
                        {errors.coachNumber && <p className="mt-1 text-sm text-red-600">{errors.coachNumber}</p>}
                      </div>

                      <div>
                        <label htmlFor="seatNumber" className="block text-sm font-medium text-gray-700 mb-1">
                          Seat Number *
                        </label>
                        <input
                          type="number"
                          id="seatNumber"
                          name="seatNumber"
                          value={formData.seatNumber}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.seatNumber ? 'border-red-500' : 'border-gray-300'}`}
                          placeholder="Enter seat number (e.g., 12, 24)"
                          required
                        />
                        {errors.seatNumber && <p className="mt-1 text-sm text-red-600">{errors.seatNumber}</p>}
                      </div>

                      <div>
                        <label htmlFor="sourceStation" className="block text-sm font-medium text-gray-700 mb-1">
                          Source Station *
                        </label>
                        <select
                          id="sourceStation"
                          name="sourceStation"
                          value={formData.sourceStation}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.sourceStation ? 'border-red-500' : 'border-gray-300'}`}
                          required
                        >
                          {stations.map(station => (
                            <option key={station.value} value={station.value}>
                              {station.label}
                            </option>
                          ))}
                        </select>
                        {errors.sourceStation && <p className="mt-1 text-sm text-red-600">{errors.sourceStation}</p>}
                      </div>

                      <div>
                        <label htmlFor="destinationStation" className="block text-sm font-medium text-gray-700 mb-1">
                          Destination Station *
                        </label>
                        <select
                          id="destinationStation"
                          name="destinationStation"
                          value={formData.destinationStation}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.destinationStation ? 'border-red-500' : 'border-gray-300'}`}
                          required
                        >
                          {stations.map(station => (
                            <option key={station.value} value={station.value}>
                              {station.label}
                            </option>
                          ))}
                        </select>
                        {errors.destinationStation && <p className="mt-1 text-sm text-red-600">{errors.destinationStation}</p>}
                      </div>
                    </div>
                    
                    <div>
                      <label htmlFor="complaint" className="block text-sm font-medium text-gray-700 mb-1">
                        Complaint Details *
                      </label>
                      <textarea
                        id="complaint"
                        name="complaint"
                        value={formData.complaint}
                        onChange={handleChange}
                        rows={6}
                        className={`w-full px-3 py-2 border rounded-md ${errors.complaint ? 'border-red-500' : 'border-gray-300'}`}
                        placeholder="Please describe your complaint in detail (minimum 20 characters)"
                        required
                      />
                      {errors.complaint && <p className="mt-1 text-sm text-red-600">{errors.complaint}</p>}
                      <p className="mt-1 text-sm text-gray-500">
                        Character count: {formData.complaint.length}/500
                      </p>
                    </div>
                    
                    <div className="flex justify-end">
                      <button
                        type="submit"
                        disabled={isSubmitting}
                        className={`px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${isSubmitting ? 'opacity-75 cursor-not-allowed' : ''}`}
                      >
                        {isSubmitting ? 'Submitting...' : 'Submit Complaint'}
                      </button>
                    </div>
                    
                    <p className="text-sm text-gray-500">
                      * Required fields
                    </p>
                  </div>
                </form>
              </div>
              
              {/* Assistance Box - Takes 1/3 width on larger screens */}
              <div className="lg:w-1/3">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 h-full sticky top-6">
                  <h2 className="text-lg font-medium text-blue-800 mb-3">Need immediate assistance?</h2>
                  <p className="text-blue-700 mb-4">
                    Call our railway support: <span className="font-semibold">139 (Railway Helpline)</span>
                  </p>
                  <div className="space-y-3">
                    <div className="flex items-start">
                      <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                      </svg>
                      <div>
                        <h3 className="font-medium text-blue-800">24/7 Railway Support</h3>
                        <p className="text-sm text-blue-600">Available for all train-related issues</p>
                      </div>
                    </div>
                    <div className="flex items-start">
                      <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <div>
                        <h3 className="font-medium text-blue-800">Quick Resolution</h3>
                        <p className="text-sm text-blue-600">Average resolution time: 24 hours</p>
                      </div>
                    </div>
                    <div className="flex items-start">
                      <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                      </svg>
                      <div>
                        <h3 className="font-medium text-blue-800">Official Channels</h3>
                        <p className="text-sm text-blue-600">Direct connection to railway authorities</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}