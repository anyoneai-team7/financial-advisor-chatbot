import {
  createParser,
  ParsedEvent,
  ReconnectInterval,
} from 'eventsource-parser'
import { apiPayload } from '../pages/api/chat'

export type ChatGPTAgent = 'user' | 'system' | 'assistant'

export interface ChatGPTMessage {
  role: ChatGPTAgent
  content: string
}


export async function OpenAIStream(payload: apiPayload) {
  const encoder = new TextEncoder()
  const decoder = new TextDecoder()

  let counter = 0

  console.log(JSON.stringify(payload))
  const res = await fetch('http://localhost:5000/api/ask_gpt3', {
    headers: {
      'Content-Type': 'application/json',
    },
    method: 'POST',
    body: JSON.stringify(payload),
  })

  console.log(res.body)
  
  const stream = new ReadableStream({
    async start(controller) {
      // callback
      function onParse(event: ParsedEvent | ReconnectInterval) {
        console.log("here")
        if (event.type === 'event') {
          const data = event.data
          // https://beta.openai.com/docs/api-reference/completions/create#completions/create-stream
          if (data === '[DONE]') {
            console.log('DONE')
            controller.close()
            return
          }
          try {
            console.log(data)
            const json = JSON.parse(data)
            const text = json.content || ''
            if (counter < 2 && (text).length) {
              // this is a prefix character (i.e., "\n\n"), do nothing
              return
            }
            const queue = encoder.encode(text)
            controller.enqueue(queue)
            counter++
          } catch (e) {
            // maybe parse error
            controller.error(e)
          }
        }
      }

      // stream response (SSE) from OpenAI may be fragmented into multiple chunks
      // this ensures we properly read chunks and invoke an event for each SSE event stream
      const parser = createParser(onParse)
      for await (const chunk of res.body as any) {
        parser.feed(decoder.decode(chunk))
      }
    },
  })

  return stream

}
