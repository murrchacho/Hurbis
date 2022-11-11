import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation, useNavigate, Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/All';


const RequireAuth = ({children}) => {
    const location = useLocation();
    const {data} = useAuth();

    if(!data.username) {
        return <Navigate to='/login' state={{from: location}} />
    }
  
    return children;
  };
  
  
export default RequireAuth