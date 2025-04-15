"use client";

import React, { useState, FormEvent } from 'react';
import Navbar from "@/app/components/Navbar";
import Sidebar from "@/app/components/Sidebar";

interface ComplaintFormData {
  name: string;
  email: string;
  phone: string;
  complaint: string;
}

interface FormErrors {
  name?: string;
  email?: string;
  phone?: string;
  complaint?: string;
}

export default function ComplaintPage() {
  const [formData, setFormData] = useState<ComplaintFormData>({
    name: '',
    email: '',
    phone: '',
    complaint: ''
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [submitSuccess, setSubmitSuccess] = useState<boolean>(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};
    
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    else if (!/^\S+@\S+\.\S+$/.test(formData.email)) newErrors.email = 'Email is invalid';
    if (!formData.phone.trim()) newErrors.phone = 'Phone number is required';
    else if (!/^[\d\s\+\-\(\)]{10,}$/.test(formData.phone)) newErrors.phone = 'Invalid phone number';
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
          name: '',
          email: '',
          phone: '',
          complaint: ''
        });
      } catch (error) {
        console.error('Error submitting complaint:', error);
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="flex">
        <Sidebar />
        
        <main className="flex-1 p-8">
          <div className="max-w-6xl mx-auto">
            <h1 className="text-2xl font-bold mb-6">File a Complaint</h1>
            
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
                        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                          Full Name *
                        </label>
                        <input
                          type="text"
                          id="name"
                          name="name"
                          value={formData.name}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.name ? 'border-red-500' : 'border-gray-300'}`}
                          placeholder="Enter your full name"
                        />
                        {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name}</p>}
                      </div>
                      
                      <div>
                        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                          Email Address *
                        </label>
                        <input
                          type="email"
                          id="email"
                          name="email"
                          value={formData.email}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.email ? 'border-red-500' : 'border-gray-300'}`}
                          placeholder="Enter your email"
                        />
                        {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email}</p>}
                      </div>
                      
                      <div>
                        <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">
                          Phone Number *
                        </label>
                        <input
                          type="tel"
                          id="phone"
                          name="phone"
                          value={formData.phone}
                          onChange={handleChange}
                          className={`w-full px-3 py-2 border rounded-md ${errors.phone ? 'border-red-500' : 'border-gray-300'}`}
                          placeholder="Enter your phone number"
                        />
                        {errors.phone && <p className="mt-1 text-sm text-red-600">{errors.phone}</p>}
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
                    Call our support hotline: <span className="font-semibold">+1 (800) 123-4567</span>
                  </p>
                  <div className="space-y-3">
                    <div className="flex items-start">
                      <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                      </svg>
                      <div>
                        <h3 className="font-medium text-blue-800">24/7 Support</h3>
                        <p className="text-sm text-blue-600">Available round the clock</p>
                      </div>
                    </div>
                    <div className="flex items-start">
                      <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <div>
                        <h3 className="font-medium text-blue-800">Fast Response</h3>
                        <p className="text-sm text-blue-600">Average wait time: 2 minutes</p>
                      </div>
                    </div>
                    <div className="flex items-start">
                      <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                      </svg>
                      <div>
                        <h3 className="font-medium text-blue-800">Verified Experts</h3>
                        <p className="text-sm text-blue-600">Certified professionals</p>
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