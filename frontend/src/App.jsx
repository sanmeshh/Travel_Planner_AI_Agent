import { useState } from "react";
import axios from "axios";

const cardStyle = {
  background: "#ffffff",
  borderRadius: 12,
  padding: 20,
  boxShadow: "0 10px 25px rgba(0,0,0,0.08)",
  marginBottom: 20,
  color:"black"
};
const inputStyle = {
  width: "100%",
  padding: "12px 16px",
  borderRadius: "8px",
  border: "1px solid #e2e8f0", // Light border
  fontSize: "14px",
  backgroundColor: "#ffffff",   // White background
  color: "#1a202c",             // Dark text
  outline: "none",
  transition: "border-color 0.2s",
};

const buttonStyle = {
  padding: "10px 16px",
  borderRadius: 8,
  border: "none",
  cursor: "pointer",
  fontWeight: 600,
};

export default function App() {
  const [sessionId, setSessionId] = useState("trip1");
  const [userId, setUserId] = useState("u1");

  const [form, setForm] = useState({
  budget_min: "",
  budget_max: "",
  preferred_location: "",
  activities: "",
  trip_type: "", 
  start_date: "",
  end_date:""          
});

  const [status, setStatus] = useState("");
  const [finalDecision, setFinalDecision] = useState(null);
  const [explanation, setExplanation] = useState(null);

  const update = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // -----------------------------
  // Submit Preferences
  // -----------------------------
  const submit = async () => {
  try {
    await axios.post(
      "http://127.0.0.1:8000/submit_preferences",
      {
        budget: { 
          min_budget: form.budget_min ? Number(form.budget_min) : null, 
          max_budget: form.budget_max ? Number(form.budget_max) : null 
        },
        preferred_location: form.preferred_location || null,
        activities: form.activities.split(",").map((a) => a.trim()).filter(Boolean),
        trip_type: form.trip_type || null,
    
        start_date: form.start_date || null,
        end_date: form.end_date || null,
      },
      { params: { session_id: sessionId, user_id: userId } }
    );
    setStatus("Preferences saved!");
  } catch (err) {
    setStatus("Error saving preferences");
  }
};

  // Lock Group
 
  const lockGroup = async () => {
    const res = await axios.post(
      "http://127.0.0.1:8000/lock_group",
      null,
      { params: { session_id: sessionId } }
    );

    if (res.data.status === "locked") {
      setStatus(` Group locked (${res.data.expected_users} users)`);
    } else if (res.data.status === "already_locked") {
      setStatus("Group already locked");
    }
  };

  // -----------------------------
  // Mark Ready
  // -----------------------------
  const markReady = async () => {
    const res = await axios.post(
      "http://127.0.0.1:8000/ready",
      null,
      {
        params: {
          session_id: sessionId,
          user_id: userId,
        },
      }
    );

    if (res.data.status === "final") {
      setFinalDecision(res.data.result);
      setExplanation(res.data.explanation);
      setStatus("Final decision ready!");
    } else {
      setStatus("Waiting for other users");
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background:
          "linear-gradient(90deg, white 0%, lightgreen 50%, darkblue 100%)",
        padding: 30,
      }}
    >
      <div style={{ maxWidth: 720, margin: "0 auto" }}>
        <h1 style={{ textAlign: "center", marginBottom: 30, color: "white",fontSize: "3rem",
                      fontWeight: "800",
                      fontFamily: "'Inter', sans-serif",
                      textShadow: "2px 2px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000"}}>
          AgenticAI Group Travel Planner
        </h1>

        {/* Session */}
        <div style={cardStyle}>
          <h3>Session</h3>
          <div style={{ display: "flex", gap: 10 }}>
            <input
              style={inputStyle}
              value={sessionId}
              placeholder="Session ID"
              onChange={(e) => setSessionId(e.target.value)}
            />
            <input
              style={inputStyle}
              value={userId}
              placeholder="User ID"
              onChange={(e) => setUserId(e.target.value)}
            />
          </div>
        </div>

        {/* Preferences */}
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
              placeholder="Preferred Location (eg. Lonavala)"
              onChange={update}
            />
            <input
              style={inputStyle}
              name="activities"
              placeholder="Activities (eg.Water park,chikki shopping)"
              onChange={update}
            />

            <input
              style={inputStyle}
              name="trip_type"
              placeholder="Trip Type (eg.Road Trip,Weekend Gateway) "
              value={form.destination_type}
              onChange={update}
            />

            
            <div style={{ display: "flex", gap: "10px" }}>
            <div style={{ flex: 1 }}>
              <label style={{ fontSize: "12px", color: "#080808" }}>Start Date</label>
              <input
                type="date"
                style={inputStyle}
                name="start_date"
                value={form.start_date}
                onChange={update}
              />
            </div>
            <div style={{ flex: 1 }}>
              <label style={{ fontSize: "12px", color: "#0e0a0a" }}>End Date</label>
              <input
                type="date"
                style={inputStyle}
                name="end_date"
                value={form.end_date}
                onChange={update}
              />
            </div>
          </div>
          </div>

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
              onClick={markReady}
            >
              Mark Ready
            </button>
          </div>

          {status && (
            <p style={{ marginTop: 12, color: "#444" }}>{status}</p>
          )}
        </div>

        {/* Final Decision */}
        {finalDecision && (
          <div style={{ ...cardStyle, border: "2px solid #16a34a" }}>
            <h3>Final Trip Plan</h3>

            <p>
              <strong>Location:</strong>{" "}
              {finalDecision.final_location}
            </p>

            {finalDecision.final_budget && (
              <p>
                <strong>Budget:</strong>{" "}
                {finalDecision.final_budget.min_budget} –{" "}
                {finalDecision.final_budget.max_budget}
              </p>
            )}

            <p>
              <strong>Activities:</strong>{" "}
              {finalDecision.activities?.map((a) => (typeof a === 'string' ? a : a.name)).join(", ")}
            </p>
                {finalDecision.trip_type && (
            <p>
              <strong>Trip Type:</strong> {finalDecision.trip_type}
            </p>
          )}
          </div>
        )}

        {/* Explanation */}
        {explanation && (
          <div style={{ ...cardStyle, border: "2px solid #2563eb" }}>
            <h3>Why this decision?</h3>

            <p>{explanation.overview}</p>

            <h4>{explanation.location.title}</h4>
            <p>{explanation.location.summary}</p>

      
      {explanation.dates && (
        <div>

          <h4 style={{ margin: "0 0 4px 0", color: "#0a0a0a" }}>{explanation.dates.title}</h4>

          <p>{explanation.dates.summary}</p>

        </div>
      )}

      {explanation.trip_type && (
        <div>

          <h4 style={{ margin: "0 0 4px 0", color: "#16181a" }}>{explanation.trip_type.title}</h4>

          <p>{explanation.trip_type.summary}</p>

        </div>
      )}

            <h4>{explanation.budget.title}</h4>
            <p>{explanation.budget.summary}</p>

            <h4>{explanation.activities.title}</h4>
            <p>{explanation.activities.summary}</p>
          </div>
        )}
      </div>
    </div>
  );
}
