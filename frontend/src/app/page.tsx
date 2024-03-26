"use client";

import { Button } from "antd";
import { deleteCookie } from "cookies-next";
import { useRouter } from "next/navigation";

export default function Page() {
  const router = useRouter();
  
  const onLogoutClick = () => {
    deleteCookie("token");
    deleteCookie("refresh_token");
    router.push("/login");
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        height: "100vh",
      }}
    >
      <h1>Welcome to app</h1>
      <Button onClick={onLogoutClick}>Logout</Button>
    </div>
  );
  // Define other routes and logic
}
