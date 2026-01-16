import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/dashboard" className="navbar-brand">
                    <span className="brand-icon">📊</span>
                    <span className="brand-text">
                        <strong>FESP</strong> Dx
                    </span>
                </Link>

                <div className="navbar-menu">
                    <Link to="/dashboard" className="nav-link">Dashboard</Link>
                    <Link to="/assessments" className="nav-link">Evaluaciones</Link>
                    <Link to="/assessment/new" className="nav-link">Nueva Evaluación</Link>
                    <Link to="/admin" className="nav-link">Admin</Link>
                </div>

                <div className="navbar-user">
                    <div className="user-info">
                        <span className="user-name">Administrador</span>
                        <span className="user-role">admin</span>
                    </div>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;
