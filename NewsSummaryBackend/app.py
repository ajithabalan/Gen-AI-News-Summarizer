
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_community.utilities import SerpAPIWrapper
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# ✅ Load API keys securely
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# ✅ Initialize Flask App
app = Flask(__name__)
CORS(app)

# ✅ Web Search Tool (Using SerpAPI)
search_tool = Tool(
    name="web_search",
    func=SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY).run,
    description="Fetches the latest news from the web."
)

# ✅ Hugging Face AI Summarizer
def hf_generate(prompt):
    """Generates text using Hugging Face LLM."""
    try:
        client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1", token=HUGGINGFACE_API_KEY)
        response = client.chat_completion(messages=[{"role": "user", "content": prompt}])
        return response.get("choices", [{}])[0].get("message", {}).get("content", "No response.")
    except Exception as e:
        return f"Error in LLM: {str(e)}"

summarization_tool = Tool(
    name="ai_summarizer",
    func=hf_generate,
    description="Generates summaries using Hugging Face model."
)

# ✅ FIX: Use Hugging Face as the LLM
llm = Tool(name="hf_llm", func=hf_generate, description="Hugging Face LLM for text generation")

# ✅ Initialize LangChain Agent with memory
memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools=[search_tool, summarization_tool],
    llm=llm,  # ✅ FIXED: Using Hugging Face LLM
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
)

@app.route("/get-news", methods=["POST"])
def get_news():
    """Fetch and summarize latest news on a given topic."""
    data = request.json
    topic = data.get("topic", "")

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    try:
        # ✅ Step 1: Search for news
        news_results = search_tool.run(topic)
        if not news_results:
            return jsonify({"error": "No news found."}), 404

        # ✅ Step 2: Summarize news using Hugging Face
        summary = hf_generate(f"Summarize this: {news_results}")

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
