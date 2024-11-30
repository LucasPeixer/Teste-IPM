import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/login";
import TodoList from "./components/todoList";
import AddTodo from "./components/addTodo";
import EditTodo from "./components/EditTodo";  // Defina o componente de edição

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/todos" element={<TodoList />} />
        <Route path="/add" element={<AddTodo />} />
        <Route path="/edit/:id" element={<EditTodo />} />
      </Routes>
    </Router>
  );
};

export default App;
