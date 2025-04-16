"use client";

import React, { useEffect, useState } from "react";
import { IoIosLogOut } from "react-icons/io";
import { useRouter } from "next/navigation";

function Navbar() {

  const [message, setMessage] = useState("");
  const router = useRouter();

  const logoutHandler = async () => {
    try {
      const res = await fetch("http://localhost:8080/auth/logout", {
        method: "POST",
        credentials: "include",
      });
  
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

  const adminSigninHandler = () => {
    router.push("/admin-signin")
  }
  

  return( 

    <>
    <div className="navbar bg-neutral text-neutral-content">
  <div className="flex-1">
    <a className="btn btn-ghost text-xl">RailComplainDesk</a>
  </div>
  <div className="flex gap-6 mr-3">
    <button className="btn btn-square btn-ghost p-3" onClick={adminSigninHandler}>
      Admin
    </button>
    <button className="btn btn-square btn-ghost p-3" onClick={logoutHandler}>
    Logout
    </button>
  </div>
</div>
    </>
  );
}

export default Navbar;
