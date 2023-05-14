import { Text, Page } from '@vercel/examples-ui'
import { Chat } from '../components/Chat'

function Home() {
  return (
    <Page className="flex flex-col max-w-full p-16">
      <section className="flex flex-col gap-6">
        <Text variant="h1">FINANCIAL ADVISOR CHATBOT</Text>
      </section>

      <section className="flex flex-col gap-3 py-3">
        <Text variant="h2">AI Chat Bot:</Text>
        <div>
          <Chat />
        </div>
      </section>
    </Page>
  )
}


export default Home
