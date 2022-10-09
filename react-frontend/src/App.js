import logo from './logo.svg';
import Axios from 'axios';
import './App.css';

function App() {
  const getJoke = () => {
    Axios.get('http://official-joke-api.appspot.com/random_joke').then((response) => {
      console.log(response.data);
    });
  };
  return (
    <div className="App">
      <p>Token from Flask change not showing = {window.token}</p>
      <button onClick={getJoke}>Get Joke</button>
    </div>
  );
}

export default App;
