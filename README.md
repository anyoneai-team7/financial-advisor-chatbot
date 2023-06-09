# Financial Advisor Chatbot

## Final project for the degree of ML engineer at [Anyone AI](https://www.linkedin.com/school/anyone-ai/) bootcamp.

### Team members:

+ [Ciro Villafraz](https://www.linkedin.com/in/ciro-villafraz/)

+ [Alexander Mulet de los Reyes](https://www.linkedin.com/in/muletdelosreyes89)

+ [Sebastian Lugo](https://www.linkedin.com/in/jhoan-sebastian-lugo-ruiz-8577b01b6/)

+ [Alejandro León](https://www.linkedin.com/in/jose-alejandro-leon-andrade-88249ab2)

### Mentor:
+ [Claudio A. Gauna](https://www.linkedin.com/in/claudio-andres-gauna-2b697b97/)

# ABSTRACT
In this project, we created a chatbot acting as a financial advisor enable to answer questions related to public companies listed in NASDAQ. The bot uses a conversational Agent to coordinate chains of thoughts inserted in ChatGPT through its API, and has access to a database with around ~10.000 public financial documents and news from internet sources to provide users with reliable and accurate answers. All documents were preprocessed and indexed in an Elastiserach document store, and the search is done with the sparse retriever BM25 paired with a Sentence Transformers Ranker. BM25 is fast and lightweight, however, it is not sensitive to word order, nither to the semantics of the text but rather treats text as a bag of words. By placing a Ranker afterward we were able to offset this weakness and have a better-sorted list of relevant documents. The model was tested with **50** questions related to 10 different companies, obtaining an effectiveness of **82%** of correct answers, **12%** of not found answers and only **6%** of incorrect answers. The incorrect answers are all associated with obtaining contexts related to the user's question but from different periods than the one requested in the query. In addition, most of the answers not found or wrongly answered could be solved by slightly modifying the question asked or providing more details to the bot. 

# Goal
The main goal of this project is to provide users with a platform in which they can interact with a Chatbot assistant and make questions about finance over NASDAQ companies. To develop the solution we first need to extract all the text data from the provided dataset and store it in a platform such as Elastisearch, which would allow us to subsequently perform text searches to retrieve the results most similar to the user's question. We then have to plug in a Generative Model like [ChatGPT](https://openai.com/blog/chatgpt) to take the retrieved text chunks and create a final answer for the user. The user should be provided with a friendly chat interface and an API to establish communication between the UI and the model. 

### Required tasks by order:

- Exploratory Dataset Analysis (EDA)

- Data pre-processing and data preparation

- Storing the documents' text data  in the database or framework

- Make a system capable of taking as input a question, searching on the documents database, and building the final answer using the documents' text and a generative model that puts it all together.

- An API (Flask or FastAPI) that allows users to ask questions to the chatbot and receive answers

- A simple UI having an interface similar to ChatGPT

- Present results and a demo of the system running

- Make everything containerized using Docker. 

# System architecture
In order to enable modular development, scalability, and flexibility we have created a microservices architecture with six services containerized with docker and docker-compose (*Figure 1*):
```
├── etl -> Used to extract, transform and load the documents into elastiserach
├── elastisearch -> Used to store, search, and analyze all indexed documents
├── frontend -> User interface (UI) so that users can interact directly with the system
├── api -> Used to implement the communication interface between the UI and the model
├── redis -> Used as a message broker, inside has a task queue and a hash table.
├── generative_retriever -> It is the code that implements the retriver-generative model, it gets the 
                            user query from Redis, active an Agent that use a retriever tool to get   
                            information, and returns the answers.
```
*Figure 1*. System architecture. 
![System_architecture](https://i.imgur.com/T8tjHg2.png)

## Full project structure

```
├── etl            # Scripts to connects to an AWS bucket, then downloads, preprocesses, and indexes documents in Elastiserach.
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── main.py
│   └── src
│   │   ├── extract.py
│   │   ├── load.py
│   │   ├── transform.py
│   │   └── utils
│   │       └── text_normalizer.py
│   └── tests
│       └── test_etl.py
├── eda             # Scripts to do the exploratory data analysis of the collection of text used
│   ├── eda.ipynb
│   ├── contractions.py
│   ├── download_sample.py
│   ├── text_normalizer.py
│   └── visualization.py
├── api             # Scripts used to create the flask API that allows the communication between the UI and the model
│   ├── Dockerfile
│   ├── app.py
│   ├── middleware.py
│   ├── views.py
│   ├── settings.py
│   └── tests
│       └── test_api.py
├── frontend        # Scrpits for the frontend using Next.js
│   ├── Dockerfile
│   ├── next-env.d.ts
│   ├── package-lock.json
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── turbo.json
│   └── components
│   │   ├── Button.tsx
│   │   ├── Chat.tsx
│   │   ├── ChatLine.tsx
│   │   └── Login.tsx
│   └── pages
│   │   ├── _app.tsx
│   │   ├── index.tsx
│   │   └── chatAI
│   │       └── index.tsx
│   └── public
│   │   ├── anyone.png
│   │   └── favicon.ico
│   └── utils
│       └── OpenAIStream.ts
├── generative_retriever   # Scripts for the generative-retriever model the main frameworks used here are Haystacks and Langchain
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── main.py
│   ├── qa_dataset.json
│   └── src
│   │   ├── lang_agent.py
│   │   ├── retriever.py
│   │   ├── settings.py
│   │   └── utils.py
│   └── tests
│       └── test_agent.py
├── tests                # Test the integration of the entire system
│   └── test_integration.py
├── .env
├── .gitignore
├── docker-compose.yml
├── package-lock.json
├── README.md
└── LICENSE

```

# ETL
ETL is the process of Extraction, transformation, and loading of the data. We have used the library [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) to get documents from an AWS bucket. All documents are in pdf format, these are downloaded and stored in folders by companies. [Haystacks](https://haystack.deepset.ai/) library is first used to transform each pdf into text and then to preprocess, split them into chunks and index in an Elastiserach document store.

# API
We have used [Flask](https://flask.palletsprojects.com/en/2.3.x/) to build the API. Flask is a lightweight and flexible web framework for Python with the necessary tools and libraries to build web applications, APIs, and other related services. The Flask API enables the interconnection between the users' web interface and the generative retrieval model.  On the other hand, [Redis](https://redis.io/docs/) is an open source in-memory data structure store that can be used as a database, cache and message broker. The API code is able to receive requests (questions to the bot) from the user, put them in a redis queue, wait for the model to return the answer in a redis hash table and send it to the user interface as a response from the bot. This is an appropriate approach to offer a service as requested.

# Generative-retriever model
The generative-retriever model is referred to as the code that receives the user query, retrieves relevant information, and generates an appropriate answer for the user.
### Agent
The proposed model is basically the [chat-conversational-react-description](https://python.langchain.com/en/latest/modules/agents/agents/examples/chat_conversation_agent.html) Agent of [LangChain](https://python.langchain.com/en/latest/index.html). An Agent is a very versatile, prompt-based component that uses a large language model (LLM) and employs reasoning to answer complex questions beyond the capabilities of extractive or generative question answering. The agent has information on the set of tools that can access, when the Agent receives a query, it forms a plan of action consisting of steps it has to complete. It then starts with choosing the right tool and proceeds using the output from each tool as input for the next. It uses the tools in a loop until it reaches the final answer. The chat-conversational-react-description Agent is optimized for conversation settings. It uses the [ReAct](https://ai.googleblog.com/2022/11/react-synergizing-reasoning-and-acting.html) framework to decide which tool to use, and uses memory to remember the previous conversation interactions. The LLM used by the Agent is [gpt-3.5-turbo](https://platform.openai.com/docs/guides/gpt) which we access through its API.
### Tool
Our agent is provided with a single tool consisting of a customized [Retrieval Question/Answering](https://python.langchain.com/en/latest/modules/chains/index_examples/vector_db_qa.html) (*Figure 2*). This tool receives the **Input Action** generated by the agent. It then performs a search that returns the most relevant document chunks stored in the Elastisearch using [BM25](https://docs.haystack.deepset.ai/docs/retriever), then further reduces the output by ranking these documents using a Cross-encoder-sentence-transformer model ([ms-frame-MiniLM-L-12-v2](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-12-v2)). Finally, the tool uses gpt-3.5-turbo to parse the obtained context and generate an observation as the output of the tool. 

From the observation the agent will generate a new thought, deciding whether to use the tool again or proceed to give a response to the user. 

*Figure 2.* Agent's processes cycle

![Agent](https://i.imgur.com/3yuvcDQ.png)

### The output from the Agent:

```
Query: What is Inogen Inc's total gross margin percentage for 2020? 

> Entering new AgentExecutor chain…

I need to search for Inogen Inc gross margin percentage 2020.

Action: RetrieverQA 

Action Input: Inogen Inc gross margin percentage 2020

Observation: Inogen Inc's overall gross margin percentage for the year ended June 30, 2020 was 1.226% as stated in Document[1]. 

Thought:I now know the final answer

Final Answer: Inogen Inc's total gross margin percentage for 2020 was 1.226%

> Finished chain
```


# User Interface
The graphical interface consists of two main views, the login and the chat (Figure 3). Each section of the page is divided into components to improve performance and section rendering. The Next.js framework is implemented, using TypeScript with JavaScript and utilizing Tailwind CSS for styling.

 *Figure 3*. User interface
![User interface](https://i.imgur.com/7tHuTOs.jpg)

# Instalation
The project is able to build all images and run containers using docker-compose. 
```
bash
$ docker-compose up -d
```
First, make sure to create and set values to environment variables in a file .env located at the root:
```
UID=
OPENAI_API_KEY=
AWS_SECRET_KEY=
AWS_ACCESS_KEY=
ELASTICSEARCH_HOST=
TRANSFORMERS_CACHE="/app/.cache"
GUNICORN_TIMEOUT=
```
After building and running containers you could use the demo through your *'localhost'* at port *'3000'* using any web browser: [http://localhost:3000/](http://localhost:3000/)

To stop the services:
```
$ docker-compose down
```
# Tests

We provide unit tests along with the project that you can run and check from your side the code meets the minimum requirements of correctness needed to approve. To run just execute:

### 1. Modules

We make use of [multi-stage docker builds](https://docs.docker.com/develop/develop-images/multistage-build/) so we can have into the same Dockerfile environments for testing and also for deploying our service.

#### 1.1. Api
Run:
```
$ cd api/
$ docker build --build-arg="UID=$(id -u)" -t flask_api_test --progress=plain --target test .
```

#### 1.2. Etl
Run:
```
$ cd etl/
$ docker build --build-arg="UID=$(id -u)" -t etl-service_test --progress=plain --target test .
```

#### 1.3. Model (generative_retriever)
Run:
```
$ cd generative_retriever/
$ docker build -t model_test --progress=plain --build-arg "UID=$(id -u)" --target test .  
```
If you run elascticsearch with docker compose, run this after building the image run
```
$ docker run --env-file ../.env --network="financial-advisor-chatbot_default" model_test
```


# Resources
- [Lil'Log: How to Build an Open-Domain Question Answering System?](https://lilianweng.github.io/posts/2020-10-29-odqa/)

- [Haystack Tutorial: Build Your First Question Answering System](https://haystack.deepset.ai/tutorials/01_basic_qa_pipeline)

- [Haystack Tutorial: Build a Scalable Question Answering System](https://haystack.deepset.ai/tutorials/03_scalable_qa_system)

- [Haystack Tutorial: Preprocessing Your Documents](https://haystack.deepset.ai/tutorials/08_preprocessing)

- [Haystack Tutorial: Generative QA with Retrieval-Augmented Generation](https://haystack.deepset.ai/tutorials/07_rag_generator)

- [OpenAI API](https://openai.com/blog/openai-api)

- [Papers with code: "Generative Question Answering"](https://paperswithcode.com/task/generative-question-answering/codeless)

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://ai.googleblog.com/2022/11/react-synergizing-reasoning-and-acting.html)

- [Conversation Agent (for Chat Models) in LangChain](https://python.langchain.com/en/latest/modules/agents/agents/examples/chat_conversation_agent.html)


