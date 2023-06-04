import React, { useState, useEffect } from "react";
import { PageProps } from "gatsby";

const containerStyles = "flex flex-col items-center justify-center h-screen p-16 bg-blue-200";
const chatContainerStyles = "bg-white rounded-lg p-4 w-full max-w-xl h-80 overflow-y-auto mb-8 shadow-lg";
const messageContainerStyles = "flex justify-start";
const messageStyles = "bg-blue-500 text-white p-4 rounded-lg mb-4 self-start transition-transform duration-300 transform hover:scale-105";
const botMessageStyles = "bg-gray-200 text-black p-4 rounded-lg mb-4 self-start";
const formStyles = "flex flex-col w-full max-w-xl";
const inputStyles = "rounded-lg p-4 mb-4";
const sendButtonStyles = "rounded-lg px-4 py-2 bg-blue-500 text-white font-bold transition-transform duration-200";
const sendButtonPressedStyles = "transform scale-95";

const IndexPage: React.FC<PageProps> = () => {
  const [messages, setMessages] = useState<{ message: string; user: string }[]>([]);
  const [chatInput, setChatInput] = useState<string>("");

  useEffect(() => {
    const chatContainer = document.getElementById("chatContainer");
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }, [messages]);

  function handleChatInputSubmit(event: React.FormEvent) {
    event.preventDefault();

    if (chatInput) {
      setMessages((oldMessages) => [...oldMessages, { message: chatInput, user: "user" }]);
      setChatInput("");
    }
  }

  return (
    <main className={containerStyles}>
      <div className={`border border-gray-300 p-2 rounded-lg mb-4 ${chatContainerStyles}`} id="chatContainer">
        {messages.map((messageObj, index) => (
          <div key={index} className={messageObj.user === "user" ? `${messageContainerStyles} ${messageStyles}` : botMessageStyles}>
            {messageObj.message}
          </div>
        ))}
      </div>

      <form onSubmit={handleChatInputSubmit} className={formStyles}>
        <input
          type="text"
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          className={inputStyles}
        />
        <button
          type="submit"
          className={sendButtonStyles}
          onClick={() => console.log("Button pressed")} // Replace with your logic
        >
          Send
        </button>
      </form>
    </main>
  );
};

export default IndexPage;
