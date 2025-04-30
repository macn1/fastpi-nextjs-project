import Navbar from "../../../../components/Navbar"


export default function Login() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-white to-lime-50 font-serif">
    <div className="flex flex-col md:flex-row shadow-xl rounded-3xl overflow-hidden max-w-5xl w-full">
      {/* Left Section */}
      <div className="bg-white p-10 md:w-1/2 flex flex-col justify-center items-start">
        <h2 className="text-3xl font-bold mb-4 text-black">
          welcome to <span className="text-black">Bookify</span>
        </h2>
        <p className="text-sm text-gray-700 mb-6">
          Dive into a world of millions of books. Discover, explore, and
          enjoy endless stories, knowledge, and adventures — all in one place.
        </p>
        <img src="/bookify.png" alt="Bookify illustration" className="w-full h-auto" />

      </div>

      
      <div className="bg-lime-50 p-10 md:w-1/2 flex flex-col justify-center">
        <h2 className="text-2xl font-semibold mb-6 text-black">
          Create Account
        </h2>
        <form className="space-y-4 text-black">
          <input
            type="text"
            placeholder="Full Name"
            className="w-full px-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-lime-400"
          />
          <div className="relative">
            <input
              type="password"
              placeholder="Pass word"
              className="w-full px-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-lime-400"
            />
            <span className="absolute right-3 top-2.5 text-gray-500 cursor-pointer">
              👁️
            </span>
          </div>
          <input
            type="email"
            placeholder="Email"
            className="w-full px-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-lime-400"
          />
          <input
            type="text"
            placeholder="Mobile Number"
            className="w-full px-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-lime-400"
          />

          <button
            type="submit"
            className="w-full bg-yellow-200 text-black font-semibold py-2 rounded-md border border-gray-600 hover:bg-yellow-300"
          >
            Register
          </button>
        </form>

        <div className="my-6 flex items-center">
          <div className="flex-grow h-px bg-gray-300"></div>
          <span className="mx-4 text-gray-500 text-sm">Or sign in with</span>
          <div className="flex-grow h-px bg-gray-300"></div>
        </div>

        <div className="flex justify-center gap-4">
          <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg" alt="Google" className="w-6 h-6" />
          <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/facebook/facebook-original.svg" alt="Facebook" className="w-6 h-6" />
          <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/x/x-original.svg" alt="X" className="w-6 h-6" />
        </div>
      </div>
    </div>
  </div>
  );
}
