import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

function Navbar() {
    const { user, logout, isAdmin, isWriter } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

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
                    {isWriter() && (
                        <Link to="/assessment/new" className="nav-link">Nueva Evaluación</Link>
                    )}
                    {isAdmin() && (
                        <Link to="/admin" className="nav-link">Admin</Link>
                    )}
                </div>

                <div className="navbar-user">
                    <div className="user-info">
                        <span className="user-name">{user?.name}</span>
                        <span className="user-role">{user?.role}</span>
                    </div>
                    <button onClick={handleLogout} className="btn-ghost logout-btn">
                        Salir
                    </button>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;
