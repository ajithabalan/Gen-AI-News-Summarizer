import React, { useState } from "react";

const NewsForm = ({ fetchNews }) => {
  const [topic, setTopic] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (topic.trim()) {
      fetchNews(topic);
    } else {
      alert("Please enter a topic.");
    }
  };

  return (
    <div className="card">
      <h2>Enter a Topic</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          className="input-field"
          placeholder="e.g., AI in Healthcare"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />
        <button type="submit" className="button">
          Get News Summary
        </button>
      </form>
    </div>
  );
};

export default NewsForm;
