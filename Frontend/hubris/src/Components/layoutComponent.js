import { Link, Outlet } from 'react-router-dom'

const Layout = () => {
    return(
        <>
            <header>
                <Link to="/">Главная</Link>
                <Link to="/chat">Чат</Link>
                <Link to="/login">Вход</Link>
                <Link to="/404">404</Link>
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