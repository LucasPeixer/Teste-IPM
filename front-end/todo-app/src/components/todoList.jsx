import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const TodoList = () => {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTodos = async () => {
      const token = localStorage.getItem("token");
      if (!token) return; // Verifica se o usuário está autenticado

      const response = await fetch("http://localhost:5000/todos", {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });
      const data = await response.json();
      setTodos(data);
      setLoading(false);
    };

    fetchTodos();
  }, []);

  const handleDelete = async (id) => {
    const token = localStorage.getItem("token");

    const response = await fetch(`http://localhost:5000/todos/${id}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });

    if (response.ok) {
      setTodos(todos.filter(todo => todo.id !== id));
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between mb-4">
          <h2 className="text-xl font-semibold">Tarefas</h2>
          <Link to="/add" className="py-2 px-4 bg-red-600 text-white rounded hover:bg-red-700">Adicionar Tarefa</Link>
        </div>
        {loading ? (
          <div>Carregando...</div>
        ) : (
          <div>
            {todos.length === 0 ? (
              <div className="text-gray-500">Nenhuma tarefa encontrada.</div>
            ) : (
              <ul>
                {todos.map(todo => (
                  <li key={todo.id} className="mb-4 p-4 border border-gray-300 rounded hover:bg-gray-50">
                    <h3 className="font-medium">{todo.title}</h3>
                    <p>{todo.description}</p>
                    <div className="flex justify-between mt-2">
                      <span className="text-gray-600">{todo.status}</span>
                      <div>
                        <button
                          onClick={() => handleDelete(todo.id)}
                          className="py-1 px-3 bg-red-600 text-white rounded hover:bg-red-700"
                        >
                          Deletar
                        </button>
                        <Link to={`/edit/${todo.id}`} className="ml-2 py-1 px-3 bg-blue-600 text-white rounded hover:bg-blue-700">
                          Editar
                        </Link>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default TodoList;
