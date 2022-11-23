import './App.css';
import { React } from 'react';
import { Routes, Route } from 'react-router-dom'
import * as Components from './Components/All'
import * as HOCs from './Components/HOCs/All';
import './Sass/index.scss'
function App() {
  return (
    <div className="App">
      <HOCs.AuthProvider>
        <Routes>
          <Route path="/" element={<Components.Layout/>}>
            <Route index element={<Components.Homepage/>} />
            <Route path="/chat" element={
              <HOCs.RequireAuth>
                <Components.Chat/>
              </HOCs.RequireAuth>
              } />
            <Route path="/login" element={<Components.Login/>} />
            <Route path="/logout" element={<Components.Logout/>} />
            <Route path="*" element={<Components.Error/>} />
          </Route>
        </Routes>
      </HOCs.AuthProvider>
    </div>
  );
}

export default App;
