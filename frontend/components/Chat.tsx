import { useEffect, useState } from 'react'
import { Button } from './Button'
import { type ChatGPTMessage, ChatLine, LoadingChatLine } from './ChatLine'
import { useCookies } from 'react-cookie'

import { OpenAIStream, apiPayload } from '../utils/OpenAIStream'


const COOKIE_NAME = 'user_chat_finacial'

// default first message to display in UI (not necessary to define the prompt)
export const initialMessages: ChatGPTMessage[] = [
  {
    role: 'assistant',
    content: 'Hi! I am a financial AI assistant. Ask me anything!',
  },
]

const InputMessage = ({ input, setInput, sendMessage, initialChat }: any) => (
  <div className="mt-6 flex clear-both pb-6">
    <input
      type="text"
      aria-label="chat input"
      required
      className="min-w-0 flex-auto appearance-none rounded-md border border-zinc-900/10 bg-white px-3 py-[calc(theme(spacing.2)-1px)] shadow-md shadow-zinc-800/5 placeholder:text-zinc-400 focus:border-teal-500 focus:outline-none focus:ring-4 focus:ring-teal-500/10 sm:text-sm"
      value={input}
      onKeyDown={(e) => {
        if (e.key === 'Enter') {
          sendMessage(input)
          setInput('')
        }
      }}
      onChange={(e) => {
        setInput(e.target.value)
      }}
    />
    <Button
      type="submit"
      className="ml-4 flex-none"
      onClick={() => {
        sendMessage(input)
        setInput('')
      }}
    >
      Say
    </Button>
    <Button
      className="ml-4 flex-none"
      onClick = {initialChat}
    >
      Delete
    </Button>
  </div>
)

export function Chat() {
  const [messages, setMessages] = useState<ChatGPTMessage[]>(initialMessages)
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [cookie, setCookie] = useCookies([COOKIE_NAME])

  useEffect(() => {
    if (!cookie[COOKIE_NAME]) {
      // generate a semi random short id
      const randomId = Math.random().toString(36).substring(7)
      setCookie(COOKIE_NAME, randomId)
    }
  }, [cookie, setCookie])

  const initialChat = () => {
    setMessages(initialMessages)
    const randomId = Math.random().toString(36).substring(7)
    setCookie(COOKIE_NAME, randomId)
  }
  // send message to API /api/chat endpoint
  const sendMessage = async (message: string) => {
    setLoading(true)
    const newMessages = [
      ...messages,
      { role: 'user', content: message } as ChatGPTMessage,
    ]
    setMessages(newMessages)
    const last10messages = newMessages.slice(-10) // remember last 10 messages

    const payload = {
      messages: last10messages,
      user: cookie[COOKIE_NAME],
    } as apiPayload

    const data = await OpenAIStream(payload)

    if (!data) {
      return
    }

    setMessages([
      ...newMessages,
      { role: 'assistant', content: data.content } as ChatGPTMessage,
    ])

    setLoading(false)
  }

  return (
    
      <div className='h-full p-16'>
        
        {messages.map(({ content, role }, index) => (
          <ChatLine key={index} role={role} content={content} />
        ))}

        {loading && <LoadingChatLine />}

        {messages.length < 2 && (
          <span className="mx-auto flex flex-grow text-gray-600 clear-both">
            Type a message to start the conversation
          </span>
        )}
 
        <InputMessage
              input={input}
              setInput={setInput}
              sendMessage={sendMessage}
              initialChat={initialChat}
        />
                   
        
      </div>
    
  )
}
