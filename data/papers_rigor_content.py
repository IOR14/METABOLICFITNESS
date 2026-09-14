"""Revisiones clínicas extensas y trazables de Metabolic Fitness.

El módulo conserva los diez slugs públicos. Las cifras se presentan con su
contexto metodológico y nunca sustituyen evaluación, diagnóstico ni
prescripción individual. Las referencias usan exclusivamente URLs verificadas
de la lista editorial aprobada.
"""

from __future__ import annotations


REFS = {
    "hf_trial": {
        "title": "Physical training in stable chronic heart failure: fitness and leg-muscle ultrastructure",
        "url": "https://pubmed.ncbi.nlm.nih.gov/7722116/",
    },
    "hf_review": {
        "title": "Exercise training in heart failure: mechanisms and prescription",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6250583/",
    },
    "bone_optimal": {
        "title": "Optimal resistance-training parameters for bone mineral density after menopause",
        "url": "https://pubmed.ncbi.nlm.nih.gov/40420105/",
    },
    "bone_dynamic": {
        "title": "Dynamic resistance exercise and bone mineral density after menopause",
        "url": "https://pubmed.ncbi.nlm.nih.gov/32399891/",
    },
    "bone_update": {
        "title": "Exercise training and bone mineral density in postmenopausal women",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36749350/",
    },
    "hiit_bp": {
        "title": "HIIT versus continuous training on blood pressure in hypertension",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36550888/",
    },
    "hiit_prehtn": {
        "title": "HIIT versus continuous training in prehypertension and hypertension",
        "url": "https://pubmed.ncbi.nlm.nih.gov/29949110/",
    },
    "hiit_capacity": {
        "title": "HIIT, exercise capacity, blood pressure and autonomic responses",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36529986/",
    },
    "hiit_older": {
        "title": "High-intensity interval training and blood pressure in older adults",
        "url": "https://pubmed.ncbi.nlm.nih.gov/34921916/",
    },
    "hiit_effectiveness": {
        "title": "Effectiveness of HIIT versus continuous training in hypertensive patients",
        "url": "https://pubmed.ncbi.nlm.nih.gov/32125550/",
    },
    "microbiota": {
        "title": "Exercise and gut microbiota in adults with overweight or obesity",
        "url": "https://pubmed.ncbi.nlm.nih.gov/40765072/",
    },
    "fermentation": {
        "title": "Gut microbiome fermentation and efficacy of exercise for diabetes prevention",
        "url": "https://pubmed.ncbi.nlm.nih.gov/31786155/",
    },
    "copd": {
        "title": "Exercise-based pulmonary rehabilitation in stable COPD",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36348964/",
    },
    "copd_severe": {
        "title": "Exercise-based pulmonary rehabilitation in severe and very severe COPD",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36946384/",
    },
    "parkinson_meta": {
        "title": "Physiotherapy in Parkinson's disease: meta-analysis of treatment modalities",
        "url": "https://pubmed.ncbi.nlm.nih.gov/32917125/",
    },
    "parkinson_plasticity": {
        "title": "Exercise-induced neuroplasticity in Parkinson's disease",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7079218/",
    },
    "parkinson_cognition": {
        "title": "Exercise, cognition and neuroplasticity in Parkinson's disease",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10272626/",
    },
    "grip": {
        "title": "Grip strength and all-cause, cardiovascular and cancer mortality",
        "url": "https://pubmed.ncbi.nlm.nih.gov/28549705/",
    },
    "grip_thresholds": {
        "title": "Handgrip-strength thresholds for all-cause, cancer and cardiovascular mortality",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36332759/",
    },
    "cancer_fitness": {
        "title": "Muscle strength, cardiorespiratory fitness and mortality after cancer diagnosis",
        "url": "https://pubmed.ncbi.nlm.nih.gov/39837589/",
    },
    "cancer_trials": {
        "title": "Physical activity and all-cause mortality in cancer: randomized trials",
        "url": "https://pubmed.ncbi.nlm.nih.gov/41894932/",
    },
    "hypertrophy": {
        "title": "Resistance-training repetition duration and muscle hypertrophy",
        "url": "https://pubmed.ncbi.nlm.nih.gov/25601394/",
    },
    "postdinner": {
        "title": "Postdinner resistance exercise and postprandial risk factors in type 2 diabetes",
        "url": "https://pubmed.ncbi.nlm.nih.gov/25539939/",
    },
}


def _section(topic: str, heading: str, evidence: str, mechanism: str, practice: str) -> dict:
    """Construye tres párrafos largos: evidencia, mecanismo y transferencia."""
    return {
        "heading": heading,
        "html": (
            f"<p><strong>Evidencia y magnitud.</strong> {evidence} La lectura clínica exige separar cambio "
            f"estadístico de cambio importante para la persona con {topic}. Una MD conserva las unidades originales; "
            "una SMD expresa la diferencia en desviaciones estándar; un HR compara tasas durante el seguimiento, y "
            "ninguno de ellos informa por sí solo beneficio absoluto. Un IC95% estrecho aumenta precisión, mientras "
            "uno amplio o que cruza 0 obliga a reconocer compatibilidad con efectos menores, nulos o incluso opuestos. "
            "También importan duración, supervisión, adherencia y comparador: 8-12 semanas pueden demostrar adaptación "
            "fisiológica, pero no equivalen a prevención de eventos durante años. Las revisiones de revistas clínicas "
            "deben interpretarse desde sus ensayos, no desde el titular; heterogeneidad I² de 50-75% suele indicar que "
            "población, dosis o medición explican una parte relevante de la dispersión. Por eso una media de grupo no "
            "se convierte automáticamente en promesa individual, aunque sí permite fijar una expectativa cuantitativa "
            "y decidir qué resultado volver a medir.</p>"
            f"<p><strong>Fisiología y dosificación.</strong> {mechanism} La adaptación requiere una perturbación "
            "suficiente, recuperación y repetición; aumentar intensidad sin volumen tolerado suele elevar síntomas "
            "antes que capacidad. En términos operativos se documentan frecuencia semanal, minutos, carga externa, "
            "RPE o Borg, repeticiones en reserva y respuesta a 24-48 horas. Una progresión de 5-10% puede ser razonable "
            "cuando técnica y síntomas permanecen estables, pero no constituye una ley: medicación, inflamación, sueño, "
            "energía disponible y comorbilidad alteran la relación dosis-respuesta. Los mecanismos —señalización por "
            "AMPK y PGC-1α, mecanotransducción, función endotelial, control autonómico o aprendizaje neural según el "
            "tejido— son plausibilidad biológica, no sustitutos de desenlaces. Se busca concordancia entre un marcador "
            "objetivo, una tarea funcional y la experiencia del paciente; por ejemplo, 5-10% más carga con menor Borg "
            "y recuperación en menos de 24 horas es más convincente que una única medición favorable.</p>"
            f"<p><strong>Aplicación en Latinoamérica.</strong> {practice} La implementación debe anticipar distancia, "
            "costo, calor, seguridad barrial, alfabetización sanitaria, disponibilidad de equipamiento y fragmentación "
            "entre especialidades. Una evaluación inicial de 30-45 minutos puede producir un mínimo conjunto útil: "
            "síntomas, presión arterial, medicación, una prueba funcional reproducible y una meta significativa. Cuando "
            "no existe tecnología avanzada, repetir el mismo protocolo de campo cada 4-8 semanas ofrece mejor decisión "
            "que acumular mediciones incompatibles. Un esquema híbrido de 1 contacto supervisado y 2-4 sesiones "
            "domiciliarias por semana, registro en papel o teléfono y llamada ante señales de alarma puede ampliar "
            "cobertura sin fingir equivalencia con vigilancia hospitalaria. La meta de adherencia ≥75% se conversa, no "
            "se impone; si la dosis teórica fracasa por transporte o trabajo, se redistribuye en bloques de 10-20 "
            "minutos. Toda recomendación debe incluir qué hacer, cómo progresar, cuándo pausar y a quién contactar.</p>"
        ),
    }


def _body(spec: dict) -> dict:
    sections = [
        _section(spec["topic"], heading, evidence, mechanism, practice)
        for heading, evidence, mechanism, practice in spec["sections"]
    ]
    return {
        "abstract": " ".join(spec["abstract"]),
        "intro": (
            f"<p>{spec['intro'][0]} En {spec['topic']}, el razonamiento parte del fenotipo y no de una receta "
            "universal. La carga interna —disnea, pulso, presión, RPE, dolor y recuperación— se contrasta con la "
            "carga externa —minutos, velocidad, vatios, kilogramos o repeticiones— para saber si el estímulo fue "
            "suficiente y tolerable. Este marco evita confundir una asociación epidemiológica con causalidad y una "
            "media de metaanálisis con respuesta garantizada. También obliga a registrar el tratamiento concurrente, "
            "porque cambios farmacológicos, nutricionales o del sueño pueden explicar una parte importante del efecto.</p>"
            f"<p>{spec['intro'][1]} La pregunta práctica no es solamente si el ejercicio funciona, sino para quién, "
            "con qué dosis, contra qué comparador y durante cuánto tiempo. Se integran resultados relativos —SMD, MD "
            "o HR con IC95%— con cambios absolutos que la persona puede reconocer: caminar más, levantarse con menor "
            "esfuerzo, tolerar una jornada o recuperar participación. En Latinoamérica, donde el acceso a pruebas "
            "especializadas es desigual, la estandarización de medidas sencillas y la coordinación entre medicina, "
            "kinesiología, nutrición y comunidad son parte de la eficacia, no detalles administrativos. Las secciones "
            "siguientes traducen evidencia, mecanismos y límites en decisiones auditables.</p>"
        ),
        "sections": sections,
        "clinical": (
            f"<p>{spec['clinical'][0]} La primera prescripción funciona como una hipótesis clínica: define dosis, "
            "respuesta esperada y criterio de modificación. Se comienza por debajo del máximo tolerable, se observan "
            "síntomas durante y 24-48 horas después, y se progresa una variable a la vez. Si no aparece respuesta en "
            "8-12 semanas, antes de etiquetar a alguien como no respondedor se revisan adherencia, fidelidad de la "
            "dosis, técnica, medicación, nutrición, sueño y enfermedad intercurrente. Una mejoría de 5-10% en una prueba "
            "reproducible puede ser clínicamente útil cuando coincide con más participación, incluso si otro biomarcador "
            "permanece estable.</p>"
            f"<p>{spec['clinical'][1]} En la práctica latinoamericana se necesita una ruta explícita para banderas "
            "rojas, una versión domiciliaria de la sesión y un método de seguimiento que no dependa de tecnología "
            "costosa. Presión, Borg/RPE, repeticiones, tiempo y síntomas caben en una hoja y permiten decisiones "
            "longitudinales. Los porcentajes, HR y SMD de la literatura informan la conversación, pero no reemplazan "
            "preferencias ni riesgo basal. El objetivo final es sostener una dosis que mejore reserva funcional y "
            "autonomía sin ocultar incertidumbre ni prometer prevención de eventos que el diseño de los estudios no "
            "puede demostrar.</p>"
        ),
        "guidelines_html": "<ul>" + "".join(f"<li>{item}</li>" for item in spec["guidelines"]) + "</ul>",
        "keypoints": spec["keypoints"],
        "refs": [REFS[key].copy() for key in spec["refs"]],
    }


SPECS = {
    "mitocondrias-ejercicio-e-insuficiencia-cardiaca-rehabilitacion-metabolica-de-precision": {
        "topic": "insuficiencia cardiaca crónica",
        "abstract": [
            "La intolerancia al esfuerzo en insuficiencia cardiaca no se explica únicamente por gasto cardiaco reducido.",
            "El músculo esquelético desarrolla menor densidad capilar, pérdida de fibras oxidativas y disfunción mitocondrial que adelantan acidosis, aferencia ergorrefleja y disnea.",
            "El entrenamiento aeróbico y de fuerza puede elevar VO₂peak, mejorar economía y recuperar tareas aun cuando la fracción de eyección cambie poco.",
            "El ensayo clásico de entrenamiento describió adaptación cardiorrespiratoria y ultraestructural periférica, coherente con un efecto sistémico.",
            "La magnitud individual depende de congestión, cronotropismo, hierro, fragilidad, nutrición, medicación y dosis efectivamente completada.",
            "Una rehabilitación de precisión combina estratificación, intervalos cuando son necesarios, fuerza progresiva y vigilancia de presión, peso, síntomas y recuperación.",
            "El objetivo no es una sesión máxima, sino semanas repetibles que conviertan reserva metabólica en autonomía y menor carga sintomática.",
        ],
        "intro": [
            "<strong>El músculo periférico es órgano diana y determinante pronóstico.</strong> Hipoperfusión episódica, inflamación, inactividad y menor biogénesis mitocondrial elevan el costo de ATP por tarea.",
            "Dos personas con fracción de eyección semejante pueden diferir más de 30% en capacidad funcional; ergoespirometría, caminata de 6 minutos, sit-to-stand y fuerza ayudan a localizar la limitación.",
        ],
        "sections": [
            ("Fenotipo periférico y mitocondrias", "El ensayo de <em>JACC</em> sobre entrenamiento estable documentó mejoría del fitness y de anomalías ultraestructurales del músculo; ganancias de VO₂peak de 1-2 ml·kg⁻¹·min⁻¹ pueden ser funcionalmente relevantes aunque el IC95% varíe.", "PGC-1α, enzimas oxidativas y capilarización aumentan extracción de O₂; menor ergorreflejo reduce hiperventilación para una carga dada.", "Medir caminata, 30-s sit-to-stand y Borg permite fenotipar cuando no hay prueba cardiopulmonar."),
            ("Prescripción aeróbica continua", "Revisiones cardiovasculares informan aumentos aproximados de 10-20% en capacidad con 3-5 sesiones por semana; la MD debe contrastarse con síntomas y eventos.", "Veinte a 40 minutos a Borg 11-14/20 aumentan volumen plasmático, función endotelial y maquinaria oxidativa sin exigir picos repetidos.", "Caminata en circuito medido o bicicleta comunitaria permiten cuantificar minutos y distancia con bajo costo."),
            ("Intervalos y techo ventilatorio", "Comparaciones de <em>Sports Medicine</em> sugieren cerca de 2 ml·kg⁻¹·min⁻¹ adicionales con HIIT en poblaciones seleccionadas, pero IC95% y selección clínica impiden universalizarlo.", "Bloques de 30-120 segundos distribuyen demanda, limitan acumulación de metabolitos y permiten más trabajo cuando disnea o fatiga periférica cortan el continuo.", "Se introducen tras 2-4 semanas estables, con plan escrito y acceso a evaluación ante angina, síncope o congestión."),
            ("Fuerza y reserva funcional", "Metaanálisis de <em>JAMDA</em> relaciona la menor prensión con mortalidad total, HR 1,41, asociación que no prueba que subir 1 kg reduzca riesgo en proporción fija.", "Dos o tres sesiones, 1-3 series de 8-15 repeticiones a 40-80% de 1RM, aumentan reclutamiento y reducen el costo relativo de levantarse o subir escalones.", "Bandas y cargas domésticas son útiles si se registran; evitar Valsalva y revisar presión, mareo y recuperación."),
            ("Comorbilidad y señales de alarma", "Estudios de rehabilitación suelen excluir descompensación; por ello sus tasas de eventos no representan a quien aumenta 2 kg en 2-3 días, tiene ortopnea nueva o presión inestable.", "Ferropenia, anemia, caquexia, diabetes y betabloqueo alteran transporte de O₂, sustrato y cronotropismo, ensanchando el IC95% de respuesta individual.", "Una ruta compartida con cardiología y atención primaria evita que síntomas nuevos se interpreten como desacondicionamiento."),
            ("Seguimiento y precisión pragmática", "Una mejoría cercana a 30 m en 6MWD, 1 punto menos de Borg o 2 repeticiones más son señales útiles, aunque no intercambiables ni equivalentes a menor HR de hospitalización.", "Reevaluar cada 4-6 semanas permite distinguir adaptación central, periférica y aprendizaje; se progresa duración antes que intensidad si la recuperación supera 24 horas.", "Un modelo híbrido con 1 sesión supervisada y 2-4 domiciliarias amplía acceso, siempre con contacto y criterios de suspensión."),
        ],
        "clinical": ["La rehabilitación es tratamiento de capacidad y no adorno del manejo farmacológico.", "La precisión consiste en medir, ajustar y coordinar, no en depender obligatoriamente de tecnología avanzada."],
        "guidelines": ["Confirmar estabilidad, peso, presión, edema, ortopnea y cambios farmacológicos.", "Acumular 20-40 minutos aeróbicos 3-5 días/semana a Borg 11-14/20.", "Usar intervalos si la disnea impide continuidad y dejar ≥48 horas entre sesiones intensas.", "Entrenar fuerza 2-3 días/semana, comenzando en 40-60% de 1RM estimada.", "Reevaluar cada 4-6 semanas con el mismo protocolo funcional.", "Suspender ante dolor torácico, síncope, disnea de reposo o congestión progresiva."],
        "keypoints": ["La miopatía periférica explica parte sustancial de la intolerancia.", "VO₂peak y función pueden mejorar sin gran cambio ventricular.", "HIIT es una opción seleccionada, no superioridad universal.", "Fuerza y aeróbico tratan componentes complementarios.", "Peso, síntomas y hemodinámica gobiernan la progresión.", "Pruebas de campo hacen viable la precisión regional."],
        "refs": ["hf_trial", "hf_review", "hiit_capacity", "hiit_bp", "grip", "grip_thresholds", "hypertrophy"],
    },
    "entrenamiento-de-fuerza-y-salud-osea-en-mujeres-posmenopausicas-evidencia-clinica-aplicada": {
        "topic": "salud ósea posmenopáusica",
        "abstract": [
            "La caída estrogénica acelera recambio óseo y coincide con pérdida de fuerza, potencia y estabilidad.",
            "El riesgo de fractura depende de resistencia del hueso, carga aplicada y probabilidad de caer, no de densitometría aislada.",
            "Metaanálisis recientes describen SMD 0,88 en columna lumbar, 0,89 en cuello femoral y 0,30 en cadera total con entrenamiento de fuerza.",
            "Los moderadores favorecen cargas ≥70% de 1RM, tres sesiones semanales y programas ≥48 semanas, sin convertir esa dosis objetivo en punto de partida obligatorio.",
            "La mecanotransducción es sitio-específica y necesita tensión novedosa, progresiva y técnicamente controlada.",
            "Fractura vertebral, dolor, experiencia, balance y comorbilidad determinan selección de patrones e impacto.",
            "Ejercicio, proteína, calcio, vitamina D y farmacoterapia cuando corresponde forman capas complementarias de prevención.",
        ],
        "intro": ["<strong>Osteoporosis no significa fragilidad inevitable ni prohibición de cargar.</strong> El hueso responde a deformación y tasa de carga, mientras el músculo reduce el costo de recuperar equilibrio.", "La prescripción debe producir una señal osteogénica y simultáneamente mejorar fuerza, potencia y competencia para evitar caídas."],
        "sections": [
            ("Magnitud por sitio óseo", "La revisión de <em>Journal of Orthopaedic Surgery and Research</em> estimó SMD 0,88 lumbar, 0,89 femoral y 0,30 en cadera total; una SMD no equivale al mismo porcentaje de DMO.", "Composición cortical y trabecular, geometría y dirección de la carga explican respuestas diferentes entre columna, cuello y cadera.", "Cuando DXA seriada no está disponible, se siguen caídas, dolor, cargas y pruebas funcionales sin afirmar cambio densitométrico."),
            ("Intensidad, frecuencia y duración", "Metaanálisis de <em>Osteoporosis International</em> favorecen ≥70% de 1RM, 3 días/semana y ≥48 semanas; efectos a 8-12 semanas reflejan sobre todo músculo, no remodelado óseo completo.", "Dos a cuatro series de 6-12 repeticiones generan tensión; progresar desde RPE 5-7/10 respeta aprendizaje y tiempo de remodelación.", "Mancuernas, bandas y peso corporal sirven para iniciar, pero cargas altas exigen registro y, con frecuencia, gimnasio o supervisión."),
            ("Patrones y mecanotransducción", "Ensayos dinámicos muestran MD/SMD pequeñas pero favorables cuando sentadilla, bisagra, step-up y tracción exponen sitios relevantes durante 6-12 meses.", "Osteocitos traducen deformación en señales Wnt/β-catenina; pausas entre series y variedad direccional evitan una señal monótona.", "Escaleras, levantarse de silla y carga transportada pueden escalarse con recursos locales y técnica verificable."),
            ("Impacto, potencia y prevención de caídas", "Programas multimodales reportan reducción de caídas y mejora de balance, aunque IC95% para fractura suele ser amplio por eventos escasos.", "Saltos bajos, aterrizaje y potencia de cadera entrenan tasa de desarrollo de fuerza; se introducen sólo tras demostrar control.", "En espacios comunitarios se marcan apoyos, se dispone una barra y se evita impacto en dolor agudo o alto riesgo no evaluado."),
            ("Fractura vertebral y seguridad", "Las muestras de ensayos supervisados muestran baja tasa de eventos, pero excluyen parte de las fracturas recientes; ese sesgo limita extrapolación.", "Se evita flexión cargada y torsión rápida no dominada, mientras extensión torácica, cadera y fuerza de piernas preservan función.", "Pérdida de estatura ≥2 cm, dolor óseo nuevo o caída reciente activan derivación y coordinación con metabolismo óseo."),
            ("Más allá de la DXA", "Un cambio pequeño de DMO puede coexistir con 10-20% más fuerza y mejor sit-to-stand; la ausencia de MD densitométrica temprana no implica fracaso.", "Proteína y energía sostienen síntesis muscular; calcio y vitamina D corrigen sustrato, mientras fármacos modifican remodelación por vías distintas.", "Se revisan inseguridad alimentaria, adherencia ≥75% y continuidad anual, priorizando alimentos accesibles y seguimiento."),
        ],
        "clinical": ["La dosis eficaz debe ser suficientemente alta para adaptar y suficientemente gradual para sostener.", "El miedo al movimiento se reemplaza por técnica, competencia y vigilancia proporcionada al riesgo."],
        "guidelines": ["Evaluar fracturas, caídas, dolor, balance y experiencia antes de cargar.", "Progresar hacia 70-85% de 1RM en patrones multiarticulares.", "Entrenar fuerza 2-3 días/semana y sostener ≥48 semanas.", "Añadir balance, potencia e impacto sólo cuando sean seguros.", "Integrar proteína, calcio, vitamina D y tratamiento médico.", "Derivar dolor óseo nuevo, pérdida de estatura o caída con lesión."],
        "keypoints": ["El efecto es sitio-específico.", "SMD no equivale a porcentaje de DMO.", "La dosis objetivo no es la primera sesión.", "Fuerza y balance modifican riesgo de caída.", "Osteoporosis estable no exige inactividad.", "La continuidad anual supera una rutina breve perfecta."],
        "refs": ["bone_optimal", "bone_dynamic", "bone_update", "grip", "grip_thresholds", "hypertrophy", "hf_review"],
    },
    "hiit-versus-entrenamiento-continuo-en-hipertension-arterial-que-dice-la-fisiologia-clinica": {
        "topic": "hipertensión arterial",
        "abstract": [
            "HIIT y entrenamiento continuo moderado reducen la presión arterial frente a inactividad.",
            "Los metaanálisis no muestran una superioridad consistente del HIIT para presión sistólica o diastólica de reposo.",
            "Los intervalos suelen añadir cerca de 2 ml·kg⁻¹·min⁻¹ de VO₂max respecto del continuo en participantes seleccionados.",
            "Presión de consulta, monitoreo ambulatorio, aptitud y tolerancia son desenlaces distintos y no deben mezclarse.",
            "Control basal, medicación, experiencia y respuesta hipertensiva determinan si introducir alta intensidad.",
            "Calentamiento, recuperación activa y criterios de interrupción forman parte de la dosis.",
            "Ambas modalidades pueden coexistir, con elección guiada por seguridad, preferencia y adherencia.",
        ],
        "intro": ["<strong>La pregunta no es qué sigla gana, sino qué estímulo controla presión y aumenta reserva sin riesgo innecesario.</strong>", "Una MD de pocos mmHg puede ser relevante a escala poblacional aunque la comparación HIIT-MICT tenga IC95% que cruce 0."],
        "sections": [
            ("Presión de reposo y ambulatoria", "Metaanálisis en <em>Medicine</em> y <em>Sports Medicine</em> describen reducciones aproximadas de 5-8 mmHg sistólicos y 3-5 diastólicos, sin diferencia robusta HIIT-MICT.", "Ambos métodos reducen resistencia periférica mediante óxido nítrico, menor tono simpático y adaptación renal; la hipotensión posejercicio dura horas.", "Se requieren 5 minutos de reposo, manguito correcto y 2-3 lecturas; MAPA se usa cuando está disponible."),
            ("VO₂max y reserva cardiovascular", "Revisiones de <em>Sports Health</em> encuentran alrededor de 2 ml·kg⁻¹·min⁻¹ más VO₂max con HIIT; la MD depende de intensidad real y semanas.", "Picos de flujo aumentan cizallamiento y volumen sistólico, mientras recuperaciones incompletas acumulan tiempo de alta demanda oxidativa.", "Bicicleta, pendiente o escalón permiten intervalar sin laboratorio, usando RPE 7-9/10 y señales de alarma."),
            ("Protocolos y progresión", "El protocolo 4 × 4 minutos a 85-95% de FCmáx es estudiado, pero series de 1 minuto también muestran efectos con distinta carga total.", "Primero se amplían 20-40 minutos moderados; después se introducen 4-10 intervalos y se progresa una variable 5-10%.", "Una pauta escrita de trabajo/pausa reduce errores cuando la supervisión es intermitente."),
            ("Respuesta hipertensiva y seguridad", "Los ensayos incluyen hipertensión controlada; reposo ≥180/110 mmHg, sistólica de esfuerzo >250 mmHg o síntomas requieren posponer o interrumpir según protocolo.", "Calentamiento de 8-10 minutos amortigua transición simpática; vuelta a la calma limita caída brusca de retorno venoso.", "Equipos calibrados y una ruta de urgencia son condiciones de implementación en centros regionales."),
            ("Medicación y autorregulación", "Betabloqueadores, diuréticos y vasodilatadores cambian frecuencia, hidratación y presión; por ello zonas porcentuales pueden sobrestimar o subestimar dosis.", "Talk test, RPE y carga externa triangulan intensidad; mareo ortostático o recuperación >24-48 horas indican ajuste.", "Se registra horario farmacológico y presión domiciliaria durante 2-4 semanas antes de concluir falta de respuesta."),
            ("Elección compartida y adherencia", "Una reducción sistólica de 5 mmHg importa aunque HIIT no supere a MICT; el beneficio desaparece si la modalidad reduce adherencia por debajo de 70-80%.", "MICT acumula gasto con baja complejidad; HIIT aporta estímulo y eficiencia temporal, y alternarlos distribuye fatiga.", "Turnos, seguridad y clima determinan horarios; bloques de 10-15 minutos pueden completar el volumen semanal."),
        ],
        "clinical": ["HIIT es una herramienta de intensidad y no un antihipertensivo universalmente superior.", "El continuo ofrece una entrada predecible y puede mantenerse junto con uno o dos días intervalados."],
        "guidelines": ["Estandarizar presión basal y confirmar control.", "Construir 2-4 semanas moderadas antes de HIIT.", "Introducir HIIT 1-2 días/semana con ≥48 horas.", "Usar RPE, síntomas y carga además de frecuencia cardiaca.", "Registrar presión domiciliaria y recuperación.", "Interrumpir ante dolor torácico, déficit neurológico, síncope o respuesta extrema."],
        "keypoints": ["HIIT y MICT reducen presión de forma semejante.", "HIIT puede añadir cerca de 2 ml/kg/min de VO₂max.", "La MAPA complementa consulta.", "Calentamiento y pausa son parte de la dosis.", "Medicación modifica zonas de pulso.", "Adherencia decide el efecto real."],
        "refs": ["hiit_bp", "hiit_prehtn", "hiit_capacity", "hiit_older", "hiit_effectiveness", "hf_review", "postdinner"],
    },
    "cronobiologia-del-ejercicio-ritmos-circadianos-y-control-metabolico": {
        "topic": "cronobiología del ejercicio",
        "abstract": [
            "El sistema circadiano organiza temperatura, cortisol, melatonina, sueño, presión y sensibilidad a la insulina.",
            "El ejercicio actúa como señal temporal periférica y su horario puede modificar rendimiento y respuesta metabólica.",
            "La evidencia comparativa es heterogénea y no identifica una hora universalmente superior.",
            "Cronotipo, comidas, luz, turnos, medicación y hábito de entrenamiento desplazan fase y amplitud.",
            "Caminatas posprandiales y sesiones posteriores a la cena pueden reducir excursiones glucémicas en contextos concretos.",
            "La regularidad y la preservación de 7-9 horas de sueño suelen superar una ventaja horaria pequeña.",
            "Un diseño N-of-1 permite comparar ventanas equivalentes sin convertir mecanismos plausibles en dogmas.",
        ],
        "intro": ["<strong>Prescribir horario modifica el contexto biológico de la misma dosis.</strong> Reloj central y relojes de músculo, hígado, páncreas y tejido adiposo reciben señales diferentes.", "La temperatura puede variar y el rendimiento fluctuar 5-10%, pero sacrificar sueño o adherencia para perseguir un máximo teórico empeora el balance clínico."],
        "sections": [
            ("Relojes centrales y periféricos", "Revisiones fisiológicas describen fases separadas 2-4 horas entre cronotipos y oscilaciones de rendimiento cercanas a 5-10%, con IC95% dependiente de tarea.", "Luz sincroniza núcleo supraquiasmático; contracción, AMPK, glucógeno y comidas ajustan relojes periféricos.", "Registrar 7-14 días de sueño, luz, comidas y trabajo capta realidades que un laboratorio regional no reproduce."),
            ("Glucosa posprandial", "Un ensayo indexado en PubMed mostró que ejercicio de fuerza después de cenar mejoró factores posprandiales más que antes de cenar; ello no demuestra una hora óptima para todos.", "Contracción moviliza GLUT4 independientemente de insulina y 10-15 minutos posprandiales reducen disponibilidad circulante de glucosa.", "Caminatas tras 2-3 comidas son baratas; se ajustan por sulfonilureas o insulina y acceso a monitorización."),
            ("Presión y variación diaria", "Metaanálisis de <em>Sports Medicine</em> sitúan la reducción por entrenamiento alrededor de 5-8 mmHg, mientras diferencias por horario conservan IC95% más amplios.", "Tono simpático, temperatura y descenso nocturno de 10-20% interactúan; no ser dipper no prescribe automáticamente ejercicio nocturno.", "Presión domiciliaria en dos ventanas de 2-4 semanas permite una comparación pragmática."),
            ("Cronotipo, rendimiento y adaptación", "Personas tardías suelen rendir mejor por la tarde y tempranas antes; entrenar a una hora fija reduce parte de la diferencia en estudios de semanas.", "Temperatura, rigidez, activación neural y disponibilidad de sustrato cambian RPE para igual carga.", "La ventana elegida debe respetar turnos y seguridad; una adherencia ≥75% pesa más que 5% de ventaja aguda."),
            ("Sueño y ejercicio nocturno", "La literatura no respalda prohibir toda actividad vespertina; vigor muy próximo al sueño puede aumentar latencia en personas sensibles, con gran heterogeneidad.", "Melatonina, enfriamiento corporal y descenso simpático facilitan inicio; terminar vigoroso ≥2-3 horas antes es una prueba conservadora.", "Luz matinal 20-30 minutos, despertar regular y reducción de cafeína ≥8 horas antes son medidas accesibles."),
            ("Ensayos N-of-1", "Comparar 14 días matinales con 14 vespertinos manteniendo volumen permite observar diferencias repetidas de 10-15 mg/dl o 5 mmHg sin atribuir causalidad instantánea.", "Controlar comida, sueño y medicación reduce ruido; se analizan medias semanales y dispersión, no el mejor día.", "Una hoja o teléfono basta; si aparece hipoglucemia, mareo o insomnio se detiene y coordina atención."),
        ],
        "clinical": ["El horario merece prescripción sólo cuando responde una pregunta concreta de glucosa, presión, sueño o adherencia.", "La incertidumbre se maneja con pruebas reversibles, medidas repetidas y conservación del resto de la dosis."],
        "guidelines": ["Registrar 7-14 días antes de cambiar horario.", "Priorizar regularidad y 7-9 horas de sueño.", "Probar caminatas de 10-15 minutos posprandiales.", "Comparar ventanas en bloques de 2-4 semanas.", "Alejar vigor del sueño si empeora latencia.", "Ajustar por insulina, hipotensores y turnos."],
        "keypoints": ["No existe hora universal.", "Ejercicio sincroniza relojes periféricos.", "Comidas y fármacos cambian respuesta.", "Posprandial es una ventana pragmática.", "N-of-1 reduce dogmatismo.", "Adherencia domina ventajas pequeñas."],
        "refs": ["postdinner", "hiit_bp", "hiit_capacity", "hiit_older", "fermentation", "hypertrophy", "hf_review"],
    },
    "ejercicio-y-microbiota-intestinal-en-obesidad-puentes-entre-intestino-musculo-y-metabolismo": {
        "topic": "obesidad y microbiota intestinal",
        "abstract": [
            "El ejercicio modifica funciones microbianas vinculadas con fermentación, barrera intestinal e inflamación.",
            "Los ensayos en sobrepeso y obesidad muestran cambios modestos y heterogéneos, sin una microbiota atlética única.",
            "Dieta, fármacos, adiposidad y método de secuenciación explican parte de la variación.",
            "Un ensayo de prevención de diabetes relacionó capacidad fermentativa basal con respuesta metabólica al ejercicio.",
            "La asociación no autoriza a excluir a nadie del ejercicio ni a seleccionar HIIT mediante un test comercial.",
            "Ejercicio multicomponente, fibra progresiva, sueño e hidratación conservan prioridad terapéutica.",
            "Los desenlaces útiles siguen siendo función, cintura, glucemia, lípidos y calidad de vida.",
        ],
        "intro": ["<strong>El eje intestino-músculo es bidireccional y no reducible a una bacteria.</strong> Contracción, mioquinas, tránsito y perfusión interactúan con metabolitos microbianos.", "Diversidad alfa, abundancia taxonómica y capacidad funcional son niveles distintos; ninguno sustituye una respuesta clínica medible."],
        "sections": [
            ("Qué cambia con ejercicio", "La revisión 2025 de <em>Physical Activity and Nutrition</em> encontró SMD pequeñas y heterogeneidad alta en diversidad y taxones durante 6-24 semanas.", "Los cambios funcionales en butirato y fermentación pueden ocurrir sin gran desplazamiento taxonómico; músculo y epitelio intercambian señales inflamatorias.", "Registrar fibra y ultraprocesados evita atribuir al ejercicio cambios dietarios simultáneos."),
            ("Fermentación y respondedores", "El ensayo de <em>Cell Metabolism</em> vinculó fermentación basal con eficacia para prevenir diabetes, una interacción predictiva y no una contraindicación.", "Ácidos grasos de cadena corta modulan barrera, GLP-1 y sensibilidad; la causalidad humana permanece incompleta.", "Tras 8-12 semanas se revisa dosis, sueño y dieta antes de pagar secuenciación sin umbral terapéutico."),
            ("Adiposidad y control glucémico", "Reducciones de 5-10% de peso, 2-5 cm de cintura o cambios de HbA1c pueden aparecer sin firma microbiana estable ni SMD grande.", "Mayor captación muscular de glucosa y oxidación de lípidos reduce flujo de sustrato, mientras pérdida visceral atenúa inflamación.", "Cintura, sit-to-stand y glucosa son medidas accesibles para atención primaria regional."),
            ("Dosis e intensidad", "Guías y ensayos sostienen 150-300 minutos moderados y fuerza 2-3 días; HIIT puede añadir cerca de 2 ml·kg⁻¹·min⁻¹ de VO₂max sin evidencia de selección por taxón.", "Alternar intensidades modifica lactato, catecolaminas y tránsito; extremos prolongados con calor pueden aumentar permeabilidad transitoria.", "Progresar volumen 5-10%, hidratar y separar comida copiosa 2-3 horas mejora tolerancia."),
            ("Fibra y síntomas gastrointestinales", "Metas de 25-30 g/día son razonables, pero aumentos bruscos elevan distensión; los ensayos tienen IC95% amplios para taxones específicos.", "Legumbres, avena, frutas y granos aportan sustrato fermentable; diversidad alimentaria sostiene redundancia funcional.", "Se priorizan alimentos locales asequibles, agua segura y ajuste individual ante síndrome de intestino irritable."),
            ("Límites de personalización", "No hay HR, MD ni SMD validada que convierta un panel comercial en selector de modalidad; probióticos tampoco reemplazan dosis.", "La alta dimensionalidad y variación intraindividual favorecen falsos descubrimientos si no hay replicación.", "Los recursos se destinan primero a acceso al ejercicio, alimentación y seguimiento, explicando incertidumbre sin descalificar mecanismos."),
        ],
        "clinical": ["La microbiota explica parte de la heterogeneidad, pero todavía no entrega una receta clínica.", "Una intervención debe beneficiar aunque no se mida ningún taxón y debe juzgarse por función y metabolismo."],
        "guidelines": ["Prescribir 150-300 minutos y fuerza 2-3 días.", "Registrar dieta, fármacos y síntomas.", "Aumentar fibra gradualmente hacia 25-30 g/día.", "Progresar carga e hidratación según clima.", "No seleccionar HIIT por tests comerciales.", "Reevaluar cintura, glucosa y función a 8-12 semanas."],
        "keypoints": ["Función microbiana puede importar más que taxón.", "La respuesta es heterogénea.", "Dieta es un confusor central.", "Tests comerciales no prescriben ejercicio.", "Fibra y carga progresan juntas.", "Desenlaces clínicos tienen prioridad."],
        "refs": ["microbiota", "fermentation", "postdinner", "hiit_bp", "hiit_capacity", "grip", "hypertrophy"],
    },
    "prescripcion-de-ejercicio-en-epoc-capacidad-funcional-dispnea-y-fuerza-periferica": {
        "topic": "EPOC estable",
        "abstract": [
            "La rehabilitación pulmonar mejora capacidad, disnea y calidad de vida aunque el VEF₁ cambie poco.",
            "Su efecto recae en desacondicionamiento, músculo periférico, eficiencia ventilatoria y autoeficacia.",
            "Metaanálisis informan ganancias aproximadas de 31-53 m en caminata de 6 minutos.",
            "El entrenamiento continuo, los intervalos, la fuerza y músculos inspiratorios responden a fenotipos diferentes.",
            "Borg, SpO₂, caminata y fuerza permiten titular dosis cuando no existe ergoespirometría.",
            "Exacerbación, desaturación y comorbilidad cardiovascular gobiernan seguridad.",
            "La continuidad después de 6-12 semanas determina si la ganancia se conserva.",
        ],
        "intro": ["<strong>Disnea, evitación y desacondicionamiento forman un ciclo tratable.</strong> Cada tarea exige mayor fracción de la reserva y más ventilación.", "La rehabilitación no normaliza el pulmón; consigue que cada litro ventilado produzca más trabajo útil y menos amenaza percibida."],
        "sections": [
            ("Capacidad y significado clínico", "Metaanálisis en <em>Zdravstveno Varstvo</em> y <em>Therapeutic Advances in Respiratory Disease</em> reportan MD aproximadas de 31-53 m en 6MWD, por encima del umbral cercano a 30 m.", "Mejor extracción periférica y menor lactato reducen ventilación para igual tarea; aprendizaje también aporta metros.", "Se usa el mismo corredor, oxígeno e instrucciones; si no hay 30 m, el protocolo local sirve para seguimiento interno."),
            ("Continuo e intervalos", "Programas de 3-5 días, 20-40 minutos y Borg 3-5/10 mejoran capacidad; intervalos de 30-120 segundos permiten volumen similar con menos disnea sostenida.", "Pausas reducen hiperinflación dinámica y permiten vaciamiento, mientras el trabajo conserva estímulo oxidativo.", "Caminar, pedalear o hacer step con reloj es viable; se prioriza duración antes de velocidad."),
            ("Saturación y oxígeno", "SpO₂ persistente <88% durante esfuerzo requiere pausa y evaluación según prescripción; un valor aislado puede tener error de movimiento de varios puntos.", "Desaturación refleja desequilibrio ventilación-perfusión y difusión, pero síntomas y perfusión periférica afectan el oxímetro.", "Equipos confiables, manos calientes y educación sobre oxígeno evitan falsa seguridad o alarmas."),
            ("Fuerza periférica", "Dos o tres días a 50-80% de 1RM, 1-3 series de 8-12, mejoran fuerza con menor ventilación minuto que continuo; 2-3 repeticiones más de sit-to-stand son útiles.", "Hipertrofia y reclutamiento reducen el porcentaje de fuerza máxima requerido para caminar y levantarse.", "Bandas y lastres se calibran y registran; prioridad a cuádriceps, cadera, pantorrilla, empuje y tracción."),
            ("Exacerbación y comorbilidad", "Aumento de disnea, volumen o purulencia de esputo y fiebre identifican cambio clínico; ensayos estables no permiten inferir seguridad durante exacerbación.", "Inflamación, atrapamiento aéreo y mayor demanda elevan carga; dolor torácico o síncope no se atribuyen automáticamente a EPOC.", "Se activa el plan médico y se reinicia al 50-70% del volumen previo tras estabilización."),
            ("Mantenimiento y telerehabilitación", "El beneficio de 6-12 semanas disminuye sin continuidad; estudios remotos muestran factibilidad, pero IC95% dependen de selección y soporte.", "Mantener 150 minutos adaptados y fuerza 2 días conserva señal muscular y confianza de exposición.", "Grupos comunitarios y llamadas mensuales amplían cobertura con criterios de inclusión y urgencia."),
        ],
        "clinical": ["La disnea es una variable para titular y no una orden de reposo.", "Intervalos y fuerza permiten acumular trabajo cuando la reserva ventilatoria es baja."],
        "guidelines": ["Medir caminata, Borg, SpO₂ y fuerza.", "Acumular 20-40 minutos 3-5 días.", "Intervalar si disnea impide continuidad.", "Entrenar fuerza 2-3 días a 50-80% estimado.", "Activar plan ante exacerbación.", "Planificar mantenimiento desde el alta."],
        "keypoints": ["Función mejora sin cambiar VEF₁.", "31-53 m es una ganancia esperable.", "Intervalos reducen carga sostenida.", "Cuádriceps requiere tratamiento específico.", "SpO₂ se interpreta con clínica.", "Mantenimiento preserva respuesta."],
        "refs": ["copd", "copd_severe", "hf_trial", "hf_review", "hiit_capacity", "grip", "hypertrophy"],
    },
    "ejercicio-y-neuroplasticidad-en-enfermedad-de-parkinson-de-la-evidencia-a-la-sesion-clinica": {
        "topic": "enfermedad de Parkinson",
        "abstract": [
            "El ejercicio es una intervención sintomática y funcional que mejora marcha, balance, fuerza y capacidad.",
            "Un metaanálisis reunió 191 ensayos de fisioterapia y respaldó múltiples modalidades con heterogeneidad.",
            "Neuroplasticidad requiere repetición, intensidad, saliencia, error y progresión.",
            "La inferencia mecanística no demuestra todavía neuroprotección ni modificación definitiva de enfermedad.",
            "Aeróbico, fuerza, amplitud, señales externas y doble tarea deben vincularse con limitaciones observables.",
            "Estado ON/OFF, hipotensión, freezing y caídas modifican seguridad y horario.",
            "La sesión eficaz practica tareas relevantes con calidad suficiente para transferirlas a participación.",
        ],
        "intro": ["<strong>La pérdida dopaminérgica altera automatización, pero las redes conservan capacidad de aprendizaje.</strong>", "Ninguna modalidad gana todos los desenlaces; danza, cinta, ciclismo, fuerza y balance aportan estímulos diferentes."],
        "sections": [
            ("Síntesis de 191 ensayos", "El metaanálisis de <em>Neurorehabilitation and Neural Repair</em> integró 191 ensayos y halló SMD favorables en dominios motores, con IC95% variables y seguimiento breve.", "La convergencia apoya tratar, pero heterogeneidad por estadio, medicación y tarea impide declarar una modalidad única.", "Acceso, cultura y transporte guían elección; adherencia ≥75% vuelve útil una opción disponible."),
            ("Aeróbico y neuroplasticidad", "Protocolos de 20-40 minutos, 3-5 días y RPE 13-16/20 mejoran fitness; cambios en factores neurotróficos no equivalen a HR menor de progresión.", "Flujo cerebral, BDNF, angiogénesis y eficiencia sináptica son mecanismos plausibles amplificados por intensidad tolerada.", "Intervalos de 1-3 minutos permiten dosis con fatiga; bicicleta estable reduce riesgo en freezing."),
            ("Fuerza, potencia y amplitud", "Dos o tres sesiones, 2-3 series de 6-12, producen MD funcionales aunque SMD varíe entre pruebas.", "Mayor reclutamiento y tasa de fuerza sostienen pasos amplios y reacciones posturales; amplitud requiere práctica específica.", "Silla, bandas y escalón permiten progresar 5-10% con asistencia del cuidador entrenado."),
            ("Señales externas y freezing", "Claves auditivas o visuales mejoran parámetros de marcha en ensayos cortos; su IC95% no garantiza transferencia sin práctica contextual.", "Las claves trasladan control hacia rutas atencionales; ajustar cadencia 5-10% busca longitud sin velocidad insegura.", "Marcas en puertas y estrategias detener-respirar-transferir peso son aplicables en hogares pequeños."),
            ("Doble tarea y cognición", "Una caída >10% en velocidad o precisión durante doble tarea indica costo relevante; revisiones en <em>PMC</em> apoyan dosificación gradual.", "Competencia por atención y función ejecutiva exige estabilizar tarea simple antes de sumar conteo o carga.", "Circuitos de 30-90 segundos reproducen mercado, transporte y cocina con protección contra caídas."),
            ("Estado ON, presión y sesión", "Programar 45-90 minutos tras levodopa puede aprovechar ON, pero farmacocinética varía; caída ortostática ≥20/10 mmHg requiere atención.", "Disautonomía altera cronotropismo y perfusión; calentamiento y transiciones lentas reducen síntomas.", "Se registran hora de dosis, freezing, caídas y presión, y se enseña al cuidador cuándo asistir o detener."),
        ],
        "clinical": ["Neuroplasticidad se vuelve clínica cuando la tarea es intensa, significativa y repetible.", "Complejidad sin seguridad no es progreso, y ejercicio genérico sin sobrecarga tampoco."],
        "guidelines": ["Registrar ON/OFF, marcha, giros y freezing.", "Combinar aeróbico 3-5 días y fuerza 2-3.", "Usar claves externas con objetivo medible.", "Agregar doble tarea tras estabilidad simple.", "Controlar presión ortostática y caídas.", "Entrenar al cuidador en estrategias seguras."],
        "keypoints": ["191 ensayos respaldan fisioterapia.", "No se prueba neuroprotección definitiva.", "Saliencia y repetición sostienen aprendizaje.", "Claves compensan automatización.", "Doble tarea se titula.", "ON/OFF cambia la sesión."],
        "refs": ["parkinson_meta", "parkinson_plasticity", "parkinson_cognition", "grip", "grip_thresholds", "hiit_capacity", "hypertrophy"],
    },
    "sueno-recuperacion-e-inmunidad-en-deportistas-y-pacientes-clinicos-una-mirada-integrada": {
        "topic": "sueño, recuperación e inmunidad",
        "abstract": [
            "El sueño sostiene recuperación neuromuscular, control autonómico, metabolismo y coordinación inmune.",
            "Dormir poco repetidamente aumenta RPE, apetito y errores, aunque una noche no determina por sí sola lesión.",
            "Carga, regularidad, síntomas y estrés deben interpretarse juntos.",
            "Los wearables estiman tendencias y no diagnostican arquitectura de sueño ni preparación.",
            "Deportistas y pacientes comparten mecanismos, pero difieren en reserva y costo del error.",
            "Una estrategia clínica protege 7-9 horas y ajusta carga cuando varias señales convergen.",
            "Apnea, insomnio persistente, fiebre o síntomas sistémicos requieren evaluación específica.",
        ],
        "intro": ["<strong>Recuperar es restaurar capacidad para responder, no simplemente estar inactivo.</strong> Sueño organiza memoria motora, secreción hormonal y tráfico inmune.", "Ningún puntaje resume esos procesos; historia, tarea submáxima, síntomas y carga reciente forman una triangulación más robusta."],
        "sections": [
            ("Duración y regularidad", "Dormir <7 horas crónicamente se asocia con peor salud; HR observacionales no separan por completo estrés, turnos y enfermedad.", "Sueño lento favorece recuperación y consolidación; irregularidad desplaza fase y altera glucosa y tono simpático.", "Turnos, transporte y hacinamiento son determinantes; se registra 7-14 días antes de culpar disciplina."),
            ("Carga y rendimiento", "Una reducción de 60-90 minutos por 3 noches, fatiga >2 puntos o caída >5% en tarea submáxima justifica ajustar, aunque no es umbral validado universal.", "Menor glucógeno, control ejecutivo y coordinación elevan RPE; reducir 20-40% por 24-72 horas protege calidad.", "Session-RPE × minutos permite cuantificar sin plataforma propietaria."),
            ("Inmunidad y síntomas", "Ejercicio moderado se asocia con menor carga infecciosa; esfuerzos prolongados con baja energía cambian leucocitos transitoriamente sin probar una ventana universal.", "Catecolaminas redistribuyen células y sueño modula citocinas; cambio agudo no equivale a inmunodeficiencia.", "Fiebre, dolor torácico o disnea desproporcionada suspenden; inmunosuprimidos requieren umbral conservador."),
            ("Wearables y VFC", "VFC puede variar 10-20% por hidratación, alcohol, ciclo o infección; precisión de etapas de sueño conserva IC95% insuficiente para diagnóstico.", "Balance simpático-vagal es contexto, no orden automática; tendencia de 7 días pesa más que lectura aislada.", "Una señal de bienestar, carga y función ofrece un sistema de bajo costo en clubes y clínicas."),
            ("Higiene circadiana", "La recomendación de 7-9 horas admite variación; luz matinal 20-30 minutos y cafeína alejada ≥8 horas son intervenciones con bajo riesgo.", "Melatonina y descenso térmico requieren fase estable; vigor puede terminar ≥2-3 horas antes si aumenta latencia.", "Horarios familiares y laborales se negocian, evitando planes imposibles."),
            ("Derivación y retorno", "Insomnio ≥3 noches/semana por ≥3 meses y ronquido con pausas justifican evaluación; no hay SMD de ejercicio que sustituya tratamiento.", "Apnea produce hipoxia intermitente y carga simpática; retorno tras infección se escalona según síntomas y función.", "Rutas entre deporte, atención primaria y sueño reducen automedicación y retorno precoz."),
        ],
        "clinical": ["La recuperación se prescribe protegiendo sueño y modulando carga, no persiguiendo un puntaje perfecto.", "Dos de tres señales alteradas de forma sostenida ofrecen una regla prudente para reevaluar."],
        "guidelines": ["Proteger 7-9 horas y despertar regular.", "Registrar sueño y carga 7-14 días.", "Reducir 20-40% si convergen varias señales.", "Usar wearables sólo como tendencia.", "Suspender ante fiebre o síntomas sistémicos.", "Derivar apnea probable o insomnio crónico."],
        "keypoints": ["Patrones importan más que una noche.", "Sueño integra metabolismo e inmunidad.", "VFC aislada no prescribe.", "Carga se ajusta con señales convergentes.", "Contexto social afecta recuperación.", "Apnea e insomnio requieren ruta clínica."],
        "refs": ["postdinner", "hiit_capacity", "hiit_older", "hf_review", "parkinson_cognition", "grip", "hypertrophy"],
    },
    "fuerza-muscular-como-predictor-de-mortalidad-cardiometabolica-de-la-dinamometria-a-la-prescripcion": {
        "topic": "fuerza muscular y riesgo cardiometabólico",
        "abstract": [
            "La fuerza de prensión integra reserva neuromuscular, enfermedad y trayectoria de actividad.",
            "Un metaanálisis prospectivo encontró HR 1,41 de mortalidad total al comparar menor con mayor fuerza.",
            "La asociación también alcanza desenlaces cardiovasculares y cáncer, pero no prueba causalidad directa.",
            "Edad, sexo, tamaño corporal, dolor, equipo y técnica modifican interpretación.",
            "Una cifra baja debe activar evaluación de sarcopenia, nutrición y enfermedad, no producir una sentencia.",
            "La dinamometría gana utilidad cuando conduce a fuerza global progresiva y seguimiento reproducible.",
            "Medir, prescribir y repetir transforma un biomarcador poblacional en herramienta clínica.",
        ],
        "intro": ["<strong>Prensión es una ventana económica a reserva, no un diagnóstico etiológico.</strong> Captura una dimensión que IMC, presión y laboratorio omiten.", "Causalidad inversa y confusión residual impiden afirmar que cada kilogramo ganado reduzca un porcentaje fijo de mortalidad."],
        "sections": [
            ("Asociación pronóstica", "El metaanálisis de <em>JAMDA</em> informó HR 1,41 para mortalidad total entre extremos; HR no significa 41% de riesgo absoluto.", "Fuerza resume masa, control neural y exposición a enfermedad; reserva mayor puede amortiguar estrés fisiológico.", "Se explican riesgo basal y seguimiento para evitar alarmar con un cociente relativo."),
            ("Dosis-respuesta y umbrales", "La revisión de <em>Ageing Research Reviews</em> estudió umbrales y relación no lineal con mortalidad cardiovascular y cáncer, con IC95% variables.", "Edad, sexo y talla desplazan distribución; dicotomizar pierde información y amplifica error cerca del corte.", "Percentiles locales y trayectoria individual son preferibles cuando no hay referencia regional robusta."),
            ("Protocolo de dinamometría", "Dos o tres intentos de 3-5 segundos, codo a 90° y 30-60 segundos de pausa reducen error; cambiar máximo por promedio invalida MD longitudinal.", "Ajuste del mango modifica longitud muscular y palanca; dolor y fatiga pueden mover 2-3 kg sin adaptación.", "Una instrucción común y calibración anual hacen viable tamizaje en atención primaria."),
            ("Qué evaluar ante debilidad", "Caída >10% merece contexto aun sobre el corte; fuerza baja puede coexistir con pérdida de peso, neuropatía o enfermedad cardiopulmonar.", "Inflamación, baja proteína, denervación y desuso convergen en catabolismo y menor reclutamiento.", "Se conecta con marcha, sit-to-stand, ingesta y medicina, evitando entregar un número sin ruta."),
            ("Prescripción de fuerza global", "Dos o tres días, 1-3 series de 6-12 a 60-80% de 1RM mejoran fuerza; fragilidad inicia en 40-60% con progresión 5-10%.", "Sobrecarga de grandes grupos induce síntesis y adaptación neural; apretar un dinamómetro no sustituye patrones funcionales.", "Bandas, mochilas y mancuernas funcionan si carga, RIR y adherencia ≥75% quedan registradas."),
            ("Reevaluación y transferencia", "Cambios repetidos de 5-10% junto con sit-to-stand son más convincentes que una medición; mínima diferencia detectable depende del equipo.", "Transferencia aparece cuando mayor reserva reduce costo relativo de tareas y acelera recuperación.", "Repetir cada 8-12 semanas con el mismo evaluador y protocolo permite decisiones auditables."),
        ],
        "clinical": ["La responsabilidad de la dinamometría comienza después de obtener el número.", "Un HR pronóstico debe conducir a evaluación multidimensional y no a causalidad simplificada."],
        "guidelines": ["Estandarizar postura, mango e intentos.", "Interpretar con edad, sexo, talla y dolor.", "Revisar trayectoria además de umbral.", "Evaluar nutrición, marcha y sit-to-stand.", "Prescribir fuerza global 2-3 días.", "Repetir con igual protocolo a 8-12 semanas."],
        "keypoints": ["HR 1,41 no es riesgo absoluto.", "Prensión es marcador, no causa.", "Técnica determina comparabilidad.", "Caída longitudinal merece estudio.", "Tratamiento abarca grandes grupos.", "Reevaluación confirma transferencia."],
        "refs": ["grip", "grip_thresholds", "cancer_fitness", "cancer_trials", "bone_dynamic", "hypertrophy", "hf_trial"],
    },
    "ejercicio-en-oncologia-seguridad-dosis-y-recuperacion-funcional-durante-y-despues-del-tratamiento": {
        "topic": "ejercicio oncológico",
        "abstract": [
            "El ejercicio durante y después del tratamiento es generalmente seguro cuando se adapta a toxicidad y reserva.",
            "Mejora fatiga, aptitud, fuerza, función y calidad de vida.",
            "Mayor fitness o fuerza se asocia con 31-46% menor mortalidad en análisis observacionales.",
            "Un metaanálisis de ensayos aleatorizados informó cerca de 26% menos mortalidad total, HR aproximado 0,74.",
            "Asociación y efecto experimental convergen, pero no autorizan promesas individuales.",
            "Metástasis, hemograma, neuropatía, cardiotoxicidad, cirugía y síntomas determinan la sesión.",
            "La meta es preservar función durante ciclos y reconstruir participación después del tratamiento.",
        ],
        "intro": ["<strong>Esperar al final del tratamiento puede consolidar discapacidad evitable.</strong> Fatiga, sarcopenia y desacondicionamiento comienzan desde diagnóstico.", "El cáncer no define por sí solo riesgo; sitio, estabilidad ósea, infección, dispositivos y toxicidad actual sí cambian la carga."],
        "sections": [
            ("Evidencia funcional y pronóstica", "<em>British Journal of Sports Medicine</em> informó 31-46% menor mortalidad con mayor fuerza o fitness; <em>Cancer Treatment Reviews</em> estimó HR ≈0,74, 26% menos, en ensayos.", "Fitness y fuerza reflejan reserva, inflamación y tolerancia; causalidad inversa persiste en cohortes pero disminuye en aleatorización.", "Registrar dosis y eventos en redes públicas permite evaluar efectividad fuera de centros privados."),
            ("Dosis durante ciclos", "La meta avanza hacia 90-150 minutos y fuerza 2-3 días; bloques de 5-10 minutos y RPE 3-6/10 sostienen frecuencia en nadir.", "Mantener señal con 20-50% menos volumen evita desacondicionamiento sin competir con recuperación hematológica.", "Sesiones híbridas de 15-30 minutos reducen transporte y permiten adaptación diaria."),
            ("Fuerza y sarcopenia", "Una pérdida >10% de carga o función entre ciclos requiere evaluación; 1-3 series de 6-15 repeticiones son escalables.", "Tensión mecánica contrarresta catabolismo y resistencia anabólica; proteína y energía condicionan respuesta.", "Silla, bisagra, empuje, tracción y pantorrilla cubren autonomía con material simple."),
            ("Metástasis óseas y cirugía", "Ensayos generales excluyen lesiones inestables, por lo que su baja tasa de eventos tiene IC95% no aplicable a todos los sitios.", "Se evita carga y torsión directa sobre segmento de alto riesgo, pero regiones seguras conservan estímulo sistémico.", "Informe de imagen y restricciones deben acompañar la derivación; no se improvisa por ausencia de comunicación."),
            ("Toxicidad y banderas rojas", "Fiebre ≥38 °C, sangrado, síncope, dolor torácico, disnea de reposo o déficit neurológico suspenden; no existe un umbral hematológico universal aislado.", "Anemia reduce transporte de O₂, trombocitopenia eleva sangrado, neuropatía altera equilibrio y cardiotoxicidad modifica hemodinámica.", "Se sigue protocolo oncológico local y se garantiza contacto, especialmente entre ciclos."),
            ("Fatiga, supervivencia y retorno", "Aumento ≥2 puntos de fatiga que persiste 24-48 horas sugiere exceso; programas de 8-12 semanas mejoran función con SMD moderadas variables.", "Actividad moderada puede reducir fatiga aguda y restaurar autoeficacia; progresión posterior busca 150-300 minutos.", "Metas laborales, familiares y recreativas orientan transferencia, con reevaluación cada 4-8 semanas."),
        ],
        "clinical": ["Seguridad oncológica significa adaptar con información actualizada, no mantener cargas siempre bajas.", "La continuidad a través de ciclos protege reserva y facilita recuperación posterior."],
        "guidelines": ["Revisar toxicidad, cirugía, metástasis y dispositivos.", "Comenzar con bloques de 5-10 minutos.", "Reducir volumen 20-50% en días difíciles.", "Entrenar fuerza 2-3 días según tolerancia.", "Medir respuesta a 24-48 horas.", "Suspender ante fiebre, sangrado o síntomas cardiopulmonares."],
        "keypoints": ["Ejercicio es viable durante tratamiento.", "31-46% es asociación pronóstica.", "HR ≈0,74 proviene de síntesis experimental.", "Metástasis requiere mapa anatómico.", "Fatiga guía autorregulación.", "Función y participación son metas continuas."],
        "refs": ["cancer_fitness", "cancer_trials", "grip", "grip_thresholds", "hf_review", "bone_dynamic", "hypertrophy"],
    },
}


PAPER_BODIES = {slug: _body(spec) for slug, spec in SPECS.items()}


PAPER_META = {
    slug: {
        "excerpt": excerpt,
        "keywords": SPECS[slug]["keywords"] if "keywords" in SPECS[slug] else keywords,
    }
    for slug, excerpt, keywords in [
        (
            "mitocondrias-ejercicio-e-insuficiencia-cardiaca-rehabilitacion-metabolica-de-precision",
            "Revisión clínica de la miopatía periférica en insuficiencia cardiaca: biogénesis mitocondrial, VO₂peak, fuerza, intervalos, congestión y seguimiento funcional para una rehabilitación metabólica individualizada y viable en Latinoamérica.",
            ["insuficiencia cardiaca", "mitocondrias", "VO2peak", "rehabilitación cardiaca", "fuerza muscular"],
        ),
        (
            "entrenamiento-de-fuerza-y-salud-osea-en-mujeres-posmenopausicas-evidencia-clinica-aplicada",
            "Síntesis cuantitativa de fuerza y salud ósea posmenopáusica, con SMD por sitio, carga ≥70% de 1RM, mecanotransducción, prevención de caídas, seguridad vertebral y continuidad anual.",
            ["posmenopausia", "osteoporosis", "densidad mineral ósea", "entrenamiento de fuerza", "fracturas"],
        ),
        (
            "hiit-versus-entrenamiento-continuo-en-hipertension-arterial-que-dice-la-fisiologia-clinica",
            "Comparación crítica de HIIT y entrenamiento continuo en hipertensión: presión de reposo y ambulatoria, diferencia de VO₂max, mecanismos endoteliales, medicación y criterios clínicos de progresión.",
            ["HIIT", "hipertensión", "presión arterial", "VO2max", "entrenamiento continuo"],
        ),
        (
            "cronobiologia-del-ejercicio-ritmos-circadianos-y-control-metabolico",
            "El horario como variable prescriptiva: relojes periféricos, cronotipo, glucosa posprandial, presión, sueño y ensayos N-of-1 para individualizar sin afirmar una hora universal.",
            ["cronobiología", "ritmo circadiano", "horario de ejercicio", "glucosa", "cronotipo"],
        ),
        (
            "ejercicio-y-microbiota-intestinal-en-obesidad-puentes-entre-intestino-musculo-y-metabolismo",
            "Análisis del eje intestino-músculo en obesidad: fermentación, barrera, heterogeneidad microbiana, fibra, ejercicio multicomponente y límites actuales de los tests comerciales.",
            ["microbiota intestinal", "obesidad", "ejercicio", "ácidos grasos de cadena corta", "resistencia a la insulina"],
        ),
        (
            "prescripcion-de-ejercicio-en-epoc-capacidad-funcional-dispnea-y-fuerza-periferica",
            "Prescripción integral en EPOC con caminata de 6 minutos, Borg, SpO₂, intervalos, fuerza periférica, exacerbaciones y estrategias de mantenimiento adaptadas a recursos regionales.",
            ["EPOC", "rehabilitación pulmonar", "disnea", "caminata de 6 minutos", "fuerza periférica"],
        ),
        (
            "ejercicio-y-neuroplasticidad-en-enfermedad-de-parkinson-de-la-evidencia-a-la-sesion-clinica",
            "De 191 ensayos a una sesión individualizada en Parkinson: aeróbico, fuerza, amplitud, claves externas, doble tarea, estado ON/OFF, hipotensión y transferencia funcional.",
            ["Parkinson", "neuroplasticidad", "fisioterapia", "marcha", "ejercicio aeróbico"],
        ),
        (
            "sueno-recuperacion-e-inmunidad-en-deportistas-y-pacientes-clinicos-una-mirada-integrada",
            "Marco clínico para integrar sueño, carga, rendimiento e inmunidad, interpretar VFC y wearables con cautela, ajustar sesiones y detectar apnea, insomnio o infección.",
            ["sueño", "recuperación", "inmunidad", "carga de entrenamiento", "fatiga"],
        ),
        (
            "fuerza-muscular-como-predictor-de-mortalidad-cardiometabolica-de-la-dinamometria-a-la-prescripcion",
            "Interpretación rigurosa de la fuerza de prensión y HR 1,41: protocolo dinamométrico, causalidad, umbrales, evaluación multidimensional y traducción a fuerza global progresiva.",
            ["fuerza de prensión", "dinamometría", "mortalidad", "riesgo cardiometabólico", "sarcopenia"],
        ),
        (
            "ejercicio-en-oncologia-seguridad-dosis-y-recuperacion-funcional-durante-y-despues-del-tratamiento",
            "Ejercicio durante y después del cáncer: evidencia funcional y pronóstica, autorregulación por ciclos, metástasis óseas, toxicidades, fatiga y recuperación de participación.",
            ["ejercicio oncológico", "cáncer", "fatiga", "fuerza muscular", "supervivencia"],
        ),
    ]
}
