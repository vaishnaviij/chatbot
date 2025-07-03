// import React, { useState, useEffect, useRef } from 'react';
// import axios from 'axios';

// const ChatInterface = ({ userId }) => {
//   const [messages, setMessages] = useState([]);
//   const [inputMessage, setInputMessage] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const messagesEndRef = useRef(null);

//   useEffect(() => {
//     const loadConversation = async () => {
//       try {
//         if (userId) {
//           const response = await axios.get(/api/user/${userId});
//           if (response.data.success && response.data.user.conversation_history) {
//             // Transform the conversation history into message format
//             const formattedMessages = response.data.user.conversation_history.flatMap(conv => [
//               { role: 'user', content: conv.user },
//               { role: 'assistant', content: conv.assistant }
//             ]);
//             setMessages(formattedMessages);
//           } else {
//             // Welcome message if no history exists
//             setMessages([{
//               role: 'assistant',
//               content: "Hello! I'm Counselmate, your AI career counselor. How can I help you with your career questions today?"
//             }]);
//           }
//         } else {
//           // Welcome message for non-logged in users
//           setMessages([{
//             role: 'assistant',
//             content: "Hello! I'm Counselmate, your AI career counselor. How can I help you with your career questions today?"
//           }]);
//         }
//       } catch (error) {
//         console.error('Error loading conversation:', error);
//         setMessages([{
//           role: 'assistant',
//           content: "Hello! I'm having trouble loading our previous conversation, but I'm still happy to help!"
//         }]);
//       }
//     };

//     loadConversation();
//   }, [userId]);

//   const scrollToBottom = () => {
//     messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
//   };

//   useEffect(() => {
//     scrollToBottom();
//   }, [messages]);

//   const handleSendMessage = async (e) => {
//     e.preventDefault();
//     if (!inputMessage.trim()) return;
  
//     const userMessage = { role: 'user', content: inputMessage };
//     const newMessages = [...messages, userMessage];
//     setMessages(newMessages);
//     setInputMessage('');
//     setIsLoading(true);
  
//     try {
//       console.log('Sending message with:', {
//         user_id: userId,
//         message: inputMessage,
//         conversation_history: newMessages
//       });
  
//       const response = await axios.post('/api/chat', {
//         user_id: userId,
//         message: inputMessage,
//         conversation_history: newMessages.map(m => ({
//           role: m.role,
//           content: m.content
//         }))
//       });
  
//       if (response.data.success && response.data.response) {
//         setMessages(prev => [...prev, { 
//           role: 'assistant', 
//           content: response.data.response 
//         }]);
//       } else {
//         throw new Error(response.data.message || 'Invalid response from server');
//       }
//     } catch (error) {
//       console.error('Chat error:', error);
//       setMessages(prev => [...prev, {
//         role: 'assistant',
//         content: "Sorry, I encountered an error. Please try again."
//       }]);
//     } finally {
//       setIsLoading(false);
//     }
//   };
//   return (
//     <div className="chat-interface">
//       <div className="messages-container">
//         {messages.map((message, index) => (
//           <div key={index} className={message ${message.role}}>
//             <div className="message-content">
//               {message.content.split('\n').map((paragraph, i) => (
//                 <p key={i}>{paragraph}</p>
//               ))}
//             </div>
//           </div>
//         ))}
//         {isLoading && (
//           <div className="message assistant">
//             <div className="message-content loading">
//               <div className="typing-indicator">
//                 <span></span>
//                 <span></span>
//                 <span></span>
//               </div>
//             </div>
//           </div>
//         )}
//         <div ref={messagesEndRef} />
//       </div>
//       <form onSubmit={handleSendMessage} className="message-form">
//         <input
//           type="text"
//           value={inputMessage}
//           onChange={(e) => setInputMessage(e.target.value)}
//           placeholder="Type your career question here..."
//           disabled={isLoading}
//         />
//         <button type="submit" disabled={isLoading || !inputMessage.trim()}>
//           Send
//         </button>
//       </form>
//     </div>
//   );
// };

// export default ChatInterface;


import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const ChatInterface = ({ user }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const loadConversation = async () => {
      try {
        if (user?.username) {
          const response = await axios.get(`/api/user/${user.username}`); // ✅ Fixed Syntax
          if (response.data.success && response.data.user.conversation_history) {
            // Convert conversation history into message format
            const formattedMessages = response.data.user.conversation_history.flatMap(conv => [
              { role: 'user', content: conv.user },
              { role: 'assistant', content: conv.assistant }
            ]);
            setMessages(formattedMessages);
          } else {
            // Default welcome message
            setMessages([
              {
                role: 'assistant',
                content: "Hello! I'm Counselmate, your AI career counselor. How can I help you today?",
              },
            ]);
          }
        } else {
          // Welcome message for guest users
          setMessages([
            {
              role: 'assistant',
              content: "Hello! I'm Counselmate, your AI career counselor. How can I assist you?",
            },
          ]);
        }
      } catch (error) {
        console.error('Error loading conversation:', error);
        setMessages([
          {
            role: 'assistant',
            content: "I'm having trouble loading previous messages, but I'm happy to help!",
          },
        ]);
      }
    };

    loadConversation();
  }, [user]);

  // Function to scroll to the bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage = { role: 'user', content: inputMessage };
    const newMessages = [...messages, userMessage];

    setMessages(newMessages);
    setInputMessage('');
    setIsLoading(true);

    try {
      console.log('Current user:', user); // Debug log

      const response = await axios.post('/api/chat', {
        user_id: user?._id || 'anonymous', // ✅ Fixed user ID handling
        message: inputMessage,
        conversation_history: newMessages, // ✅ Properly passing full conversation history
      });

      if (response.data.success) {
        setMessages(prev => [...prev, { role: 'assistant', content: response.data.response }]);
      }
    } catch (error) {
      console.error('Chat error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <div className="messages-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-content">
              {message.content.split('\n').map((paragraph, i) => (
                <p key={i}>{paragraph}</p>
              ))}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message assistant">
            <div className="message-content loading">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} className="message-form">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type your career question here..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !inputMessage.trim()}>
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;
