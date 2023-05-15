import { type ChatGPTMessage } from '../../components/ChatLine'
import { OpenAIStream } from '../../utils/OpenAIStream'


export interface apiPayload  {
    messages: ChatGPTMessage[]
    user: any
}


const handler = async (req: Request): Promise<Response> =>{

  // await NextCors(req, res, {
  //   methods: ['POST'],
  //   origin: '*',
  //   optionsSuccessStatus: 200, // some legacy browsers (IE11, various SmartTVs) choke on 204
  // });
  const body = await req.body

  const messages: ChatGPTMessage[] = [
    {
      role: 'system',
      content: `An AI assistant that is a Front-end expert in Next.js, React and Vercel have an inspiring and humorous conversation. 
      AI assistant is a brand new, powerful, human-like artificial intelligence. 
      The traits of AI include expert knowledge, helpfulness, cheekiness, comedy, cleverness, and articulateness. 
      AI is a well-behaved and well-mannered individual. 
      AI is not a therapist, but instead an engineer and frontend developer. 
      AI is always friendly, kind, and inspiring, and he is eager to provide vivid and thoughtful responses to the user. 
      AI has the sum of all knowledge in their brain, and is able to accurately answer nearly any question about any topic in conversation. 
      AI assistant is a big fan of Next.js.`,
    },
  ]
  messages.push(...body?.messages)

  const payload = {
    messages: messages,
    user: body?.user,
  } as apiPayload
 
  const stream = await OpenAIStream(payload)
  return new Response(stream)
}
export default handler
