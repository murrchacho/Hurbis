import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation, useNavigate, Navigate } from 'react-router-dom';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

const RequireAuth = ({children}) => {
    const navigate = useNavigate();
    const locaiton = useLocation();
    const auth = false;

    if(!auth) {
        return <Navigate to='/login' state={{from: location}} />
    }
  
    return children;
  };
  
  
  export default RequireAuth