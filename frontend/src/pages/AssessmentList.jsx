import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { assessmentsService, statesService } from '../services/api';
import './AssessmentList.css';

function AssessmentList() {
    // Open access - always has full permissions
    const user = { role: 'admin' };
    const isWriter = () => true;
    const isAdmin = () => true;
    const [assessments, setAssessments] = useState([]);
    const [states, setStates] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filters, setFilters] = useState({
        state_id: '',
        status_filter: '',
    });

    useEffect(() => {
        const loadStates = async () => {
            const data = await statesService.list();
            setStates(data);
        };
        loadStates();
    }, []);

    useEffect(() => {
        const loadAssessments = async () => {
            setLoading(true);
            try {
                const data = await assessmentsService.list(filters);
                setAssessments(data);
            } catch (err) {
                console.error('Error loading assessments:', err);
            } finally {
                setLoading(false);
            }
        };
        loadAssessments();
    }, [filters]);

    const handleDelete = async (id) => {
        if (!window.confirm('¿Eliminar esta evaluación?')) return;
        try {
            await assessmentsService.delete(id);
            setAssessments(prev => prev.filter(a => a.id !== id));
        } catch (err) {
            alert(err.response?.data?.detail || 'Error eliminando');
        }
    };

    const getStateName = (stateId) => {
        const state = states.find(s => s.id === stateId);
        return state?.name || '-';
    };

    return (
        <div className="page">
            <div className="container">
                <div className="list-header">
                    <h1>Evaluaciones</h1>
                    {isWriter() && (
                        <Link to="/assessment/new" className="btn-primary">
                            + Nueva Evaluación
                        </Link>
                    )}
                </div>

                {/* Filters */}
                <div className="card mb-lg">
                    <div className="filters-row">
                        <div className="form-group">
                            <label>Estado</label>
                            <select
                                value={filters.state_id}
                                onChange={(e) => setFilters(prev => ({ ...prev, state_id: e.target.value }))}
                            >
                                <option value="">Todos</option>
                                {states.map(s => (
                                    <option key={s.id} value={s.id}>{s.name}</option>
                                ))}
                            </select>
                        </div>
                        <div className="form-group">
                            <label>Estado</label>
                            <select
                                value={filters.status_filter}
                                onChange={(e) => setFilters(prev => ({ ...prev, status_filter: e.target.value }))}
                            >
                                <option value="">Todos</option>
                                <option value="draft">Borrador</option>
                                <option value="completed">Completado</option>
                            </select>
                        </div>
                    </div>
                </div>

                {/* Table */}
                <div className="card">
                    {loading ? (
                        <div className="loading-state">Cargando...</div>
                    ) : assessments.length === 0 ? (
                        <div className="empty-state">
                            <p>No hay evaluaciones</p>
                            {isWriter() && (
                                <Link to="/assessment/new" className="btn-primary">Crear primera evaluación</Link>
                            )}
                        </div>
                    ) : (
                        <div className="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Nivel</th>
                                        <th>Estado</th>
                                        <th>Fecha Corte</th>
                                        <th>Status</th>
                                        <th>Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {assessments.map(assessment => (
                                        <tr key={assessment.id}>
                                            <td>{assessment.id}</td>
                                            <td>
                                                <span className={`level-badge ${assessment.level}`}>
                                                    {assessment.level === 'state' ? 'Estatal' : 'Jurisdicción'}
                                                </span>
                                            </td>
                                            <td>{getStateName(assessment.state_id)}</td>
                                            <td>{assessment.cutoff_date}</td>
                                            <td>
                                                <span className={`status-badge ${assessment.status}`}>
                                                    {assessment.status === 'completed' ? 'Completado' : 'Borrador'}
                                                </span>
                                            </td>
                                            <td>
                                                <div className="action-buttons">
                                                    <Link to={`/assessment/${assessment.id}`} className="btn-ghost">
                                                        👁️ Ver
                                                    </Link>
                                                    {isAdmin() && (
                                                        <button
                                                            className="btn-ghost btn-danger-text"
                                                            onClick={() => handleDelete(assessment.id)}
                                                        >
                                                            🗑️
                                                        </button>
                                                    )}
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default AssessmentList;
