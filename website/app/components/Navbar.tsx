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
  

  return( 

    <>
    <div className="navbar bg-neutral text-neutral-content">
  <div className="flex-1">
    <a className="btn btn-ghost text-xl">RailComplainDesk</a>
  </div>
  <div className="flex-none">
    <button className="btn btn-square btn-ghost" onClick={logoutHandler}>
    <IoIosLogOut />
    </button>
  </div>
</div>
    </>
  );
}

export default Navbar;
