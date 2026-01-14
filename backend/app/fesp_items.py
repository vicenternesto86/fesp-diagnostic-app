"""
FESP Items Definition - 23 Evaluation Items from FESP2.xlsx

Based on the consolidated FESP evaluation instrument.

Structure:
- 11 FESPs (Funciones Esenciales de Salud Pública)
- 23 evaluation items
- 4 Capacidades Institucionales (Formal, Estructural, Desempeño, Supervisión)
- 4 Ciclos de Políticas (Evaluación, Desarrollo de políticas públicas, Asignación de recursos, Acceso)
- Total maximum score: 115 points (23 items x 5 points each)
"""

# Response level definitions (same for all items)
RESPONSE_LEVELS = [
    {"value": 0, "label": "No cumple", "description": "No existe evidencia o no se realiza"},
    {"value": 1, "label": "Inicial", "description": "Existe de manera parcial sin integración"},
    {"value": 2, "label": "Limitado", "description": "Existe con integración parcial"},
    {"value": 3, "label": "Moderado", "description": "Existe completo pero sin seguimiento"},
    {"value": 4, "label": "Intermedio", "description": "Existe completo con seguimiento"},
    {"value": 5, "label": "Avanzado", "description": "Existe completo con todo el sector integrado"},
]

# Compliance level thresholds
COMPLIANCE_LEVELS = {
    "inicial": {"min": 0, "max": 20, "label": "Inicial", "color": "#FF4444"},
    "limitado": {"min": 20.01, "max": 40, "label": "Limitado", "color": "#FF8C00"},
    "moderado": {"min": 40.01, "max": 60, "label": "Moderado", "color": "#FFD700"},
    "intermedio": {"min": 60.01, "max": 80, "label": "Intermedio", "color": "#90EE90"},
    "avanzado": {"min": 80.01, "max": 100, "label": "Avanzado", "color": "#00C853"},
}

# Complete FESP Structure with 23 items from FESP2.xlsx
FESP_ITEMS = {
    "fesp_1": {
        "id": "fesp_1",
        "number": 1,
        "name": "Monitoreo y evaluación",
        "description": "Capacidad para monitorear el estado de salud de la población y evaluar las intervenciones de salud pública",
        "max_points": 15,
        "policy_cycle": "evaluacion",
        "items": [
            {
                "id": "fesp_1_1",
                "code": "1",
                "name": "Análisis Situacional de Salud Distrital (ASIS)",
                "description": "Elaboración anual del ASIS",
                "max_points": 5,
                "capability": "estructural",
                "area_seguimiento": "Accion Intersectorial (Operación Territorial y Promoción de la Salud)",
                "documento_probatorio": "Análisis Situacional de Salud Distrital ASIS, Diagnóstico Situacional",
                "options": [
                    {"value": 0, "label": "No se cuenta con ASIS"},
                    {"value": 1, "label": "Existe ASIS sin datos actualizados"},
                    {"value": 2, "label": "Existe ASIS con datos parciales"},
                    {"value": 3, "label": "Existe ASIS completo sin priorización"},
                    {"value": 4, "label": "Existe ASIS priorizado sin planes de acción"},
                    {"value": 5, "label": "Existe ASIS priorizado con planes de acción integrados"},
                ]
            },
            {
                "id": "fesp_1_2",
                "code": "2",
                "name": "Sesiones de evaluación y fortalecimiento de PAEs",
                "description": "Sesiones de evaluación de PAEs orientadas a brechas detectadas en el ASIS",
                "max_points": 5,
                "capability": "desempeno",
                "area_seguimiento": "Programas y Estrategias Prioritarias",
                "documento_probatorio": "Minutas de sesión jurisdiccional/distrital",
                "options": [
                    {"value": 0, "label": "No se realizan sesiones de evaluación"},
                    {"value": 1, "label": "Sesiones esporádicas sin estructura"},
                    {"value": 2, "label": "Sesiones periódicas sin seguimiento a brechas"},
                    {"value": 3, "label": "Sesiones con evaluación de proceso operativo"},
                    {"value": 4, "label": "Incluye indicadores epidemiológicos de impacto"},
                    {"value": 5, "label": "Evaluación integral con barreras y facilitadores"},
                ]
            },
            {
                "id": "fesp_1_10",
                "code": "10",
                "name": "Monitoreo y evaluación de intervenciones de políticas",
                "description": "Monitoreo de efectividad de las intervenciones de políticas en salud colectiva",
                "max_points": 5,
                "capability": "supervision",
                "area_seguimiento": "Gestión de la salud individual y colectiva (Gerencia) y Programas y Estrategias",
                "documento_probatorio": "Minutas con acuerdos y compromisos",
                "options": [
                    {"value": 0, "label": "No se realiza monitoreo de intervenciones"},
                    {"value": 1, "label": "Monitoreo básico sin seguimiento"},
                    {"value": 2, "label": "Monitoreo con minutas sin acuerdos"},
                    {"value": 3, "label": "Minutas con acuerdos sin seguimiento"},
                    {"value": 4, "label": "Minutas con acuerdos y seguimiento parcial"},
                    {"value": 5, "label": "Seguimiento completo de acuerdos y compromisos"},
                ]
            },
        ]
    },
    "fesp_2": {
        "id": "fesp_2",
        "number": 2,
        "name": "Vigilancia, control y gestión de riesgos",
        "description": "Capacidad para identificar, analizar y gestionar riesgos a la salud pública",
        "max_points": 10,
        "policy_cycle": "evaluacion",
        "items": [
            {
                "id": "fesp_2_4",
                "code": "4",
                "name": "Disposición y uso integral de sistemas de información",
                "description": "Uso de sistemas de información de salud colectiva y atención médica",
                "max_points": 5,
                "capability": "estructural",
                "area_seguimiento": "Información en Salud y Vigilancia Epidemiológica (Inteligencia)",
                "documento_probatorio": "Acceso y uso de plataformas federales y locales",
                "options": [
                    {"value": 0, "label": "No se utilizan sistemas de información"},
                    {"value": 1, "label": "Uso parcial de sistemas federales"},
                    {"value": 2, "label": "Uso de sistemas federales y locales fragmentados"},
                    {"value": 3, "label": "Sistemas integrados sin uso en decisiones"},
                    {"value": 4, "label": "Uso para monitoreo y evaluación"},
                    {"value": 5, "label": "Uso integral para toma de decisiones"},
                ]
            },
            {
                "id": "fesp_2_5",
                "code": "5",
                "name": "Elaboración y uso local de Canales endémicos",
                "description": "Canal endémico y difusión de situación epidemiológica",
                "max_points": 5,
                "capability": "estructural",
                "area_seguimiento": "Vigilancia Epidemiológica (Inteligencia)",
                "documento_probatorio": "Canal endémico y difusión",
                "options": [
                    {"value": 0, "label": "No se elaboran canales endémicos"},
                    {"value": 1, "label": "Elaboración esporádica sin uso"},
                    {"value": 2, "label": "Elaboración periódica sin difusión"},
                    {"value": 3, "label": "Difusión a equipo gerencial"},
                    {"value": 4, "label": "Uso para identificación de alertas"},
                    {"value": 5, "label": "Uso integral para toma de decisiones"},
                ]
            },
        ]
    },
    "fesp_3": {
        "id": "fesp_3",
        "number": 3,
        "name": "Investigación y gestión del conocimiento",
        "description": "Capacidad para generar, aplicar y difundir conocimiento en salud pública",
        "max_points": 5,
        "policy_cycle": "evaluacion",
        "items": [
            {
                "id": "fesp_3_8",
                "code": "8",
                "name": "Desarrollo de investigación operativa",
                "description": "Investigación operativa para responder a brechas de salud en territorio",
                "max_points": 5,
                "capability": "desempeno",
                "area_seguimiento": "Educación y Capacitación (Gerencia)",
                "documento_probatorio": "Protocolos de investigación, informes técnicos o publicaciones",
                "options": [
                    {"value": 0, "label": "No se realiza investigación operativa"},
                    {"value": 1, "label": "Investigación solo por instancias externas"},
                    {"value": 2, "label": "Investigación interna sin foco en brechas"},
                    {"value": 3, "label": "Investigación acorde a brechas identificadas"},
                    {"value": 4, "label": "Investigación con colaboración externa"},
                    {"value": 5, "label": "Investigación de temática del PAE con publicación"},
                ]
            },
        ]
    },
    "fesp_4": {
        "id": "fesp_4",
        "number": 4,
        "name": "Políticas, legislación y marcos regulatorios",
        "description": "Capacidad para desarrollar e implementar políticas y marcos regulatorios en salud",
        "max_points": 20,
        "policy_cycle": "desarrollo",
        "items": [
            {
                "id": "fesp_4_13",
                "code": "13",
                "name": "Capacidad para operar estrategias o políticas públicas en salud",
                "description": "Operación de políticas públicas locales, estatales o federales",
                "max_points": 5,
                "capability": "formal",
                "area_seguimiento": "Soporte Comunitario (Operación Territorial y Promoción de la salud)",
                "documento_probatorio": "Minutas, documento de estrategia, Indicadores de política pública",
                "options": [
                    {"value": 0, "label": "No se operan políticas públicas"},
                    {"value": 1, "label": "Conocimiento de políticas sin operación"},
                    {"value": 2, "label": "Operación parcial sin recursos"},
                    {"value": 3, "label": "Operación con recursos estatales"},
                    {"value": 4, "label": "Operación con recursos de múltiples fuentes"},
                    {"value": 5, "label": "Política basada en acuerdos de grupo colegiado"},
                ]
            },
            {
                "id": "fesp_4_17",
                "code": "17",
                "name": "Integrar activos en territorio a procesos locales de salud",
                "description": "Identificar y fortalecer activos en territorio (recursos humanos, materiales, culturales)",
                "max_points": 5,
                "capability": "estructural",
                "area_seguimiento": "Soporte comunitario (Operación Territorial y Promoción de la salud)",
                "documento_probatorio": "Red de Servicios, capacidad resolutiva",
                "options": [
                    {"value": 0, "label": "No se identifican activos en territorio"},
                    {"value": 1, "label": "Identificación parcial de activos"},
                    {"value": 2, "label": "Activos identificados sin integración"},
                    {"value": 3, "label": "Integración parcial a procesos de salud"},
                    {"value": 4, "label": "Red de servicios conocida del sector público"},
                    {"value": 5, "label": "Red de servicios del PAE completa e institucional"},
                ]
            },
            {
                "id": "fesp_4_21",
                "code": "21",
                "name": "Comités Municipales Intersectoriales",
                "description": "Vinculación e incentivo de Comités Municipales para gestión territorial",
                "max_points": 5,
                "capability": "formal",
                "area_seguimiento": "Acción intersectorial/intrasectorial",
                "documento_probatorio": "Acta de instalación",
                "options": [
                    {"value": 0, "label": "No existen comités municipales"},
                    {"value": 1, "label": "Comités sin acta de instalación"},
                    {"value": 2, "label": "Comités instalados sin sesiones"},
                    {"value": 3, "label": "Comités con sesiones esporádicas"},
                    {"value": 4, "label": "Comités en municipios prioritarios"},
                    {"value": 5, "label": "Comités intersectoriales activos del PAE"},
                ]
            },
            {
                "id": "fesp_4_30",
                "code": "30",
                "name": "Farmacovigilancia y condiciones de almacenamiento",
                "description": "Cumplimiento de medicamentos con requisitos de farmacovigilancia NOM-220-SSA1-2016",
                "max_points": 5,
                "capability": "formal",
                "area_seguimiento": "Logística",
                "documento_probatorio": "NOM-220-SSA1-2016. Documentos fuente de evaluaciones",
                "options": [
                    {"value": 0, "label": "No se realiza control de medicamentos"},
                    {"value": 1, "label": "Control parcial sin normativa"},
                    {"value": 2, "label": "Control de inventarios básico"},
                    {"value": 3, "label": "Control de condiciones de almacenamiento"},
                    {"value": 4, "label": "Control de caducidades implementado"},
                    {"value": 5, "label": "Cumplimiento total de farmacovigilancia"},
                ]
            },
        ]
    },
    "fesp_5": {
        "id": "fesp_5",
        "number": 5,
        "name": "Participación y movilización social",
        "description": "Capacidad para promover la participación social en salud",
        "max_points": 15,
        "policy_cycle": "desarrollo",
        "items": [
            {
                "id": "fesp_5_12",
                "code": "12",
                "name": "Integrar otros sectores en operación de estrategias de salud",
                "description": "Integración multisectorial en políticas de salud colectiva local",
                "max_points": 5,
                "capability": "estructural",
                "area_seguimiento": "Rectoría Operativa (Gerencia), Supervisión, Programas y Estrategias",
                "documento_probatorio": "Acta de instalación, reuniones ordinarias",
                "options": [
                    {"value": 0, "label": "No se integran otros sectores"},
                    {"value": 1, "label": "Participación solo del sector salud"},
                    {"value": 2, "label": "Participación de algunas instituciones"},
                    {"value": 3, "label": "Grupo colegiado instalado"},
                    {"value": 4, "label": "Reuniones con listas de asistencia y minutas"},
                    {"value": 5, "label": "Grupo colegiado con acuerdos y compromisos"},
                ]
            },
            {
                "id": "fesp_5_16",
                "code": "16",
                "name": "Integración de planes locales de salud de participación social",
                "description": "Seguimiento de planes generados en asambleas y estrategias de participación social",
                "max_points": 5,
                "capability": "formal",
                "area_seguimiento": "Soporte comunitario (Operación Territorial y Promoción de la salud)",
                "documento_probatorio": "Plan de acción, evidencia de acuerdos de asambleas",
                "options": [
                    {"value": 0, "label": "No existen planes locales de salud"},
                    {"value": 1, "label": "Planes sin registro legal"},
                    {"value": 2, "label": "Planes registrados sin seguimiento"},
                    {"value": 3, "label": "Grupos distritales identificados"},
                    {"value": 4, "label": "Grupos con participación del programa"},
                    {"value": 5, "label": "Grupos distritales activos para el PAE"},
                ]
            },
            {
                "id": "fesp_5_20",
                "code": "20",
                "name": "Integración de organizaciones de sociedad civil",
                "description": "Integración de ONGs y movimientos sociales en planes locales de salud",
                "max_points": 5,
                "capability": "estructural",
                "area_seguimiento": "Soporte comunitario, Acción intersectorial y Supervisión",
                "documento_probatorio": "Minutas y documentos de convocatoria",
                "options": [
                    {"value": 0, "label": "No se integran organizaciones civiles"},
                    {"value": 1, "label": "Identificación de organizaciones sin vinculación"},
                    {"value": 2, "label": "Vinculación parcial sin acciones conjuntas"},
                    {"value": 3, "label": "Organizaciones integradas al diagnóstico"},
                    {"value": 4, "label": "Acciones conjuntas esporádicas"},
                    {"value": 5, "label": "Acciones conjuntas con asociaciones en el PAE"},
                ]
            },
        ]
    },
    "fesp_6": {
        "id": "fesp_6",
        "number": 6,
        "name": "Desarrollo de los recursos humanos para la salud",
        "description": "Capacidad para desarrollar y gestionar el talento humano en salud",
        "max_points": 10,
        "policy_cycle": "asignacion",
        "items": [
            {
                "id": "fesp_6_23",
                "code": "23",
                "name": "Identificación y atención de necesidades de capacitación",
                "description": "Evaluaciones periódicas de capacitación para personal de salud",
                "max_points": 5,
                "capability": "desempeno",
                "area_seguimiento": "Educación y capacitación (Gerencia)",
                "documento_probatorio": "Evaluaciones periódicas de capacitación",
                "options": [
                    {"value": 0, "label": "No se identifican necesidades de capacitación"},
                    {"value": 1, "label": "Identificación anual sin plan"},
                    {"value": 2, "label": "Plan de capacitación sin ejecución"},
                    {"value": 3, "label": "Capacitaciones aisladas"},
                    {"value": 4, "label": "Cédula de necesidades de capacitación"},
                    {"value": 5, "label": "Programa de capacitación para fortalecer el PAE"},
                ]
            },
            {
                "id": "fesp_6_25",
                "code": "25",
                "name": "Colaboración con instituciones educativas",
                "description": "Colaboración con instituciones educativas, ONGs y organismos internacionales para formación",
                "max_points": 5,
                "capability": "estructural",
                "area_seguimiento": "Educación y capacitación (Gerencia)",
                "documento_probatorio": "Carta programática, cartas descriptivas, temarios, listas de asistencia",
                "options": [
                    {"value": 0, "label": "No existe colaboración educativa"},
                    {"value": 1, "label": "Colaboración informal sin convenio"},
                    {"value": 2, "label": "Convenio con una institución"},
                    {"value": 3, "label": "Convenios con múltiples instituciones"},
                    {"value": 4, "label": "Oficios de invitación a colaboración"},
                    {"value": 5, "label": "Colaboración activa para profesionalización"},
                ]
            },
        ]
    },
    "fesp_7": {
        "id": "fesp_7",
        "number": 7,
        "name": "Medicamentos y otras tecnologías de salud",
        "description": "Capacidad para gestionar medicamentos y tecnologías de salud",
        "max_points": 5,
        "policy_cycle": "asignacion",
        "items": [
            {
                "id": "fesp_7_28",
                "code": "28",
                "name": "Análisis y mejora de cadenas de suministros",
                "description": "Análisis de logística de insumos para atención médica y salud colectiva",
                "max_points": 5,
                "capability": "estructural",
                "area_seguimiento": "Cadena de Suministros (Logística)",
                "documento_probatorio": "Formatos de distribución y consumo, procesos logísticos",
                "options": [
                    {"value": 0, "label": "No existe análisis de cadena de suministros"},
                    {"value": 1, "label": "Análisis básico sin mejoras"},
                    {"value": 2, "label": "Formatos de distribución parciales"},
                    {"value": 3, "label": "Control de consumo de insumos"},
                    {"value": 4, "label": "Procesos logísticos documentados"},
                    {"value": 5, "label": "Administración integral de insumos del programa"},
                ]
            },
        ]
    },
    "fesp_8": {
        "id": "fesp_8",
        "number": 8,
        "name": "Financiamiento de la salud",
        "description": "Capacidad para gestionar y asignar recursos financieros en salud",
        "max_points": 5,
        "policy_cycle": "asignacion",
        "items": [
            {
                "id": "fesp_8_22",
                "code": "22",
                "name": "Diagnóstico situacional de profesionales de la salud",
                "description": "Diagnóstico de profesionales para atención médica y salud colectiva",
                "max_points": 5,
                "capability": "estructural",
                "area_seguimiento": "Infraestructura y Recurso humano en salud (Logística)",
                "documento_probatorio": "Base de datos de prestadores de servicios",
                "options": [
                    {"value": 0, "label": "No existe diagnóstico de profesionales"},
                    {"value": 1, "label": "Diagnóstico parcial sin base de datos"},
                    {"value": 2, "label": "Base de datos incompleta"},
                    {"value": 3, "label": "Base de datos del sector público"},
                    {"value": 4, "label": "Incluye tipo de contratación y espacios"},
                    {"value": 5, "label": "Red de prestadores del PAE en territorios"},
                ]
            },
        ]
    },
    "fesp_9": {
        "id": "fesp_9",
        "number": 9,
        "name": "Acceso a los servicios integrales y de calidad",
        "description": "Capacidad para garantizar acceso equitativo a servicios de salud de calidad",
        "max_points": 20,
        "policy_cycle": "acceso",
        "items": [
            {
                "id": "fesp_9_32",
                "code": "32",
                "name": "Conocimiento y gestión de demanda de atención médica",
                "description": "Medición y gestión de la demanda de atención médica en territorio",
                "max_points": 5,
                "capability": "estructural",
                "area_seguimiento": "CECOSABI, Gerencia",
                "documento_probatorio": "Excel, bases de datos, registros o plataformas",
                "options": [
                    {"value": 0, "label": "No se conoce la demanda de atención"},
                    {"value": 1, "label": "Conocimiento parcial sin registros"},
                    {"value": 2, "label": "Registros básicos de consultas"},
                    {"value": 3, "label": "Base de datos de servicios"},
                    {"value": 4, "label": "Seguimiento de productividad"},
                    {"value": 5, "label": "Seguimiento productivo del PAE (ej. consultas por psicólogo)"},
                ]
            },
            {
                "id": "fesp_9_33",
                "code": "33",
                "name": "Mecanismos para garantizar acceso a servicios",
                "description": "Operación de mecanismos para garantizar acceso a atención médica",
                "max_points": 5,
                "capability": "formal",
                "area_seguimiento": "CECOSABI",
                "documento_probatorio": "Documento para evaluación de acceso, lineamientos",
                "options": [
                    {"value": 0, "label": "No existen mecanismos de acceso"},
                    {"value": 1, "label": "Mecanismos informales sin documentar"},
                    {"value": 2, "label": "Lineamientos parciales"},
                    {"value": 3, "label": "Estrategia documentada"},
                    {"value": 4, "label": "Evaluación de acceso implementada"},
                    {"value": 5, "label": "Acceso a plataforma de gestión clínica del PAE"},
                ]
            },
            {
                "id": "fesp_9_34",
                "code": "34",
                "name": "Evaluación del acceso integral a servicios de salud",
                "description": "Evaluación de acceso a servicios de salud colectiva y atención médica",
                "max_points": 5,
                "capability": "supervision",
                "area_seguimiento": "Gestión de la salud individual y colectiva (Gerencia), Logística",
                "documento_probatorio": "Herramienta de evaluación, cédulas de supervisión",
                "options": [
                    {"value": 0, "label": "No se evalúa el acceso"},
                    {"value": 1, "label": "Evaluación esporádica"},
                    {"value": 2, "label": "Cédula de supervisión general"},
                    {"value": 3, "label": "Cédula de supervisión del PAE"},
                    {"value": 4, "label": "Evaluación de productividad"},
                    {"value": 5, "label": "Cédula del PAE evaluada en el último año"},
                ]
            },
            {
                "id": "fesp_9_36",
                "code": "36",
                "name": "Acceso a servicios para grupos vulnerables",
                "description": "Garantizar acceso a servicios de salud colectiva en grupos vulnerables",
                "max_points": 5,
                "capability": "estructural",
                "area_seguimiento": "Gestión de la salud individual y colectiva (Gerencia)",
                "documento_probatorio": "Ferias de la Salud",
                "options": [
                    {"value": 0, "label": "No se atienden grupos vulnerables"},
                    {"value": 1, "label": "Atención esporádica sin estrategia"},
                    {"value": 2, "label": "Estrategia parcial de atención"},
                    {"value": 3, "label": "Ferias de salud generales"},
                    {"value": 4, "label": "Ferias con enfoque del PAE"},
                    {"value": 5, "label": "Participación del programa en ferias a poblaciones vulnerables"},
                ]
            },
        ]
    },
    "fesp_10": {
        "id": "fesp_10",
        "number": 10,
        "name": "Promoción de la salud y comportamientos saludables",
        "description": "Capacidad para promover la salud y estilos de vida saludables",
        "max_points": 5,
        "policy_cycle": "acceso",
        "items": [
            {
                "id": "fesp_10_40",
                "code": "40",
                "name": "Estrategia distrital de entornos de salud y bienestar",
                "description": "Creación de entornos saludables abordando temas ambientales, salud mental, enfermedades",
                "max_points": 5,
                "capability": "estructural",
                "area_seguimiento": "Operaciones, Gerencia (Enlace académico de capacitación)",
                "documento_probatorio": "Estrategia distrital, convocatoria, formatos de trabajo",
                "options": [
                    {"value": 0, "label": "No existe estrategia de entornos saludables"},
                    {"value": 1, "label": "Estrategia parcial sin documentar"},
                    {"value": 2, "label": "Estrategia documentada sin implementación"},
                    {"value": 3, "label": "Convocatoria y formatos de trabajo"},
                    {"value": 4, "label": "Implementación con fotografías"},
                    {"value": 5, "label": "Estrategia de entornos saludables bajo criterios del PAE"},
                ]
            },
        ]
    },
    "fesp_11": {
        "id": "fesp_11",
        "number": 11,
        "name": "Gobernanza y rectoría institucional",
        "description": "Capacidad para ejercer rectoría y gobernanza del sistema de salud",
        "max_points": 5,
        "policy_cycle": "acceso",
        "items": [
            {
                "id": "fesp_11_38",
                "code": "38",
                "name": "Modelo de resiliencia del sistema distrital de salud",
                "description": "Capacidad para resistir, tolerar, absorber, recuperarse ante ocurrencias adversas",
                "max_points": 5,
                "capability": "estructural",
                "area_seguimiento": "Gerencia, Operaciones, Logística, Inteligencia y CECOSABI",
                "documento_probatorio": "Manual de organización, flujograma de emergencias, Minuta del Comité Estatal de Seguridad",
                "options": [
                    {"value": 0, "label": "No existe modelo de resiliencia"},
                    {"value": 1, "label": "Manual de organización básico"},
                    {"value": 2, "label": "Flujograma de emergencias parcial"},
                    {"value": 3, "label": "Flujograma completo de emergencias"},
                    {"value": 4, "label": "Participación del PAE en contingencias"},
                    {"value": 5, "label": "Inclusión del PAE en el CESS"},
                ]
            },
        ]
    },
}


def get_all_items():
    """Get a flat list of all evaluation items"""
    items = []
    for fesp_id, fesp in FESP_ITEMS.items():
        for item in fesp["items"]:
            items.append({
                **item,
                "fesp_id": fesp_id,
                "fesp_number": fesp["number"],
                "fesp_name": fesp["name"],
                "policy_cycle": fesp["policy_cycle"]
            })
    return items


def get_total_max_points():
    """Get the total maximum points for the instrument"""
    return sum(fesp["max_points"] for fesp in FESP_ITEMS.values())


def calculate_compliance_level(percentage: float) -> dict:
    """Get compliance level based on percentage"""
    for level_key, level in COMPLIANCE_LEVELS.items():
        if level["min"] <= percentage <= level["max"]:
            return level
    # Default to highest if above 100%
    return COMPLIANCE_LEVELS["avanzado"]


def get_capabilities():
    """Get list of institutional capabilities"""
    return ["formal", "estructural", "desempeno", "supervision"]


def get_policy_cycles():
    """Get list of policy cycles"""
    return ["evaluacion", "desarrollo", "asignacion", "acceso"]


def get_fesp_by_id(fesp_id: str):
    """Get FESP definition by ID"""
    return FESP_ITEMS.get(fesp_id)


def get_item_by_id(item_id: str):
    """Get item definition by ID"""
    for item in get_all_items():
        if item["id"] == item_id:
            return item
    return None
