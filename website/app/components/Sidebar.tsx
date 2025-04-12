"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { g } from "framer-motion/client";

function Sidebar() {
  const [name, setName] = useState("");

  useEffect(() => {

    function fetchData() {

      fetch("http://localhost:8080/auth/signin", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: "user@example.com",
          password: "password123"
        })
      })
      .then(response => response.json())
      .then(data => {
        const accessToken = data.accessToken;
      
        getProfile(accessToken);
      })
      .catch(error => {
        console.error("Login failed:", error);
      });
    }
    

    const getProfile = async (accessToken: String) => {
      try {
        let response = await fetch("http://localhost:8080/auth/profile", {
          method: "GET",
          credentials: "include",
          headers: {
            "Authorization": `Bearer ${accessToken}`
          },
        });

        if (response.status === 401) {
          const refreshResponse = await fetch(
            "http://localhost:8080/auth/refresh",
            {
              method: "POST",
              credentials: "include",
              headers: {
                "Content-Type": "application/json",
              },
            }
          );

          if (!refreshResponse.ok) {
            throw new Error("Unable to refresh token");
          }

          response = await fetch("http://localhost:8080/auth/profile", {
            method: "GET",
            credentials: "include",
            headers: {
              "Authorization": `Bearer ${accessToken}`, // Use the new AccessToken}`,
            },
          });
        }

        if (!response.ok) {
          throw new Error("Final profile fetch failed");
        }

        const data = await response.json();
        setName(data.user.name);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <div className="drawer lg:drawer-open">
        <input id="my-drawer-2" type="checkbox" className="drawer-toggle" />
        <div className="drawer-content flex flex-col items-center justify-center">
          <label
            htmlFor="my-drawer-2"
            className="btn btn-primary drawer-button lg:hidden"
          >
            Open drawer
          </label>
        </div>
        <div className="drawer-side">
          <label
            htmlFor="my-drawer-2"
            aria-label="close sidebar"
            className="drawer-overlay"
          ></label>
          <ul className="menu min-h-full w-80 p-4 bg-black text-white text-xl gap-4">
            {/* Sidebar content here */}
            {name && (
              <li className="text-xl font-bold mb-4">
                Welcome, {name}
              </li>
            )}
            <li>
              <Link href="/dashboard"  className="hover:bg-gray-800">Dashboard</Link>
            </li>
            <li>
              <Link href="/account-settings"  className="hover:bg-gray-800">Account Settings</Link>
            </li>
            <li>
              <Link href="/account-settings"  className="hover:bg-gray-800">Complaints</Link>
            </li>
            <li>
              <Link href="/account-settings"  className="hover:bg-gray-800">Complaint History</Link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;