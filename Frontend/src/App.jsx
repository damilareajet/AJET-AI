// import { useState } from "react";
import ChatBot from "./Components/ChatBot";
// import Register from "./Components/Register";
// import Login from "./Components/Login";

const App = () => {
  // const [user, setUser] = useState(null); // This holds the logged-in user's data
  // const [view, setView] = useState("login"); // Determines which view to show (login/register/chat)

  // const handleLogin = (username) => {
  //   setUser(username); // Save the username on successful login
  //   setView("chat"); // Show the chatbot view after login
  // };

  // const handleRegister = (username) => {
  //   setUser(username); // Register the user and store the username
  //   setView("chat"); // Show the chatbot view after successful registration
  // };

  return (
    <div className="App">
      {/* {view === "login" && <Login onLogin={handleLogin} onSwitch={() => setView("register")} />}
      {view === "register" && <Register onRegister={handleRegister} onSwitch={() => setView("login")} />}
      {view === "chat" && <ChatBot user={user} />} Pass the user to the ChatBot */}
      <ChatBot/>
    </div>
  );
};

export default App;
