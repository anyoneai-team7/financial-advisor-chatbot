export type ChatGPTAgent = "user" | "system" | "assistant";

export interface ChatGPTMessage {
  role: ChatGPTAgent;
  content: string;
}

export interface apiPayload {
  user: ChatGPTAgent;
  messages: ChatGPTMessage[];
}

export async function OpenAIStream(payload: apiPayload) {
  try {
    const response = await fetch("http://localhost:5000/api/ask_model", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(payload),
    });
    if (response.ok) {
      return (await response.json()) as ChatGPTMessage;
    } else {
      throw new Error("Request failed");
    }
  } catch (error: any) {
    console.error("Error:", error.message);
    throw new Error(error.message);
  }
}
