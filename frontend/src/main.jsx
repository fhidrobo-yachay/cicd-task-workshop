import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";
const API = import.meta.env.VITE_API_URL || "http://localhost:8000";
export function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");
  async function refresh() { try { const r = await fetch(`${API}/tasks`); if (!r.ok) throw Error("API unavailable"); setTasks(await r.json()); setError(""); } catch { setError("API unavailable: check backend URL and CORS"); } }
  useEffect(() => { refresh(); }, []);
  async function add(e) { e.preventDefault(); const r = await fetch(`${API}/tasks`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({title})}); if (r.ok) {setTitle(""); refresh();} }
  async function done(id) { await fetch(`${API}/tasks/${id}`, {method:"PATCH"}); refresh(); }
  return <main><h1>CI/CD Task Manager</h1><p>React → FastAPI → SQL database</p><form onSubmit={add}><input aria-label="Task title" value={title} onChange={e=>setTitle(e.target.value)} required /><button>Add task</button></form>{error && <p role="alert">{error}</p>}<ul>{tasks.map(t=><li key={t.id}>{t.title} {t.done ? "✓" : <button onClick={()=>done(t.id)}>Done</button>}</li>)}</ul></main>;
}
createRoot(document.getElementById("root")).render(<App />);
