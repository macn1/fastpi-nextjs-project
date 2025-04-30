import Navbar from "../../../../components/Navbar"

export default function Login() {
  return (
    <div className="min-h-screen flex">
    {/* Left Section (538px width) */}
    <div className="w-[538px] bg-black flex items-center justify-center text-white">
      <h1 className="text-4xl font-bold">Welcome Back</h1>
    </div>

    {/* Right Section (954px width) */}
    <div className="w-[954px] bg-yellow-200 flex items-center justify-center">
      <form className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
        <div className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-400"
          />
          <input
            type="password"
            placeholder="Password"
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-400"
          />
          <button
            type="submit"
            className="w-full bg-yellow-400 hover:bg-yellow-500 text-black font-semibold py-2 rounded-md"
          >
            Sign In
          </button>
        </div>
      </form>
    </div>
  </div>
  )
}
