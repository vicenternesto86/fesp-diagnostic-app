import { useState, useEffect } from 'react';
import { usersService, statesService } from '../services/api';
import './Admin.css';

function Admin() {
    const [activeTab, setActiveTab] = useState('users');
    const [users, setUsers] = useState([]);
    const [states, setStates] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showUserModal, setShowUserModal] = useState(false);
    const [editingUser, setEditingUser] = useState(null);
    const [userForm, setUserForm] = useState({
        name: '',
        email: '',
        password: '',
        role: 'reader',
        state_id: '',
        jurisdiction_id: '',
    });

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const [usersData, statesData] = await Promise.all([
                usersService.list(),
                statesService.list(),
            ]);
            setUsers(usersData);
            setStates(statesData);
        } catch (err) {
            console.error('Error loading data:', err);
        } finally {
            setLoading(false);
        }
    };

    const openUserModal = (user = null) => {
        if (user) {
            setEditingUser(user);
            setUserForm({
                name: user.name,
                email: user.email,
                password: '',
                role: user.role,
                state_id: user.state_id?.toString() || '',
                jurisdiction_id: user.jurisdiction_id?.toString() || '',
            });
        } else {
            setEditingUser(null);
            setUserForm({
                name: '',
                email: '',
                password: '',
                role: 'reader',
                state_id: '',
                jurisdiction_id: '',
            });
        }
        setShowUserModal(true);
    };

    const handleUserSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = {
                ...userForm,
                state_id: userForm.state_id ? parseInt(userForm.state_id) : null,
                jurisdiction_id: userForm.jurisdiction_id ? parseInt(userForm.jurisdiction_id) : null,
            };
            if (!data.password) delete data.password;

            if (editingUser) {
                await usersService.update(editingUser.id, data);
            } else {
                await usersService.create(data);
            }
            setShowUserModal(false);
            loadData();
        } catch (err) {
            alert(err.response?.data?.detail || 'Error guardando usuario');
        }
    };

    const handleDeleteUser = async (id) => {
        if (!window.confirm('¿Eliminar este usuario?')) return;
        try {
            await usersService.delete(id);
            loadData();
        } catch (err) {
            alert(err.response?.data?.detail || 'Error eliminando usuario');
        }
    };

    if (loading) {
        return <div className="page"><div className="container loading">Cargando...</div></div>;
    }

    return (
        <div className="page">
            <div className="container">
                <h1>Administración</h1>

                {/* Tabs */}
                <div className="admin-tabs">
                    <button
                        className={`admin-tab ${activeTab === 'users' ? 'active' : ''}`}
                        onClick={() => setActiveTab('users')}
                    >
                        👥 Usuarios
                    </button>
                    <button
                        className={`admin-tab ${activeTab === 'catalogs' ? 'active' : ''}`}
                        onClick={() => setActiveTab('catalogs')}
                    >
                        📋 Catálogos
                    </button>
                </div>

                {/* Users Tab */}
                {activeTab === 'users' && (
                    <div className="card">
                        <div className="card-header">
                            <h3>Gestión de Usuarios</h3>
                            <button className="btn-primary" onClick={() => openUserModal()}>
                                + Nuevo Usuario
                            </button>
                        </div>
                        <div className="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Nombre</th>
                                        <th>Email</th>
                                        <th>Rol</th>
                                        <th>Estado</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {users.map(user => (
                                        <tr key={user.id}>
                                            <td>{user.name}</td>
                                            <td>{user.email}</td>
                                            <td>
                                                <span className={`role-badge ${user.role}`}>{user.role}</span>
                                            </td>
                                            <td>{states.find(s => s.id === user.state_id)?.name || '-'}</td>
                                            <td>
                                                <button className="btn-ghost" onClick={() => openUserModal(user)}>
                                                    ✏️
                                                </button>
                                                <button
                                                    className="btn-ghost btn-danger-text"
                                                    onClick={() => handleDeleteUser(user.id)}
                                                >
                                                    🗑️
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}

                {/* Catalogs Tab */}
                {activeTab === 'catalogs' && (
                    <div className="card">
                        <div className="card-header">
                            <h3>Estados y Jurisdicciones</h3>
                        </div>
                        <div className="catalogs-list">
                            {states.map(state => (
                                <div key={state.id} className="catalog-item">
                                    <div className="catalog-header">
                                        <strong>{state.name}</strong>
                                        <span className="catalog-code">{state.code}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                        <p className="text-muted" style={{ marginTop: 'var(--space-md)' }}>
                            Para agregar/editar catálogos, use la API directamente o contacte al administrador del sistema.
                        </p>
                    </div>
                )}

                {/* User Modal */}
                {showUserModal && (
                    <div className="modal-overlay" onClick={() => setShowUserModal(false)}>
                        <div className="modal" onClick={e => e.stopPropagation()}>
                            <h2>{editingUser ? 'Editar Usuario' : 'Nuevo Usuario'}</h2>
                            <form onSubmit={handleUserSubmit}>
                                <div className="form-group">
                                    <label>Nombre</label>
                                    <input
                                        type="text"
                                        value={userForm.name}
                                        onChange={e => setUserForm(prev => ({ ...prev, name: e.target.value }))}
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Email</label>
                                    <input
                                        type="email"
                                        value={userForm.email}
                                        onChange={e => setUserForm(prev => ({ ...prev, email: e.target.value }))}
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Contraseña {editingUser && '(dejar vacío para no cambiar)'}</label>
                                    <input
                                        type="password"
                                        value={userForm.password}
                                        onChange={e => setUserForm(prev => ({ ...prev, password: e.target.value }))}
                                        required={!editingUser}
                                    />
                                </div>
                                <div className="form-group">
                                    <label>Rol</label>
                                    <select
                                        value={userForm.role}
                                        onChange={e => setUserForm(prev => ({ ...prev, role: e.target.value }))}
                                    >
                                        <option value="admin">Admin</option>
                                        <option value="writer">Writer (Capturista)</option>
                                        <option value="reader">Reader (Lector)</option>
                                    </select>
                                </div>
                                <div className="form-group">
                                    <label>Estado asignado (opcional)</label>
                                    <select
                                        value={userForm.state_id}
                                        onChange={e => setUserForm(prev => ({ ...prev, state_id: e.target.value }))}
                                    >
                                        <option value="">Sin asignar</option>
                                        {states.map(s => (
                                            <option key={s.id} value={s.id}>{s.name}</option>
                                        ))}
                                    </select>
                                </div>
                                <div className="modal-actions">
                                    <button type="button" className="btn-secondary" onClick={() => setShowUserModal(false)}>
                                        Cancelar
                                    </button>
                                    <button type="submit" className="btn-primary">
                                        Guardar
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Admin;
