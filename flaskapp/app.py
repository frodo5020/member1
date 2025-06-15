import { useEffect, useState } from "react";
import axios from "axios";

const API_BASE = "http://43.203.196.177:5000";

function App() {
  const [members, setMembers] = useState([]);
  const [search, setSearch] = useState({ id: "", name: "", gender: "", age: "" });
  const [form, setForm] = useState({ id: "", name: "", gender: "", age: "" });
  const [editStates, setEditStates] = useState({});
  const [showResults, setShowResults] = useState(false);

  const fetchMembers = async () => {
    try {
      const params = Object.fromEntries(Object.entries(search).filter(([_, v]) => v !== ""));
      const res = await axios.get(`${API_BASE}/api/members`, { params });
      setMembers(res.data);
      setShowResults(true);

      const initialEdits = {};
      res.data.forEach((m) => {
        initialEdits[m.id] = { name: m.name, gender: m.gender, age: m.age };
      });
      setEditStates(initialEdits);
    } catch (err) {
      alert("데이터 조회 실패");
    }
  };

  const handleCreate = async () => {
    try {
      await axios.post(`${API_BASE}/api/members`, form);
      setForm({ id: "", name: "", gender: "", age: "" });
      fetchMembers();
    } catch (err) {
      alert("생성 실패");
    }
  };

  const handleUpdate = async (id) => {
    try {
      await axios.put(`${API_BASE}/api/members/${id}`, editStates[id]);
      fetchMembers();
    } catch (err) {
      alert("수정 실패");
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API_BASE}/api/members/${id}`);
      fetchMembers();
    } catch (err) {
      alert("삭제 실패");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>회원 검색</h1>
      <div style={{ marginBottom: "1rem" }}>
        <input placeholder="ID" value={search.id} onChange={(e) => setSearch({ ...search, id: e.target.value })} />
        <input placeholder="이름" value={search.name} onChange={(e) => setSearch({ ...search, name: e.target.value })} />
        <input placeholder="성별" value={search.gender} onChange={(e) => setSearch({ ...search, gender: e.target.value })} />
        <input placeholder="나이" value={search.age} onChange={(e) => setSearch({ ...search, age: e.target.value })} />
        <button onClick={fetchMembers}>검색</button>
        <p style={{ fontSize: "0.9rem" }}>※ 검색 조건 없이 [검색] 버튼을 누르면 전체 회원 목록이 나옵니다.</p>
      </div>

      <h2>회원 등록</h2>
      <div>
        <input placeholder="ID" value={form.id} onChange={(e) => setForm({ ...form, id: e.target.value })} />
        <input placeholder="이름" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
        <input placeholder="성별" value={form.gender} onChange={(e) => setForm({ ...form, gender: e.target.value })} />
        <input placeholder="나이" value={form.age} onChange={(e) => setForm({ ...form, age: e.target.value })} />
        <button onClick={handleCreate}>등록</button>
      </div>

      {showResults && (
        <>
          <h2>회원 목록</h2>
          <table border="1" cellPadding="5">
            <thead>
              <tr>
                <th>ID</th>
                <th>이름</th>
                <th>성별</th>
                <th>나이</th>
                <th>수정</th>
                <th>삭제</th>
              </tr>
            </thead>
            <tbody>
              {members.map((m) => (
                <tr key={m.id}>
                  <td>{m.id}</td>
                  <td>
                    <input
                      value={editStates[m.id]?.name || ""}
                      onChange={(e) =>
                        setEditStates({ ...editStates, [m.id]: { ...editStates[m.id], name: e.target.value } })
                      }
                    />
                  </td>
                  <td>
                    <input
                      value={editStates[m.id]?.gender || ""}
                      onChange={(e) =>
                        setEditStates({ ...editStates, [m.id]: { ...editStates[m.id], gender: e.target.value } })
                      }
                    />
                  </td>
                  <td>
                    <input
                      value={editStates[m.id]?.age || ""}
                      onChange={(e) =>
                        setEditStates({ ...editStates, [m.id]: { ...editStates[m.id], age: e.target.value } })
                      }
                    />
                  </td>
                  <td>
                    <button onClick={() => handleUpdate(m.id)}>수정</button>
                  </td>
                  <td>
                    <button onClick={() => handleDelete(m.id)}>삭제</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}

export default App;
