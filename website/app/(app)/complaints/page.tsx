"use client";

import React, { useState, FormEvent } from 'react';
import Navbar from "@/app/components/Navbar";
import Sidebar from "@/app/components/Sidebar";

interface ComplaintFormData {
  trainNumber: string;
  pnr: string;
  coach: string;
  seatNumber: string;
  source: string;
  destination: string;
  complaint: string;
}

interface FormErrors {
  trainNumber?: string;
  pnr?: string;
  coach?: string;
  seatNumber?: string;
  source?: string;
  destination?: string;
  complaint?: string;
}

export default function ComplaintPage() {
  const [formData, setFormData] = useState<ComplaintFormData>({
    trainNumber: '',
    pnr: '',
    coach: '',
    seatNumber: '',
    source: '',
    destination: '',
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
    if (!formData.pnr.trim()) newErrors.pnr = 'PNR is required';
    else if (!/^[A-Za-z0-9]{10}$/.test(formData.pnr)) newErrors.pnr = 'PNR must be 10 alphanumeric characters';
    if (!formData.coach.trim()) newErrors.coach = 'Coach number is required';
    if (!formData.seatNumber.trim()) newErrors.seatNumber = 'Seat number is required';
    if (!formData.source.trim()) newErrors.source = 'Source station is required';
    if (!formData.destination.trim()) newErrors.destination = 'Destination station is required';
    if (!formData.complaint.trim()) newErrors.complaint = 'Complaint description is required';
    else if (formData.complaint.length < 20) newErrors.complaint = 'Complaint must be at least 20 characters';
    
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
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        console.log('Complaint submitted:', formData);
        setSubmitSuccess(true);
        setFormData({
          trainNumber: '',
          pnr: '',
          coach: '',
          seatNumber: '',
          source: '',
          destination: '',
          complaint: ''
        });
      } catch (error) {
        console.error('Error submitting complaint:', error);
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
                          type="text"
                          id="trainNumber"
                          name="trainNumber"
                          value={formData.trainNumber}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.trainNumber ? 'border-red-500' : 'border-gray-300'}`}
                          placeholder="Enter train number"
                        />
                        {errors.trainNumber && <p className="mt-1 text-sm text-red-600">{errors.trainNumber}</p>}
                      </div>

                      <div>
                        <label htmlFor="pnr" className="block text-sm font-medium text-gray-700 mb-1">
                          PNR Number *
                        </label>
                        <input
                          type="text"
                          id="pnr"
                          name="pnr"
                          value={formData.pnr}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.pnr ? 'border-red-500' : 'border-gray-300'}`}
                          placeholder="Enter 10-digit PNR"
                          maxLength={10}
                        />
                        {errors.pnr && <p className="mt-1 text-sm text-red-600">{errors.pnr}</p>}
                      </div>

                      <div>
                        <label htmlFor="coach" className="block text-sm font-medium text-gray-700 mb-1">
                          Coach Number *
                        </label>
                        <input
                          type="text"
                          id="coach"
                          name="coach"
                          value={formData.coach}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.coach ? 'border-red-500' : 'border-gray-300'}`}
                          placeholder="Enter coach number (e.g., A1, B2)"
                        />
                        {errors.coach && <p className="mt-1 text-sm text-red-600">{errors.coach}</p>}
                      </div>

                      <div>
                        <label htmlFor="seatNumber" className="block text-sm font-medium text-gray-700 mb-1">
                          Seat Number *
                        </label>
                        <input
                          type="text"
                          id="seatNumber"
                          name="seatNumber"
                          value={formData.seatNumber}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.seatNumber ? 'border-red-500' : 'border-gray-300'}`}
                          placeholder="Enter seat number (e.g., 12, 24B)"
                        />
                        {errors.seatNumber && <p className="mt-1 text-sm text-red-600">{errors.seatNumber}</p>}
                      </div>

                      <div>
                        <label htmlFor="source" className="block text-sm font-medium text-gray-700 mb-1">
                          Source Station *
                        </label>
                        <select
                          id="source"
                          name="source"
                          value={formData.source}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.source ? 'border-red-500' : 'border-gray-300'}`}
                        >
                          {stations.map(station => (
                            <option key={station.value} value={station.value}>
                              {station.label}
                            </option>
                          ))}
                        </select>
                        {errors.source && <p className="mt-1 text-sm text-red-600">{errors.source}</p>}
                      </div>

                      <div>
                        <label htmlFor="destination" className="block text-sm font-medium text-gray-700 mb-1">
                          Destination Station *
                        </label>
                        <select
                          id="destination"
                          name="destination"
                          value={formData.destination}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.destination ? 'border-red-500' : 'border-gray-300'}`}
                        >
                          {stations.map(station => (
                            <option key={station.value} value={station.value}>
                              {station.label}
                            </option>
                          ))}
                        </select>
                        {errors.destination && <p className="mt-1 text-sm text-red-600">{errors.destination}</p>}
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