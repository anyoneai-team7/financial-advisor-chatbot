import { Chat } from '../../components/Chat'
import { motion} from "framer-motion";


function ChatAI() {
  return (
    <div className='h-full'>
      <motion.div
      className="box"
      initial={{ opacity: 0, scale: 0.5 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{
        duration: 0.8,
        delay: 0.5,
        ease: [0, 0.71, 0.2, 1.01]
      }}
      >
          <header className='bg-cyan-800 w-full h-20 shadow-inner flex items-center'>
              <img className="pl-16 h-20 p-2" src="https://i.ibb.co/6W2b23s/anyone.png" alt="logo"/> 
              <h1 className='justify-self-center text-white'>FINANCIAL ADVISOR CHATBOT</h1>
          </header>
      </motion.div>
      <motion.div
      className="box h-5/6 overflow-auto snap-end"
      initial={{ opacity: 0, scale: 0.5 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{
        duration: 0.8,
        delay: 1,
        ease: [0, 0.71, 0.2, 1.01]
      }}
      >     
        
        <Chat />

      </motion.div>
    
      
    </div>
    
    
  )
}

export default ChatAI