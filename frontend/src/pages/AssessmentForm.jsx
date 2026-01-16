import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { statesService, assessmentsService } from '../services/api';
import './AssessmentForm.css';

const BLOCK_INFO = {
    A: { name: 'Gobernanza y rectoría', color: '#3b82f6' },
    B: { name: 'Información, vigilancia, respuesta', color: '#8b5cf6' },
    C: { name: 'Programas y calidad', color: '#22c55e' },
    D: { name: 'Talento, investigación, innovación', color: '#f59e0b' },
};

const SCORE_LABELS = [
    'Inexistente',
    'Incipiente',
    'En desarrollo',
    'Definido',
    'Gestionado',
    'Óptimo',
];

function AssessmentForm() {
    const { id } = useParams();
    const navigate = useNavigate();
    // Open access - always has write permission
    const user = { role: 'admin' };
    const isWriter = () => true;
    const isEdit = Boolean(id);

    const [states, setStates] = useState([]);
    const [jurisdictions, setJurisdictions] = useState([]);
    const [fespItems, setFespItems] = useState({});
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [activeFesp, setActiveFesp] = useState('fesp_1');

    const [formData, setFormData] = useState({
        level: 'state',
        state_id: '',
        jurisdiction_id: '',
        cutoff_date: new Date().toISOString().split('T')[0],
        items: {},
    });

    // Load initial data
    useEffect(() => {
        const loadData = async () => {
            try {
                const [statesData, fespData] = await Promise.all([
                    statesService.list(),
                    assessmentsService.getFespItems(),
                ]);
                setStates(statesData);
                setFespItems(fespData);

                // Initialize items
                const initialItems = {};
                Object.values(fespData).forEach((fesp) => {
                    fesp.items.forEach(item => {
                        initialItems[item.id] = {
                            fesp_id: fesp.id,
                            item_id: item.id,
                            score: 0,
                            evidence_text: '',
                            evidence_url: '',
                            notes: '',
                        };
                    });
                });
                setFormData(prev => ({ ...prev, items: initialItems }));

                // Pre-fill user's state if assigned
                if (user?.state_id) {
                    setFormData(prev => ({ ...prev, state_id: user.state_id.toString() }));
                    const jurisData = await statesService.getJurisdictions(user.state_id);
                    setJurisdictions(jurisData);
                }

                // Load existing assessment if editing
                if (id) {
                    const assessment = await assessmentsService.get(id);
                    const itemsMap = {};
                    assessment.items.forEach(item => {
                        itemsMap[item.item_id] = {
                            fesp_id: item.fesp_id,
                            item_id: item.item_id,
                            score: item.score,
                            evidence_text: item.evidence_text || '',
                            evidence_url: item.evidence_url || '',
                            notes: item.notes || '',
                        };
                    });
                    setFormData({
                        level: assessment.level,
                        state_id: assessment.state_id.toString(),
                        jurisdiction_id: assessment.jurisdiction_id?.toString() || '',
                        cutoff_date: assessment.cutoff_date,
                        items: itemsMap,
                    });
                    if (assessment.state_id) {
                        const jurisData = await statesService.getJurisdictions(assessment.state_id);
                        setJurisdictions(jurisData);
                    }
                }
            } catch (err) {
                console.error('Error loading data:', err);
            } finally {
                setLoading(false);
            }
        };
        loadData();
    }, [id, user]);

    // Load jurisdictions when state changes
    const handleStateChange = async (stateId) => {
        setFormData(prev => ({ ...prev, state_id: stateId, jurisdiction_id: '' }));
        if (stateId) {
            const data = await statesService.getJurisdictions(stateId);
            setJurisdictions(data);
        } else {
            setJurisdictions([]);
        }
    };

    const handleItemChange = (itemId, field, value) => {
        setFormData(prev => ({
            ...prev,
            items: {
                ...prev.items,
                [itemId]: {
                    ...prev.items[itemId],
                    [field]: value,
                },
            },
        }));
    };

    const handleSubmit = async (status = 'draft') => {
        if (!formData.state_id) {
            alert('Selecciona un estado');
            return;
        }
        if (formData.level === 'jurisdiction' && !formData.jurisdiction_id) {
            alert('Selecciona una jurisdicción');
            return;
        }

        setSaving(true);
        try {
            const payload = {
                level: formData.level,
                state_id: parseInt(formData.state_id),
                jurisdiction_id: formData.jurisdiction_id ? parseInt(formData.jurisdiction_id) : null,
                cutoff_date: formData.cutoff_date,
                status,
                items: Object.values(formData.items),
            };

            if (isEdit) {
                await assessmentsService.update(id, payload);
            } else {
                await assessmentsService.create(payload);
            }

            navigate('/assessments');
        } catch (err) {
            alert(err.response?.data?.detail || 'Error guardando la evaluación');
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return <div className="page"><div className="container loading">Cargando...</div></div>;
    }

    const readOnly = !isWriter();
    const fespList = Object.values(fespItems).sort((a, b) => a.number - b.number);

    return (
        <div className="page">
            <div className="container">
                <div className="form-header">
                    <h1>{isEdit ? 'Editar Evaluación' : 'Nueva Evaluación FESP'}</h1>
                    <div className="form-actions">
                        <button
                            className="btn-secondary"
                            onClick={() => navigate('/assessments')}
                        >
                            Cancelar
                        </button>
                        {!readOnly && (
                            <>
                                <button
                                    className="btn-secondary"
                                    onClick={() => handleSubmit('draft')}
                                    disabled={saving}
                                >
                                    💾 Guardar Borrador
                                </button>
                                <button
                                    className="btn-primary"
                                    onClick={() => handleSubmit('completed')}
                                    disabled={saving}
                                >
                                    ✓ Completar Evaluación
                                </button>
                            </>
                        )}
                    </div>
                </div>

                {/* Meta Info */}
                <div className="card mb-lg">
                    <div className="meta-grid">
                        <div className="form-group">
                            <label>Nivel</label>
                            <select
                                value={formData.level}
                                onChange={(e) => setFormData(prev => ({ ...prev, level: e.target.value }))}
                                disabled={readOnly}
                            >
                                <option value="state">Estatal</option>
                                <option value="jurisdiction">Jurisdicción</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label>Estado</label>
                            <select
                                value={formData.state_id}
                                onChange={(e) => handleStateChange(e.target.value)}
                                disabled={readOnly || (user?.state_id && user.role !== 'admin')}
                            >
                                <option value="">Seleccionar</option>
                                {states.map(s => (
                                    <option key={s.id} value={s.id}>{s.name}</option>
                                ))}
                            </select>
                        </div>
                        {formData.level === 'jurisdiction' && (
                            <div className="form-group">
                                <label>Jurisdicción</label>
                                <select
                                    value={formData.jurisdiction_id}
                                    onChange={(e) => setFormData(prev => ({ ...prev, jurisdiction_id: e.target.value }))}
                                    disabled={readOnly}
                                >
                                    <option value="">Seleccionar</option>
                                    {jurisdictions.map(j => (
                                        <option key={j.id} value={j.id}>{j.name}</option>
                                    ))}
                                </select>
                            </div>
                        )}
                        <div className="form-group">
                            <label>Fecha de Corte</label>
                            <input
                                type="date"
                                value={formData.cutoff_date}
                                onChange={(e) => setFormData(prev => ({ ...prev, cutoff_date: e.target.value }))}
                                disabled={readOnly}
                            />
                        </div>
                    </div>
                </div>

                {/* FESP Tabs */}
                <div className="block-tabs fesp-tabs">
                    {fespList.map(fesp => (
                        <button
                            key={fesp.id}
                            className={`block-tab ${activeFesp === fesp.id ? 'active' : ''}`}
                            onClick={() => setActiveFesp(fesp.id)}
                        >
                            <span className="block-code">FESP {fesp.number}</span>
                            <span className="block-name">{fesp.name}</span>
                        </button>
                    ))}
                </div>

                {/* Items Form */}
                <div className="items-container">
                    <div className="fesp-description mb-md">
                        <p>{fespItems[activeFesp]?.description}</p>
                    </div>
                    {fespItems[activeFesp]?.items.map(itemDef => {
                        const item = formData.items[itemDef.id] || {};
                        const currentOption = itemDef.options?.find(o => o.value === item.score) ||
                            { label: 'Nivel ' + item.score };

                        return (
                            <div key={itemDef.id} className="item-card card">
                                <div className="item-header">
                                    <span className="item-number">Ítem {itemDef.code}</span>
                                    <h3 className="item-name">{itemDef.name}</h3>
                                </div>
                                <p className="item-desc">{itemDef.description}</p>

                                <div className="score-section">
                                    <label>Puntaje: <strong>{item.score}</strong> - {currentOption.label}</label>
                                    <input
                                        type="range"
                                        min="0"
                                        max={itemDef.max_points}
                                        value={item.score}
                                        onChange={(e) => handleItemChange(itemDef.id, 'score', parseInt(e.target.value))}
                                        disabled={readOnly}
                                        className="score-slider"
                                    />
                                    <div className="score-labels">
                                        {itemDef.options?.map((opt) => (
                                            <div
                                                key={opt.value}
                                                className={`score-option ${item.score === opt.value ? 'active' : ''}`}
                                                onClick={() => !readOnly && handleItemChange(itemDef.id, 'score', opt.value)}
                                            >
                                                <span className="val">{opt.value}</span>
                                                <span className="lbl">{opt.label}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label>Evidencia / Justificación (Referencia: {itemDef.capability.toUpperCase()})</label>
                                    <textarea
                                        value={item.evidence_text}
                                        onChange={(e) => handleItemChange(itemDef.id, 'evidence_text', e.target.value)}
                                        placeholder="Describe las evidencias que sustentan este puntaje..."
                                        rows={3}
                                        disabled={readOnly}
                                    />
                                </div>

                                <div className="form-group">
                                    <label>URL de evidencia (opcional)</label>
                                    <input
                                        type="url"
                                        value={item.evidence_url}
                                        onChange={(e) => handleItemChange(itemDef.id, 'evidence_url', e.target.value)}
                                        placeholder="https://..."
                                        disabled={readOnly}
                                    />
                                </div>

                                <div className="form-group">
                                    <label>Observaciones</label>
                                    <textarea
                                        value={item.notes}
                                        onChange={(e) => handleItemChange(itemDef.id, 'notes', e.target.value)}
                                        placeholder="Notas adicionales..."
                                        rows={2}
                                        disabled={readOnly}
                                    />
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}

export default AssessmentForm;
