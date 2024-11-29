import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

const EditTodo = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { id } = useParams();  // Obtém o ID da tarefa da URL

  // Buscar tarefa ao carregar o componente
  useEffect(() => {
    const fetchTodo = async () => {
      try {
        const response = await fetch(`http://localhost:5000/todos/${id}`);
        const data = await response.json();
        if (response.ok) {
          setTitle(data.title);
          setDescription(data.description);
          setDueDate(data.dueDate);
        } else {
          setError(data.message || "Erro ao buscar tarefa.");
        }
      } catch (error) {
        setError("Erro de rede. Tente novamente.");
      }
    };
    fetchTodo();
  }, [id]);

  // Manipula a atualização da tarefa
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://localhost:5000/todos/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`, // Autorização com JWT
        },
        body: JSON.stringify({ title, description, dueDate }),
      });

      const data = await response.json();

      if (response.ok) {
        navigate("/todos");  // Redireciona para a lista de tarefas após atualização
      } else {
        setError(data.message || "Erro ao atualizar tarefa.");
      }
    } catch (error) {
      setError("Erro de rede. Tente novamente.");
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <div className="w-full max-w-md bg-white p-6 rounded shadow-md">
        <h2 className="text-2xl font-semibold text-center mb-4">Editar Tarefa</h2>
        {error && <div className="bg-red-200 text-red-800 p-2 mb-4 rounded">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="title" className="block text-sm font-medium">Título</label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded mt-1"
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="description" className="block text-sm font-medium">Descrição</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded mt-1"
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="dueDate" className="block text-sm font-medium">Prazo</label>
            <input
              id="dueDate"
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded mt-1"
              required
            />
          </div>
          <button type="submit" className="w-full py-2 bg-red-600 text-white rounded hover:bg-red-700">
            Atualizar Tarefa
          </button>
        </form>
      </div>
    </div>
  );
};

export default EditTodo;
