"use client"; // if using Next.js 13/14

import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="flex justify-between items-center p-4 bg-blue-600 text-white">
      <h1 className="text-xl font-bold">My App</h1>
      <div className="space-x-4">
        <Link href="/auth/login">
          <button className="bg-white text-blue-600 px-4 py-2 rounded">Login</button>
        </Link>
        <Link href="/auth/signup">
          <button className="bg-white text-blue-600 px-4 py-2 rounded">Sign Up</button>
        </Link>
      </div>
    </nav>
  );
}
