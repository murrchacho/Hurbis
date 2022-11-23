import React from 'react';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/All';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

const Login = () => {
    const navigate = useNavigate();
    const locaiton = useLocation();
    const {signin} = useAuth();

    const fromPage = locaiton.state?.from?.pathname || '/';

    const login = (props) => {
      axios.post('auth/api/v1/login', { username: props.username, password: props.password })
                .then((response)=>{
                  if(response.status == 200 && response.data != null){
                    signin(response.data.data, () => navigate(fromPage, {replace: true}));
                  }
                  else alert('Неправильно ты, дядя Федор, форму заполняешь..')
                });
    }
  
    const handleSubmit = (e) => {
      e.preventDefault();
      const form = e.target
      const username = form.username.value;
      const password = form.password.value;
      login({username, password});
    }
  
    return (
      <div>
        <form onSubmit={handleSubmit}>
          <input type="text" name="username"/>
          <input type="password" name="password"/>
          <button type="submit">Войти</button>
        </form>
      </div>
    );
  };
  
  
  export default Login