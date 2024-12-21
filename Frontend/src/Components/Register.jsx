import { useState } from "react";
import PropTypes from "prop-types"; // Import PropTypes

const Register = ({ onRegister, onSwitch }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    if (username && password) {
      onRegister(username); // Register the user
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-pink-300 via-purple-300 to-indigo-300">
      <div className="bg-white p-8 rounded-lg shadow-lg w-80">
        <h2 className="text-3xl text-center text-indigo-500 mb-6">Register</h2>
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
            className="w-full p-3 mb-4 border border-gray-300 rounded-lg"
          />
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm Password"
            className="w-full p-3 mb-6 border border-gray-300 rounded-lg"
          />
          <button type="submit" className="w-full bg-indigo-500 text-white py-3 rounded-lg hover:bg-indigo-600">
            Register
          </button>
        </form>
        <p className="mt-4 text-center">
          Already have an account?{" "}
          <span
            onClick={onSwitch}
            className="text-indigo-500 cursor-pointer hover:underline"
          >
            Login here
          </span>
        </p>
      </div>
    </div>
  );
};

// Prop validation using PropTypes
Register.propTypes = {
  onRegister: PropTypes.func.isRequired, // onRegister should be a function and is required
  onSwitch: PropTypes.func.isRequired,  // onSwitch should be a function and is required
};

export default Register;
