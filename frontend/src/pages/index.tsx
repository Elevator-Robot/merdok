import React, { useState } from "react";
import { PageProps } from "gatsby";
import "tailwindcss/tailwind.css";

const containerStyles = "flex flex-col items-center justify-center h-screen bg-blue-200";
const chatContainerStyles = "flex flex-col bg-white rounded-lg p-4 w-60 max-h-500 overflow-y-auto";
const messageStyles = "bg-blue-500 text-white p-4 rounded-lg mb-4 self-end";
const botMessageStyles = "bg-gray-200 text-black p-4 rounded-lg mb-4 self-start";
const formStyles = "flex mt-8 w-60";
const inputStyles = "flex-grow mr-4 rounded-lg p-4";
const sendButtonStyles = "rounded-lg px-4 py-2 bg-blue-500 text-white font-bold transition-transform duration-200";
const sendButtonPressedStyles = "transform scale-95";

const IndexPage: React.FC<PageProps> = () => {
  const [messages, setMessages] = useState<{ message: string; user: string }[]>([]);
  const [chatInput, setChatInput] = useState<string>("");

  function handleChatInputSubmit(event: React.FormEvent) {
    event.preventDefault();

    if (chatInput) {
      setMessages((oldMessages) => [...oldMessages, { message: chatInput, user: "user" }]);
      setChatInput("");
    }
  }

  return (
    <main className={containerStyles}>
      <div className={chatContainerStyles}>
        {messages.map((messageObj, index) => (
          <div
            key={index}
            className={messageObj.user === "user" ? messageStyles : botMessageStyles}
          >
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
