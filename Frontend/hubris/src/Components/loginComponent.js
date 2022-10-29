import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

const Login = () => {
    const navigate = useNavigate();
    const locaiton = useLocation();

    const [username, setUsername] = useState([{}]);
    const [password, setPassword] = useState([{}]);

  
    const fromPage = locaiton.state?.from?.pathname || '/';

    const login = (props) => {
      axios.post('api/auth/login/', { username: props.username, password: props.password }
      );
    }
  
    const handleUsernameChange = (e) => {
      setUsername(e.target.value);
    };
    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };
  
    return (
      <div>
        <input type="text" onChange={handleUsernameChange}></input>
        <input type="password" onChange={handlePasswordChange}></input>
        <button onClick={() => login({ username, password })}>Создать</button>
      </div>
    );
  };
  
  
  export default Login