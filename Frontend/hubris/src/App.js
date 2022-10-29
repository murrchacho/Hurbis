import './App.css';
import { Routes, Route, Link } from 'react-router-dom'
import * as Components from './Components/all'

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Components.Layout/>}>
          <Route index element={<Components.Homepage/>} />
          <Route path="/chat" element={<Components.Chat/>} />
          <Route path="/login" element={<Components.Login/>} />
          <Route path="*" element={<Components.Error/>} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;
