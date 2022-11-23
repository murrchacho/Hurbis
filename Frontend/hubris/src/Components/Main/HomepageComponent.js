import { useContext } from 'react';
import * as HOCs from '../HOCs/All';

const Homepage = () => {
    let value = useContext(HOCs.AuthContext);
    return (
      <div>
        Добро пожаловать {value.data.username
                          ? value.data.username
                          : "странник"
                          }
      </div>
    );
  };
  
  
  export default Homepage