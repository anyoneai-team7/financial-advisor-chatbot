import type { AppProps } from 'next/app'


import '@vercel/examples-ui/globals.css'

function App({ Component, pageProps }: AppProps) {


  return (
    <div
      className='bg-slate-800 font-sans h-screen overscroll-none'
    > 
      <Component {...pageProps} />
    </div>
  )
}

export default App
