import React from 'react'
import Navbar from '@/app/components/Navbar'
import Sidebar from '@/app/components/Sidebar'

const page = () => {
  return (
    <div>
      <div className="min-h-screen bg-gray-100">
      <Navbar panelName='User'/>
      
      <div className="flex">
        <Sidebar panelName='User'/>
        
        <main className="flex-1 p-8">
          <h1 className="text-2xl font-bold mb-8">Dashboard</h1>
          
        </main>
      </div>
    </div>
    </div>
  )
}

export default page
