import { useState } from "react";
import PropTypes from "prop-types"; // Import PropTypes

const Login = ({ onLogin, onSwitch }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // For simplicity, we're skipping backend validation.
    if (username && password) {
      onLogin(username); // Log the user in if form is valid
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-pink-300 via-purple-300 to-indigo-300">
      <div className="bg-white p-8 rounded-lg shadow-lg w-80">
        <h2 className="text-3xl text-center text-indigo-500 mb-6">Login</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
            className="w-full p-3 mb-4 border border-gray-300 rounded-lg"
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="w-full p-3 mb-6 border border-gray-300 rounded-lg"
          />
          <button type="submit" className="w-full bg-indigo-500 text-white py-3 rounded-lg hover:bg-indigo-600">
            Log In
          </button>
        </form>
        <p className="mt-4 text-center">
          Don't have an account?{" "}
          <span
            onClick={onSwitch}
            className="text-indigo-500 cursor-pointer hover:underline"
          >
            Register here
          </span>
        </p>
      </div>
    </div>
  );
};

// Prop validation using PropTypes
Login.propTypes = {
  onLogin: PropTypes.func.isRequired,  // onLogin should be a function and is required
  onSwitch: PropTypes.func.isRequired, // onSwitch should be a function and is required
};

export default Login;
