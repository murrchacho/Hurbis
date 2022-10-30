import React from 'react';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from './hooks/All';
import { useContext } from 'react';
import * as HOCs from '../Components/HOCs/All';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

const Logout = () => {
    const value = useContext(HOCs.AuthContext);
    const navigate = useNavigate();
    const locaiton = useLocation();
    const {signout} = useAuth();
    const fromPage = locaiton.state?.from?.pathname || '/';

    const logout = () => {
      axios.post('api/auth/logout', { username: value.data.user })
                .then((response)=>{
                  if(response.status == 200 && response.data != null){
                    signout(() => navigate("/", {replace: true}));
                  }
                  else alert('Неправильно ты, дядя Федор, форму заполняешь..')
                });
    }
  
    const handleSubmit = (e) => {
      e.preventDefault();
      logout();
    }
  
    return (
      <div>
        Вы уверены, что хотите выйти?
        <form onSubmit={handleSubmit}>
          <button type="submit">Да</button>
          <button type="button" onClick={()=>navigate(fromPage, {replace: true})}>Нет</button>
        </form>
      </div>
    );
  };
  
  
  export default Logout