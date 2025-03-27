import React, { useState } from "react";
import axios from "axios";
import NewsForm from "./components/NewsForm";
import NewsSummary from "./components/NewsSummary";
import "./App.css"; // Import CSS file

const App = () => {
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchNews = async (topic) => {
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/get-news", {
        topic,
      });
      setSummary(response.data.summary);
    } catch (error) {
      console.error("Error fetching news:", error);
      setSummary("Failed to fetch news summary.");
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <h1 className="header">AI News Summarizer</h1>
      <NewsForm fetchNews={fetchNews} />
      {loading ? <p>Loading...</p> : <NewsSummary summary={summary} />}
    </div>
  );
};

export default App;
