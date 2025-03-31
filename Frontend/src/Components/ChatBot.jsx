import { useState, useRef, useEffect } from "react";
import { FaPaperPlane, FaRobot } from "react-icons/fa";

const BOT_NAME = "AJET";
const PERSON_NAME = "You";

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

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

  // Focus input on component mount
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    // Add user message
    setMessages((prevMessages) => [
      ...prevMessages,
      { name: PERSON_NAME, side: "right", text: inputValue, time: new Date() },
    ]);

    setInputValue("");
    setIsTyping(true);

    try {
      // Simulate a bot response
      const response = await fetch(`/get?msg=${encodeURIComponent(inputValue)}`);
      const data = await response.text();

      // Add a slight delay to simulate thinking
      setTimeout(() => {
        // Add bot response
        setMessages((prevMessages) => [
          ...prevMessages,
          { name: BOT_NAME, side: "left", text: data, time: new Date() },
        ]);
        setIsTyping(false);
      }, 1000);
    } catch (error) {
      console.error("Error fetching bot response:", error);
      setIsTyping(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-indigo-100 to-purple-100 p-4 font-sans">
      <div className="w-full max-w-4xl h-[85vh] bg-white shadow-2xl rounded-2xl flex flex-col overflow-hidden border border-indigo-100">
        {/* Header */}
        <header className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-5 flex items-center justify-center shadow-lg">
          <div className="relative">
            <FaRobot className="text-4xl mr-3" />
            <span className="absolute bottom-0 right-2 w-3 h-3 bg-green-400 rounded-full animate-pulse"></span>
          </div>
          <h4 className="text-3xl font-bold">
            AJET <span className="text-indigo-200">AI</span>
          </h4>
        </header>

        {/* Messages */}
        <main className="flex-1 overflow-y-auto p-6 bg-gradient-to-b from-white to-indigo-50 space-y-4">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full flex-col text-center">
              <FaRobot className="text-6xl text-indigo-300 mb-4 animate-bounce" />
              <h3 className="text-2xl font-semibold text-indigo-600 mb-2">Welcome to AJET AI</h3>
              <p className="text-gray-500 max-w-md">Type a message below to start chatting with our intelligent assistant.</p>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.side === "right" ? "justify-end" : "justify-start"
                } animate-fadeIn`}
              >
                {msg.side === "left" && (
                  <div className="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-white mr-2 flex-shrink-0 shadow-md">
                    <FaRobot />
                  </div>
                )}
                <div
                  className={`max-w-md p-4 rounded-2xl shadow-md ${
                    msg.side === "right"
                      ? "bg-gradient-to-r from-indigo-600 to-indigo-700 text-white rounded-tr-none animate-slideInRight"
                      : "bg-white text-gray-800 rounded-tl-none animate-slideInLeft border border-indigo-100"
                  }`}
                >
                  <div className="text-sm font-semibold mb-1">{msg.name}</div>
                  <div className="text-lg leading-relaxed whitespace-pre-wrap">{msg.text}</div>
                  <div className={`text-xs mt-2 italic ${msg.side === "right" ? "text-indigo-200" : "text-gray-400"}`}>
                    {msg.time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
                {msg.side === "right" && (
                  <div className="w-10 h-10 rounded-full bg-indigo-500 flex items-center justify-center text-white ml-2 flex-shrink-0 shadow-md">
                    {PERSON_NAME.charAt(0)}
                  </div>
                )}
              </div>
            ))
          )}
          {isTyping && (
            <div className="flex justify-start animate-fadeIn">
              <div className="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-white mr-2 flex-shrink-0 shadow-md">
                <FaRobot />
              </div>
              <div className="bg-white p-4 rounded-2xl shadow-md rounded-tl-none border border-indigo-100">
                <div className="flex space-x-2">
                  <div className="w-3 h-3 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></div>
                  <div className="w-3 h-3 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></div>
                  <div className="w-3 h-3 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </main>

        {/* Footer */}
        <form
          className="bg-white p-4 flex items-center space-x-3 border-t border-indigo-100"
          onSubmit={handleSubmit}
        >
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type a message..."
              className="flex-1 px-5 py-4 text-lg rounded-full bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all duration-300 shadow-inner"
            />
                      <button
              type="submit"
              disabled={!inputValue.trim() || isTyping}
              className={`flex items-center justify-center w-14 h-14 rounded-full shadow-lg transition-all duration-300 ${
                inputValue.trim() && !isTyping
                  ? "bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 transform hover:scale-105"
                  : "bg-gray-200 text-gray-400 cursor-not-allowed"
              }`}
            >
              <FaPaperPlane className="text-xl" />
            </button>
            
            </form>
          </div>
        </div>
      );
    };

export default ChatBot;