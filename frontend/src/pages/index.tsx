import React, { useState } from "react"
import type { PageProps } from "gatsby"

const containerStyles: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  justifyContent: "center",
  height: "100vh",
  backgroundColor: "#F0F8FF",  // Light pastel blue
  fontFamily: "'Roboto', sans-serif",
}

const chatContainerStyles: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  backgroundColor: 'white',
  borderRadius: '10px',
  padding: '20px',
  width: '60%',
  maxHeight: '500px',
  overflowY: 'auto',
  boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)', // Added box shadow
}

const messageStyles: React.CSSProperties = {
  backgroundColor: '#0084FF',
  color: 'white',
  padding: '10px',
  borderRadius: '10px',
  margin: '10px 0',
  alignSelf: 'flex-end',
}

const botMessageStyles: React.CSSProperties = {
  ...messageStyles,
  backgroundColor: '#E5E5E5',
  color: 'black',
  alignSelf: 'flex-start',
}

const formStyles: React.CSSProperties = {
  display: "flex",
  marginTop: "32px",
  width: '60%',
}

const inputStyles: React.CSSProperties = {
  flexGrow: "1",
  marginRight: "16px",
  borderRadius: '10px',
  padding: '10px',
}

const IndexPage: React.FC<PageProps> = () => {
  const [messages, setMessages] = useState<{message: string, user: string}[]>([])
  const [chatInput, setChatInput] = useState<string>("")

  function handleChatInputSubmit(event: React.FormEvent) {
    event.preventDefault()

    if (chatInput) {
      setMessages((oldMessages) => [...oldMessages, {message: chatInput, user: 'user'}])
      setChatInput("")
    }
  }

  return (
    <main style={containerStyles}>
      <div style={chatContainerStyles}>
        {messages.map((messageObj, index) => (
          <div key={index} style={messageObj.user === 'user' ? messageStyles : botMessageStyles}>{messageObj.message}</div>
        ))}
      </div>

      <form onSubmit={handleChatInputSubmit} style={formStyles}>
        <input
          type="text"
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          style={inputStyles}
        />
        <input type="submit" value="Send" />
      </form>
    </main>
  )
}

export default IndexPage
