import { Link, Outlet } from 'react-router-dom'
import { useContext } from 'react';
import * as HOCs from '../Components/HOCs/All';

const Layout = () => {
    const value = useContext(HOCs.AuthContext);
    let postsLink;
    let chat;
    if (value.profile_type == "applicant"){
        postsLink =  <Link to="/vacancies">Найти работу</Link>
    }
    else if(value.profile_type){
        postsLink = <Link to="/cvs">Найти сотрудника</Link>
    }
    return(
        <>
            <header>
                <Link to="/">Главная</Link>
                {postsLink}
                <Link to="/chat">Чат</Link>
                {value.data.user
                    ? <Link to="/logout">Выход</Link>
                    : <Link to="/login">Вход</Link> 
                }
            </header>
            
            <main className='container'>
                <Outlet />
            </main>

            <footer>
                Hubris
            </footer>
        </>
    )
}

export default Layout