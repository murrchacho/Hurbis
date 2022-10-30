import { createContext, useState } from "react";

export const AuthContext = createContext(null);

export const AuthProvider = ({children}) => {
    const [data, setData] = useState({});

    const signin = (data, callback) => {
        setData(data);
        callback();
    }
    const signout = (callback) => {
        setData({});
        callback();
    }

    const value = {data, signin, signout}

    return <AuthContext.Provider value={value}>
        {children}
    </AuthContext.Provider>
}
