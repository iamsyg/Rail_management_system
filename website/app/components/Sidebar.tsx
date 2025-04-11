"use client";

import React, { useEffect, useState } from "react";

function Sidebar() {

    const [name, setName] = useState("");
    
      useEffect(() => {
        
        // const fetchData = async() => {
        //   try {
        //     const response = await fetch('http://localhost:8080/auth/profile', {
        //       method: 'GET',
        //       credentials: 'include',
        //       headers: {
        //         'Content-Type': 'application/json',
        //       },
        //     });

        //     if (response.status === 401) {
        //       await fetch("http://localhost:8080/auth/refresh", { 
        //         method: "POST", 
        //         credentials: "include",
        //         headers: {
        //           'Content-Type': 'application/json',
        //         },
        //       });
        //       return await fetch("http://localhost:8080/auth/profile", { credentials: "include" });
        //     }

        //     if (!response.ok) {
        //       throw new Error('Network response was not ok');
        //     }
        //     const data = await response.json();
        //     setName(data.name);
        //   } catch (error) {
        //     console.error('Error fetching data:', error);  
        //   }
        // }

        const fetchData = async () => {
  try {
    let response = await fetch('http://localhost:8080/auth/profile', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // If access token is expired, try refreshing
    if (response.status === 401) {
      const refreshResponse = await fetch("http://localhost:8080/auth/refresh", {
        method: "POST",
        credentials: "include",
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // If refresh also fails, exit early
      if (!refreshResponse.ok) {
        throw new Error("Unable to refresh token");
      }

      // Retry profile after refresh
      response = await fetch("http://localhost:8080/auth/profile", {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });
    }

    if (!response.ok) {
      throw new Error('Final profile fetch failed');
    }

    const data = await response.json();
    setName(data.name);

  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

    
        fetchData();
      }, []);
    

  return (
    <div>
      <ul className="menu bg-base-200 rounded-box w-56">
        <li>
          <h2 className="menu-title">{name}</h2>
          <ul>
            <li>
              <a>Item 1</a>
            </li>
            <li>
              <a>Item 2</a>
            </li>
            <li>
              <a>Item 3</a>
            </li>
          </ul>
        </li>
      </ul>
    </div>
  );
}

export default Sidebar;
