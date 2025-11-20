import { useState, useRef, useEffect } from 'react'
import axios from 'axios'

function ChatInterface({ 
  currentPresentation, 
  presentationStructure, 
  setCurrentPresentation,
  setPresentationStructure,
  setLoading 
}) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I can help you modify your presentation. Try commands like:\n• "Add summary slide for conclusion"\n• "Change to academic style"\n• "Add overview slide at the beginning"\n• "Remove slide 3"'
    }
  ])
  const [input, setInput] = useState('')
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim()) return

    if (!currentPresentation) {
      setMessages(prev => [...prev, 
        { role: 'user', content: input },
        { role: 'assistant', content: 'Please generate a presentation first before using chat commands.' }
      ])
      setInput('')
      return
    }


    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')

    setLoading(true)
    try {
      const response = await axios.post('/api/chat', {
        command: input,
        current_structure: presentationStructure,
        presentation_path: currentPresentation.output_path
      })

      const modification = response.data.modification
      const assistantMessage = {
        role: 'assistant',
        content: modification.explanation
      }

      setMessages(prev => [...prev, assistantMessage])

      if (response.data.updated_structure) {
        setPresentationStructure(response.data.updated_structure)
      }

      if (response.data.output_path) {
        setCurrentPresentation(prev => ({
          ...prev,
          output_path: response.data.output_path,
          filename: response.data.filename
        }))
      }

    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: 'Error processing command: ' + (error.response?.data?.error || error.message)
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 h-[600px] flex flex-col">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Chat Assistant</h2>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto mb-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                message.role === 'user'
                  ? 'bg-primary text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>


      <div className="flex space-x-2">
        <input
          type="text"
          className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
          placeholder="Type a command... (e.g., 'Add summary slide')"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={!currentPresentation}
        />
        <button
          className="bg-primary hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-md transition duration-200 disabled:bg-gray-300 disabled:cursor-not-allowed"
          onClick={handleSend}
          disabled={!currentPresentation || !input.trim()}
        >
          Send
        </button>
      </div>

      {!currentPresentation && (
        <p className="text-xs text-gray-500 mt-2 text-center">
          Generate a presentation first to use chat commands
        </p>
      )}
    </div>
  )
}

export default ChatInterface
