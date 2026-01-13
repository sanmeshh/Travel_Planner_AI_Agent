import { useState } from "react";
import axios from "axios";

export default function App() {
  const [sessionId, setSessionId] = useState("trip1");
  const [userId, setUserId] = useState("u1");

  const [form, setForm] = useState({
    budget_min: "",
    budget_max: "",
    location: "",
    destination_type: "",
    activities: "",
    dates: ""
  });

  const [status, setStatus] = useState("");
  const [final, setFinal] = useState(null);

  const update = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const submit = async () => {
    await axios.post("http://127.0.0.1:8000/submit_preferences", {
      ...form,
      activities: form.activities.split(",").map(a => a.trim())
    }, {
      params: { session_id: sessionId, user_id: userId }
    });
    setStatus("Preferences saved");
  };

  const ready = async () => {
    const res = await axios.post("http://127.0.0.1:8000/ready", null, {
      params: { session_id: sessionId, user_id: userId }
    });
    if (res.data.status === "final") {
      setFinal(res.data.result);
      setStatus("Final decision ready");
    } else {
      setStatus("Waiting for other users...");
    }
  };

  return (
    <div style={{ maxWidth: 700, margin: "auto", padding: 20, fontFamily: "Arial" }}>
      <h2>🧠 AI Group Travel Planner</h2>

      <div style={{ display: "flex", gap: 10, marginBottom: 10 }}>
        <input placeholder="Session ID" value={sessionId} onChange={e => setSessionId(e.target.value)} />
        <input placeholder="User ID" value={userId} onChange={e => setUserId(e.target.value)} />
      </div>

      <h3>My Preferences</h3>

      <input name="budget_min" placeholder="Min Budget" onChange={update} />
      <input name="budget_max" placeholder="Max Budget" onChange={update} />
      <input name="location" placeholder="Preferred Location" onChange={update} />
      <input name="destination_type" placeholder="Destination Type (beach, hill, city)" onChange={update} />
      <input name="activities" placeholder="Activities (comma separated)" onChange={update} />
      <input name="dates" placeholder="Dates" onChange={update} />

      <div style={{ marginTop: 10 }}>
        <button onClick={submit}>Submit Preferences</button>
        <button onClick={ready} style={{ marginLeft: 10 }}>Mark Ready</button>
      </div>

      <p>{status}</p>

      {final && (
        <div style={{ marginTop: 20, padding: 15, border: "1px solid green", borderRadius: 6 }}>
          <h3>🏆 Final Group Decision</h3>
          <pre>{JSON.stringify(final, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
