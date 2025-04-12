"use client"

import Image from "next/image";
import { useEffect, useState } from "react";
import Signup from "./(app)/signup/page";
import { redirect } from "next/navigation";

interface FormData {
  email: string;
  password: string;
}

export default function Home() {
  
  return (
    <div className="container">
      {(
        <div className="container">
          {redirect("/signin")}
        </div> )
      } 
    </div>
  );
}
