import { useState } from "react";
import axios from "axios";

const cardStyle = {
  background: "#ffffff",
  borderRadius: 12,
  padding: 20,
  boxShadow: "0 10px 25px rgba(0,0,0,0.08)",
  marginBottom: 20
};

const inputStyle = {
  width: "100%",
  padding: "10px 12px",
  borderRadius: 8,
  border: "1px solid #ddd",
  fontSize: 14
};

const buttonStyle = {
  padding: "10px 16px",
  borderRadius: 8,
  border: "none",
  cursor: "pointer",
  fontWeight: 600
};

export default function App() {
  const [sessionId, setSessionId] = useState("trip1");
  const [userId, setUserId] = useState("u1");

  const [form, setForm] = useState({
    budget_min: "",
    budget_max: "",
    preferred_location: "",
    activities: ""
  });

  const [status, setStatus] = useState("");
  const [final, setFinal] = useState(null);

  const update = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // -----------------------------
  // Submit Preferences
  // -----------------------------
  const submit = async () => {
    await axios.post(
      "http://127.0.0.1:8000/submit_preferences",
      {
        budget: {
          min_budget: form.budget_min ? Number(form.budget_min) : null,
          max_budget: form.budget_max ? Number(form.budget_max) : null
        },
        preferred_location: form.preferred_location || null,
        activities: form.activities
          .split(",")
          .map(a => a.trim())
          .filter(Boolean)
          .map(a => ({ name: a, specific_place: null }))
      },
      { params: { session_id: sessionId, user_id: userId } }
    );

    setStatus("✅ Preferences saved");
  };

  // -----------------------------
  // Lock Group
  // -----------------------------
  const lockGroup = async () => {
    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/lock_group",
        null,
        { params: { session_id: sessionId } }
      );

      if (res.data.status === "locked") {
        setStatus(`🔒 Group locked (${res.data.expected_users} users)`);
      } else if (res.data.status === "already_locked") {
        setStatus("🔒 Group already locked");
      }
    } catch {
      setStatus("❌ Failed to lock group");
    }
  };

  // -----------------------------
  // Mark Ready
  // -----------------------------
  const ready = async () => {
    const res = await axios.post(
      "http://127.0.0.1:8000/ready",
      null,
      { params: { session_id: sessionId, user_id: userId } }
    );

    if (res.data.status === "final") {
      setFinal(res.data.result);
      setStatus("🏆 Final decision ready");
    } else {
      setStatus("⏳ Waiting for other users…");
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background:
          "linear-gradient(90deg, white 0%, lightgreen 50%, darkblue 100%)",
        overflowX: "hidden"
      }}
    >
      <div style={{ maxWidth: 720, margin: "0 auto", padding: 30 }}>
        <h1 style={{ textAlign: "center", marginBottom: 30, color: "blue" }}>
          🧠 Agentic Group Travel Planner
        </h1>

        {/* Session Card */}
        <div style={cardStyle}>
          <h3>Session</h3>
          <div style={{ display: "flex", gap: 10 }}>
            <input
              style={inputStyle}
              placeholder="Session ID"
              value={sessionId}
              onChange={e => setSessionId(e.target.value)}
            />
            <input
              style={inputStyle}
              placeholder="User ID"
              value={userId}
              onChange={e => setUserId(e.target.value)}
            />
          </div>
        </div>

        {/* Preferences Card */}
        <div style={cardStyle}>
          <h3>My Preferences</h3>

          <div style={{ display: "grid", gap: 12 }}>
            <input
              style={inputStyle}
              name="budget_min"
              type="number"
              placeholder="Minimum Budget"
              onChange={update}
            />
            <input
              style={inputStyle}
              name="budget_max"
              type="number"
              placeholder="Maximum Budget"
              onChange={update}
            />
            <input
              style={inputStyle}
              name="preferred_location"
              placeholder="Preferred Location (eg. Imagica,Goa beaches,Lonavla villas)"
              onChange={update}
            />
            <input
              style={inputStyle}
              name="activities"
              placeholder="Activities,comma separated (eg. Swimming,Relaxing,Trekking)"
              onChange={update}
            />
          </div>

          {/* ACTION BUTTONS */}
          <div style={{ marginTop: 16, display: "flex", gap: 10 }}>
            <button
              style={{ ...buttonStyle, background: "#2563eb", color: "white" }}
              onClick={submit}
            >
              Save Preferences
            </button>

            <button
              style={{ ...buttonStyle, background: "#7c3aed", color: "white" }}
              onClick={lockGroup}
            >
              Lock Group
            </button>

            <button
              style={{ ...buttonStyle, background: "#16a34a", color: "white" }}
              onClick={ready}
            >
              Mark Ready
            </button>
          </div>

          {status && (
            <p style={{ marginTop: 12, fontSize: 14, color: "#444" }}>
              {status}
            </p>
          )}
        </div>

        {/* Final Decision */}
        {final && (
          <div style={{ ...cardStyle, border: "2px solid #16a34a" }}>
            <h3>🏆 Final Group Decision</h3>
            <pre
              style={{
                background: "#0f172a",
                color: "#e5e7eb",
                padding: 15,
                borderRadius: 8,
                fontSize: 13,
                overflowX: "auto",
                maxHeight: 400
              }}
            >
              {JSON.stringify(final, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
