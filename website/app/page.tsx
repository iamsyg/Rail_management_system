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

  const [name, setName] = useState("");
  const [formData, setFormData] = useState<FormData>({
      email: '',
      password: '',
    });

  useEffect(() => {
    
    const fetchData = async () => {
      try {
        const res = await fetch('http://localhost:8080/auth/signin', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify({
            email: formData.email,
            password: formData.password
          }),
        });

        if (!res.ok) {
          console.log("Not authenticated or some error occurred");
          return;
        }

        const data = await res.json();
        console.log(data.name);
        setName(data.name);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);
  

  
  return (
    <div className="container">
      {!name && (
        <div className="container">
          {redirect("/signin")}
        </div> )
      } 
    </div>
  );
}
