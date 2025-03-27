import React from "react";

const NewsSummary = ({ summary }) => {
  return (
    <div className="summary-box">
      <h2>AI-Generated Summary</h2>
      {summary ? (
        <ul>
          {summary.split("\n").map((point, index) => (
            <li key={index}>{point}</li>
          ))}
        </ul>
      ) : (
        <p>No summary available.</p>
      )}
    </div>
  );
};

export default NewsSummary;
