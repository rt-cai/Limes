// import logo from './logo.svg';
import './App.css';

function getFaviconEl() {
  return document.getElementById("favicon");
}

function App() {
  const favicon = getFaviconEl();
  favicon.href = "/force/fav"

  const todos = [
    {id: 1, text: 'asadf'},
    {id: 2, text: 'bbbb'}
  ]

  return (
    <div className="App">
      <h1> Todo List </h1>
      <TodoList todos={todos}/>
    </div>
  );
}

function TodoList(props) {
  console.log(props)

  return (
      <ul>
          {props.todos.map(todo => (
              <li>item {todo.text}</li>
          ))}
      </ul>
  )
}

export default App;
