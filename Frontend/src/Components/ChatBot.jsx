import { useState, useRef, useEffect } from "react";
import { FaPaperPlane, FaRobot } from "react-icons/fa";

const BOT_NAME = "AJET";
const PERSON_NAME = "You";

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = useRef(null);

  // Scroll to the bottom of messages
  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    // Add user message
    setMessages((prevMessages) => [
      ...prevMessages,
      { name: PERSON_NAME, side: "right", text: inputValue },
    ]);

    setInputValue("");

    try {
      // Simulate a bot response
      const response = await fetch(`/get?msg=${encodeURIComponent(inputValue)}`);
      const data = await response.text();

      // Add bot response
      setMessages((prevMessages) => [
        ...prevMessages,
        { name: BOT_NAME, side: "left", text: data },
      ]);
    } catch (error) {
      console.error("Error fetching bot response:", error);
    }
  };

  return (
    <div className="flex justify-center items-center h-screen font-sans">
      <div className="w-screen h-screen bg-white shadow-2xl rounded-lg flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-indigo-600 text-white py-4 flex items-center justify-center shadow-lg">
          <FaRobot className="text-4xl mr-3 animate-bounce" />
          <h4 className="text-3xl font-bold">AJET AI</h4>
        </header>

        {/* Messages */}
        <main className="flex-1 overflow-y-auto p-6 bg-white space-y-4">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${
                msg.side === "right" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-xs p-4 rounded-2xl shadow ${
                  msg.side === "right"
                    ? "bg-indigo-600 text-white animate-slideInRight"
                    : "bg-gray-200 text-gray-800 animate-slideInLeft"
                }`}
              >
                <div className="text-base font-semibold">{msg.name}</div>
                <div className="text-lg mt-1 leading-relaxed">{msg.text}</div>
                <div className="text-xs mt-1 text-gray-400 italic">
                  {new Date().toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </main>

        {/* Footer */}
        <form
          className="bg-gray-200 p-4 flex items-center space-x-3"
          onSubmit={handleSubmit}
        >
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type a message..."
            className="flex-1 px-4 py-3 text-lg rounded-full shadow-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <button
            type="submit"
            className="flex items-center justify-center px-5 py-3 bg-indigo-600 text-white rounded-full shadow-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <FaPaperPlane className="text-2xl animate-pulse" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatBot;
