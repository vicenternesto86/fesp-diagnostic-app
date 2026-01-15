import { useState, useEffect } from 'react';
import { Bar, Radar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { statesService, dashboardService, reportsService, assessmentsService } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './Dashboard.css';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Title,
    Tooltip,
    Legend
);

const TRAFFIC_COLORS = {
    green: '#22c55e',
    yellow: '#f59e0b',
    red: '#ef4444',
};

function Dashboard() {
    const { user } = useAuth();
    const [states, setStates] = useState([]);
    const [jurisdictions, setJurisdictions] = useState([]);
    const [assessments, setAssessments] = useState([]);
    const [selectedState, setSelectedState] = useState('');
    const [selectedJurisdiction, setSelectedJurisdiction] = useState('');
    const [selectedAssessment, setSelectedAssessment] = useState('');
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    // Load states on mount
    useEffect(() => {
        const loadStates = async () => {
            try {
                const data = await statesService.list();
                setStates(data);
                // Pre-select user's state if assigned
                if (user?.state_id) {
                    setSelectedState(user.state_id.toString());
                }
            } catch (err) {
                console.error('Error loading states:', err);
            }
        };
        loadStates();
    }, [user]);

    // Load jurisdictions when state changes
    useEffect(() => {
        if (selectedState) {
            const loadJurisdictions = async () => {
                try {
                    const data = await statesService.getJurisdictions(selectedState);
                    setJurisdictions(data);
                    // Pre-select user's jurisdiction if assigned
                    if (user?.jurisdiction_id) {
                        setSelectedJurisdiction(user.jurisdiction_id.toString());
                    }
                } catch (err) {
                    console.error('Error loading jurisdictions:', err);
                }
            };
            loadJurisdictions();
        } else {
            setJurisdictions([]);
        }
    }, [selectedState, user]);

    // Load assessments when filters change
    useEffect(() => {
        if (selectedState) {
            const loadAssessments = async () => {
                try {
                    const filters = {
                        state_id: selectedState,
                        status_filter: 'completed',
                    };
                    if (selectedJurisdiction) {
                        filters.jurisdiction_id = selectedJurisdiction;
                    }
                    const data = await assessmentsService.list(filters);
                    setAssessments(data);
                    if (data.length > 0) {
                        setSelectedAssessment(data[0].id.toString());
                    }
                } catch (err) {
                    console.error('Error loading assessments:', err);
                }
            };
            loadAssessments();
        }
    }, [selectedState, selectedJurisdiction]);

    // Load dashboard data when assessment selected
    useEffect(() => {
        if (selectedAssessment) {
            const loadDashboard = async () => {
                setLoading(true);
                setError('');
                try {
                    const data = await dashboardService.getSummary(selectedAssessment);
                    setDashboardData(data);
                } catch (err) {
                    setError('Error cargando el dashboard');
                    console.error(err);
                } finally {
                    setLoading(false);
                }
            };
            loadDashboard();
        }
    }, [selectedAssessment]);

    const handleDownloadHtml = async () => {
        if (!selectedAssessment) return;
        try {
            const blob = await reportsService.downloadHtml(selectedAssessment);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `FESP_Reporte_${dashboardData?.unit_name || 'evaluacion'}.html`;
            a.click();
            window.URL.revokeObjectURL(url);
        } catch (err) {
            alert('Error descargando reporte');
        }
    };

    const handleDownloadCsv = async () => {
        try {
            const blob = await reportsService.downloadCsv({
                state_id: selectedState,
                jurisdiction_id: selectedJurisdiction || undefined,
            });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'fesp_evaluaciones.csv';
            a.click();
            window.URL.revokeObjectURL(url);
        } catch (err) {
            alert('Error descargando CSV');
        }
    };

    // Chart data
    const fespChartData = dashboardData ? {
        labels: dashboardData.fesp_scores.map(f => `FESP ${f.fesp_number}`),
        datasets: [{
            label: 'Cumplimiento (%)',
            data: dashboardData.fesp_scores.map(f => f.compliance_percentage),
            backgroundColor: dashboardData.fesp_scores.map(f => f.color),
            borderRadius: 6,
        }],
    } : null;

    const capacityChartData = dashboardData ? {
        labels: dashboardData.capability_scores.map(c => c.capability.charAt(0).toUpperCase() + c.capability.slice(1)),
        datasets: [{
            label: 'Capacidad Institucional (%)',
            data: dashboardData.capability_scores.map(c => c.compliance_percentage),
            backgroundColor: dashboardData.capability_scores.map(c => c.color),
            borderRadius: 6,
        }],
    } : null;

    const cycleChartData = dashboardData ? {
        labels: dashboardData.policy_cycle_scores.map(c => c.cycle),
        datasets: [{
            label: 'Ciclo de Política (%)',
            data: dashboardData.policy_cycle_scores.map(c => c.compliance_percentage),
            backgroundColor: dashboardData.policy_cycle_scores.map(c => c.color),
            borderRadius: 6,
        }],
    } : null;

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'y', // Horizontal bars for FESP
        scales: {
            x: {
                beginAtZero: true,
                max: 100,
                grid: { color: 'rgba(255,255,255,0.1)' },
                ticks: { color: '#94a3b8', callback: (v) => v + '%' },
            },
            y: {
                grid: { display: false },
                ticks: { color: '#94a3b8', font: { size: 10 } },
            },
        },
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: (context) => `Cumplimiento: ${context.parsed.x}%`
                }
            }
        },
    };

    const verticalBarOptions = {
        ...chartOptions,
        indexAxis: 'x',
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                grid: { color: 'rgba(255,255,255,0.1)' },
                ticks: { color: '#94a3b8', callback: (v) => v + '%' },
            },
            x: {
                grid: { display: false },
                ticks: { color: '#94a3b8' },
            },
        },
    };

    return (
        <div className="page">
            <div className="container">
                <div className="dashboard-header">
                    <h1>Dashboard de Desempeño FESP</h1>
                    <div className="dashboard-actions">
                        <button className="btn-primary" onClick={handleDownloadHtml} disabled={!dashboardData}>
                            📄 Descargar Reporte HTML
                        </button>
                        <button className="btn-secondary" onClick={handleDownloadCsv}>
                            📊 Exportar Histórico CSV
                        </button>
                    </div>
                </div>

                {/* Filters */}
                <div className="filters-card card mb-lg">
                    <div className="filters-grid">
                        <div className="form-group">
                            <label>Entidad Federativa</label>
                            <select
                                value={selectedState}
                                onChange={(e) => {
                                    setSelectedState(e.target.value);
                                    setSelectedJurisdiction('');
                                    setSelectedAssessment('');
                                    setDashboardData(null);
                                }}
                            >
                                <option value="">Seleccionar Estado</option>
                                {states.map(s => (
                                    <option key={s.id} value={s.id}>{s.name}</option>
                                ))}
                            </select>
                        </div>
                        <div className="form-group">
                            <label>Jurisdicción / Distrito</label>
                            <select
                                value={selectedJurisdiction}
                                onChange={(e) => {
                                    setSelectedJurisdiction(e.target.value);
                                    setSelectedAssessment('');
                                    setDashboardData(null);
                                }}
                                disabled={!selectedState}
                            >
                                <option value="">Nivel Estatal (Consolidado)</option>
                                {jurisdictions.map(j => (
                                    <option key={j.id} value={j.id}>{j.name}</option>
                                ))}
                            </select>
                        </div>
                        <div className="form-group">
                            <label>Evaluación (Fecha Corte)</label>
                            <select
                                value={selectedAssessment}
                                onChange={(e) => setSelectedAssessment(e.target.value)}
                                disabled={assessments.length === 0}
                            >
                                <option value="">Seleccionar Evaluación</option>
                                {assessments.map(a => (
                                    <option key={a.id} value={a.id}>
                                        {a.cutoff_date} - {a.level === 'state' ? 'Estatal' : 'Jurisdicción'}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>
                </div>

                {loading && <div className="loading-state">Calculando indicadores...</div>}
                {error && <div className="error-state">{error}</div>}

                {dashboardData && (
                    <>
                        {/* KPI Cards */}
                        <div className="kpi-grid grid grid-4 mb-lg">
                            <div className="kpi-card card">
                                <div className="kpi-label">Unidad de Análisis</div>
                                <div className="kpi-value">{dashboardData.unit_name}</div>
                                <div className="kpi-sub">Corte: {dashboardData.cutoff_date}</div>
                            </div>
                            <div className="kpi-card card">
                                <div className="kpi-label">Cumplimiento Global</div>
                                <div className="kpi-value kpi-score" style={{ color: dashboardData.traffic_light }}>
                                    {dashboardData.total_compliance}%
                                </div>
                                <div className="kpi-sub">Total de Instrumento</div>
                            </div>
                            <div className="kpi-card card">
                                <div className="kpi-label">Nivel de Desempeño</div>
                                <div className="traffic-light" style={{ backgroundColor: dashboardData.traffic_light, color: '#fff', padding: '4px 12px', borderRadius: '20px', display: 'inline-block', marginTop: '10px' }}>
                                    {dashboardData.total_compliance >= 80 ? 'Avanzado' :
                                        dashboardData.total_compliance >= 60 ? 'Intermedio' :
                                            dashboardData.total_compliance >= 40 ? 'Moderado' :
                                                dashboardData.total_compliance >= 20 ? 'Limitado' : 'Inicial'}
                                </div>
                            </div>
                            <div className="kpi-card card">
                                <div className="kpi-label">Brechas Críticas (Items)</div>
                                <div className="kpi-value kpi-gaps">{dashboardData.gap_count}</div>
                                <div className="kpi-sub">Prioridad de atención</div>
                            </div>
                        </div>

                        {/* FESP Analysis */}
                        <div className="grid grid-1 mb-lg">
                            <div className="card">
                                <div className="card-header">
                                    <h3>Cumplimiento por Función Esencial (FESP)</h3>
                                </div>
                                <div className="chart-container" style={{ height: '400px' }}>
                                    {fespChartData && <Bar data={fespChartData} options={chartOptions} />}
                                </div>
                            </div>
                        </div>

                        {/* Multi-dimensional Analysis */}
                        <div className="charts-grid grid grid-2 mb-lg">
                            <div className="card">
                                <div className="card-header">
                                    <h3>Análisis por Capacidad Institucional</h3>
                                </div>
                                <div className="chart-container" style={{ height: '300px' }}>
                                    {capacityChartData && <Bar data={capacityChartData} options={verticalBarOptions} />}
                                </div>
                            </div>
                            <div className="card">
                                <div className="card-header">
                                    <h3>Análisis por Ciclo de Política</h3>
                                </div>
                                <div className="chart-container" style={{ height: '300px' }}>
                                    {cycleChartData && <Bar data={cycleChartData} options={verticalBarOptions} />}
                                </div>
                            </div>
                        </div>

                        {/* FESP Comparison Table */}
                        <div className="card mb-lg">
                            <div className="card-header">
                                <h3>Resumen Ejecutivo por FESP</h3>
                            </div>
                            <div className="table-container">
                                <table>
                                    <thead>
                                        <tr>
                                            <th style={{ width: '80px' }}>FESP</th>
                                            <th>Función Esencial de Salud Pública</th>
                                            <th style={{ textAlign: 'center' }}>Puntaje</th>
                                            <th style={{ textAlign: 'center' }}>Cumplimiento</th>
                                            <th style={{ textAlign: 'center' }}>Nivel</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {dashboardData.fesp_scores.map(fesp => (
                                            <tr key={fesp.fesp_id}>
                                                <td><strong>FESP {fesp.fesp_number}</strong></td>
                                                <td>{fesp.fesp_name}</td>
                                                <td style={{ textAlign: 'center' }}>{fesp.earned_points} / {fesp.max_points}</td>
                                                <td style={{ textAlign: 'center' }}>
                                                    <span className="badge" style={{ backgroundColor: fesp.color, color: '#fff' }}>
                                                        {fesp.compliance_percentage}%
                                                    </span>
                                                </td>
                                                <td style={{ textAlign: 'center' }}>{fesp.level}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* Gaps & Recommendations */}
                        {dashboardData.gaps.length > 0 && (
                            <div className="card">
                                <div className="card-header">
                                    <h3>Plan de Mejora: Brechas Identificadas</h3>
                                </div>
                                <div className="gaps-list">
                                    {dashboardData.gaps.map((gap, index) => (
                                        <div key={index} className={`gap-item priority-${gap.priority}`}>
                                            <div className="gap-header">
                                                <span className={`priority-badge ${gap.priority}`}>
                                                    {gap.priority === 'high' ? 'CRÍTICA' : 'MEDIA'}
                                                </span>
                                                <span className="gap-title">
                                                    ({gap.fesp_id.replace('fesp_', 'FESP ')}) {gap.item_name}
                                                </span>
                                                <span className="gap-score">{gap.percentage}% de cumplimiento</span>
                                            </div>
                                            <p className="gap-recommendation">{gap.recommendation}</p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </>
                )}

                {!dashboardData && !loading && (
                    <div className="empty-state card">
                        <div className="empty-icon">📊</div>
                        <h3>Monitor de Desempeño FESP</h3>
                        <p>Seleccione una entidad y evaluación para visualizar los indicadores de salud pública.</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Dashboard;
