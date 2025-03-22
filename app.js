import React, { useState } from "react";
import axios from "axios";

function App() {
  const [task, setTask] = useState("");
  const [result, setResult] = useState("");

  const sendTask = async () => {
    if (!task) {
      alert("Please enter a task!");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:5000/send_task", { task });
      setResult(response.data.result);
    } catch (error) {
      console.error("Error:", error);
      setResult("Error processing task");
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "50px" }}>
      <h1>Distributed Computing UI</h1>
      <input
        type="text"
        value={task}
        onChange={(e) => setTask(e.target.value)}
        placeholder="Enter a Python computation"
        style={{ padding: "10px", width: "300px", marginRight: "10px" }}
      />
      <button onClick={sendTask} style={{ padding: "10px 20px" }}>Submit</button>
      <h2>Result: {result}</h2>
    </div>
  );
}

export default App;
