"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ToastContainer, toast } from 'react-toastify';

type NavbarProps = {
  panelName: string;
};

function Navbar({ panelName }: NavbarProps) {
  const [message, setMessage] = useState("");
  const router = useRouter();

  const logoutHandler = async () => {
    try {
      const res = await toast.promise(
        fetch("http://localhost:8080/auth/logout", {
          method: "POST",
          credentials: "include",
        }),
        {
          pending: 'Logging out...',
          success: 'Logged out successfully',
          error: 'Logout failed'
        }
      );


      if (res.ok) {
        // Optional: redirect or update UI
        setMessage("Logged out successfully");
        router.push("/signin");
      } else {
        setMessage("Logout failed");
      }
    } catch (error) {
      console.error("Error during logout:", error);
      setMessage("Something went wrong");
    }
  };

  const checkAdmin = async () => {
    try {
      const res = await fetch("http://localhost:8080/auth/profile", {
          method: "GET",
          credentials: "include",
        })
        
    

      if (!res.ok) {
        if (res.status === 401) {
          router.push("/signin");
        }
      }

      const userData = await res.json();
      console.log(userData);

      if (userData.user.role === "admin") {
        // router.push("/admin-dashboard");

        // if(panelName === "User") {
        //   router.push("/dashboard");
        // }


        if (panelName === "User") {
          router.push("/dashboard");
        } else {
          router.push("/admin-dashboard");
        }
      } else {
        
        toast.error('Access denied: Admins only area', {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: false,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: "dark",
        });
      }
    } catch (error) {
      console.error("Error during logout:", error);
      return false;
    }
  };

  return (
    <>
      <div className="navbar bg-neutral text-neutral-content">
        <div className="flex-1">
          <a className="btn btn-ghost text-xl">RailComplainDesk</a>
        </div>
        <div className="flex gap-6 mr-3">
          <button className="btn btn-square btn-ghost p-3" onClick={checkAdmin}>
            {panelName}
          </button>
          <button
            className="btn btn-square btn-ghost p-3"
            onClick={logoutHandler}
          >
            Logout
          </button>
        </div>
      </div>

      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick={false}
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
    </>
  );
}

export default Navbar;
