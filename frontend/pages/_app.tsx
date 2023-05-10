import type { AppProps } from 'next/app'


import '@vercel/examples-ui/globals.css'

function App({ Component, pageProps }: AppProps) {


  return (
    <div
      max-w-full
    >
      <Component {...pageProps} />

    </div>
  )
}

export default App
