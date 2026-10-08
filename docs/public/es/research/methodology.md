---
title: Método y salvaguardas
eyebrow: Límite del diseño de investigación
description: Un esquema metodológico cauto para un posible estudio educativo futuro de TTOD.
permalink: /es/research/methodology/
lang: es
---

# El método antes de los datos

La hebra B prepara y somete un protocolo de estudio de caso educativo: preguntas explícitas, información a las personas participantes, revisión ética y de protección de datos, acceso y retención definidos, y una separación clara entre docencia, evaluación y participación voluntaria en la investigación. Las plantillas y el dossier para el comité viven en el repositorio bajo `docs/research/ethics/`. **El análisis de artefactos estudiantiles como datos de investigación no comienza** hasta que el órgano ético competente autorice el protocolo y conste el consentimiento válido. La hebra A (filosófica) permanece aparada y no tiene sujetos humanos.

La docencia puede continuar sin tratar el trabajo de curso como evidencia de investigación.

## Postura metodológica

El trabajo de ingeniería sigue una lógica de indagación de diseño: articular un problema pedagógico, construir una intervención trazable, exponer sus supuestos y conservar evidencia de la iteración. Eso sostiene decisiones de diseño disciplinadas, pero no convierte el desarrollo de producto en investigación educativa.

Un estudio futuro podría usar un diseño de caso acotado para examinar el artefacto en contexto. Si el foco es cómo el alumnado negocia el apoyo de la IA, un enfoque de teoría fundamentada constructivista con comparación constante puede ser apropiado; [Liu, Fan y Pan 2026](#ref-liu-fan-pan-2026) ofrecen un ejemplo reciente en educación de la programación, no un protocolo que copiar sin cambio. Quien investiga debe declarar posicionalidad, muestreo, codificación, tratamiento de casos negativos y el límite entre hallazgos inductivos y conceptos sensibilizadores previos.

La autorregulación bajo asistencia de IA es en sí un objeto empírico. [López-Pernas et al. 2025](#ref-lopez-pernas-et-al-2025) codificaron miles de interacciones de estudiantado de grado con ChatGPT en un curso de programación web para estudiar colaboración, dependencia y delegación en el tiempo — evidencia de que los registros de proceso y la codificación de interacción pueden ser instrumentos de investigación cuando están autorizados, no de que los registros de TTOD ya lo sean.

## Posible diseño empírico

Un caso educativo acotado podría combinar la auditoría técnica del artefacto con el análisis cualitativo de registros de decisión versionados y una explicación oral breve. Las preguntas, los criterios de inclusión, el libro de códigos y el plan de análisis deberían registrarse o versionarse antes del análisis. Cualquier comparación debería centrarse en el razonamiento y la trazabilidad observables, salvo que el diseño sostenga una inferencia más fuerte.

Los artefactos potenciales incluyen un repositorio estudiantil, notas de decisión, uso declarado de IA, comprobaciones automatizadas y una defensa de cambios seleccionados. La triangulación puede comparar lo que hace el producto, lo que dice el registro y lo que el alumnado puede explicar; el desacuerdo entre esas fuentes es evidencia que analizar, no ruido que borrar. Nada de ello debería recogerse para investigación sin la autorización y la comunicación exigidas.

Los diseños de evaluación en educación de la computación ya tratan productos web construidos por el alumnado como evidencia auténtica. [Garcia 2025](#ref-garcia-2025) estudia portfolios digitales auto-codificados en un curso de diseño y desarrollo web bajo un marco basado en proyectos, lo que motiva mantener juntas la autoría técnica y la reflexión — sin pretender los mismos resultados para TTOD. Estudios de proceso brownfield como [Shihab et al. 2025](#ref-shihab-et-al-2025) motivan preguntas sobre cómo el alumnado acepta, rechaza y depura sugerencias de IA dentro de un código base heredado — la situación que la columna docente crea de propósito.

## Salvaguardas

- El acceso al curso y la calificación no deben depender de la participación en la investigación.
- La participación pedagógica en el proyecto de cohorte y el consentimiento investigador para uso secundario son distintos (formularios A frente a B).
- El repositorio docente y cualquier conjunto de datos de investigación deben tener identidades y reglas de acceso distintas.
- La minimización de datos, la retención, la seudonimización, la retirada y el acceso de quien revisa deben resolverse de antemano — no se recogen categorías especiales de datos personales; el corpus investigador, si se autoriza, solo contiene trazas de proceso seudonimizadas.
- La referencia rica del profesorado debe aislarse del artefacto estudiantil por evidencia, no por afirmación.
- Los resultados deben distinguir viabilidad, observación docente, evidencia de evaluación y evidencia de investigación.
- Los hallazgos negativos, mixtos o no concluyentes siguen siendo resultados válidos.
- Las pretensiones filosóficas de la hebra A no deben importarse como garantías empíricas de la hebra B.

## Anclajes de evidencia

Las fuentes siguientes motivan, pero no validan, el diseño propuesto. Las formas autor–año del texto enlazan a la lista Chicago inferior.

### Espina metodológica (informe, n pequeño, ética de datos de proceso)

- [Runeson y Höst 2009](#ref-runeson-host-2009) sobre cómo conducir e informar estudios de caso en ingeniería del software (proceso y listas de comprobación).
- [Runeson, Höst, Rainer y Regnell 2012](#ref-runeson-et-al-2012) — el manual ampliado de Wiley (*Case Study Research in Software Engineering*).
- [Wohlin et al. 2012](#ref-wohlin-et-al-2012) sobre estrategias empíricas en ingeniería del software (encuesta, experimento, estudio de caso); aquí para mantener la hebra B claramente **no experimental**.
- [Heckman et al. 2022](#ref-heckman-et-al-2022) sobre empirismo y normas de informe en CER.
- [Brown y Guzdial 2024](#ref-brown-guzdial-2024) sobre datos ricos frente a grandes — legitimidad del n pequeño sin inferencia poblacional.
- [McGill et al. 2023](#ref-mcgill-et-al-2023) sobre CER sólida: transferibilidad, informe de consentimiento, hallazgos nulos.
- [Fischer et al. 2024](#ref-fischer-et-al-2024) sobre arquitecturas de consentimiento para datos de proceso de programación.

### Dominio y fenómeno

- [Shihab et al. 2025](#ref-shihab-et-al-2025) sobre efectos y procesos de Copilot en tareas de codificación brownfield.
- [Nikolić y Basta Nikolić 2026](#ref-nikolic-basta-nikolic-2026) sobre un marco de cuatro pilares de evaluación resiliente a la IA (conceptual; sin datos de validación).
- [Liu, Fan y Pan 2026](#ref-liu-fan-pan-2026) sobre andamiaje frente a descarga cognitiva en educación de la programación asistida por IA.
- [López-Pernas et al. 2025](#ref-lopez-pernas-et-al-2025) sobre dinámicas de autorregulación en la resolución de problemas de programación estudiante–IA.
- [Garcia 2025](#ref-garcia-2025) sobre portfolios auto-codificados como evaluación auténtica en diseño y desarrollo web.
- [Davalos y Zhang 2026](#ref-davalos-zhang-2026) sobre la visibilidad del aprendizaje cuando la IA entra en el bucle de evaluación.
- [Prather et al. 2024](#ref-prather-et-al-2024) sobre beneficios y daños de la IA generativa para principiantes (rendimiento frente a aprendizaje).
- [*Computer Science Curricula 2023*](#ref-cs2023) sobre IA generativa, ética y responsabilidad profesional a escala de currículo.

Estas fuentes sostienen el estudio del proceso y del diseño de la evaluación. No establecen eficacia para esta plataforma, este curso o esta cohorte.

## Análisis y controles de calidad

- Versionar las preguntas de investigación, las definiciones de artefacto, las consignas de entrevista o defensa y el plan de análisis antes de examinar resultados.
- Mantener la telemetría de ingeniería, el trabajo de curso evaluado y los registros de investigación consentidos como conjuntos de datos distintos, con reglas de acceso distintas.
- Usar al menos dos formas de evidencia para pretensiones sobre el razonamiento; no inferir comprensión solo a partir de la actividad del repositorio. [Davalos y Zhang 2026](#ref-davalos-zhang-2026) argumentan que conservar salidas finales mientras se pierde la visibilidad del proceso es un fallo de medición — no solo un problema de detección.
- Registrar casos que desmienten, cambios de codificación, memorandos de quien investiga e interpretaciones no resueltas.
- Informar el entorno de aprendizaje, la política de IA, el acceso a herramientas, la experiencia previa, el contexto lingüístico y la profundidad del código de partida para que quien lee pueda juzgar la transferibilidad.
- Tratar la accesibilidad, la carga de trabajo y la participación diferencial como preguntas de investigación y posibles daños, no meros detalles de implementación.

<figure class="diagram-teaser">
  <a class="diagram-teaser-link" href="{{ '/assets/diagrams/ttod-research-safeguards.html' | relative_url }}">
    <img src="{{ '/assets/diagrams/ttod-research-safeguards.png' | relative_url }}" alt="Diagrama de flujo de datos: evidencia candidata — registros, calificaciones y defensa — filtrada por consentimiento y revisión ética y de datos, autorizada hacia conjuntos de datos docentes y de investigación distintos, y triangulada en hallazgos validados o en hallazgos negativos/mixtos igualmente válidos." loading="lazy">
  </a>
  <figcaption><a href="{{ '/assets/diagrams/ttod-research-safeguards.html' | relative_url }}">Abrir el diagrama interactivo de salvaguardas ↗</a> — cómo se filtraría la evidencia, cómo se mantendría en conjuntos de datos de acceso distinto, y cómo se triangularía una vez autorizada. (Interfaz en inglés.)</figcaption>
</figure>

## Evidencia que aún falta

La preparación de la investigación debe profundizar su evidencia sobre el desvanecimiento del ejemplo trabajado, el trazado de sistemas, la carga cognitiva, el aprendizaje de estudio, la transferencia conceptual de front-end, la autorregulación estudiante–IA más allá de casos de un solo curso y el doble rol docente–investigador. Los clásicos primarios sobre carga cognitiva al aprender software y sobre aprendizaje cognitivo están incompletos o sin metadatos bibliográficos verificados para la cita pública; el lenguaje de pretensión los mantiene por ello como necesidades abiertas de evidencia, no como justificación citada. Los requisitos legales o institucionales vigentes deben verificarse contra fuentes autorizadas cuando se redacte un protocolo.

## Referencias

- <span id="ref-brown-guzdial-2024"></span>Brown, Neil C. C., and Mark Guzdial. 2024. “Confidence vs Insight: Big and Rich Data in Computing Education Research.” In *Proceedings of the 55th ACM Technical Symposium on Computer Science Education V. 1*, 158–64. [https://doi.org/10.1145/3626252.3630813](https://doi.org/10.1145/3626252.3630813).
- <span id="ref-cs2023"></span>*Computer Science Curricula 2023*. Association for Computing Machinery, IEEE Computer Society, and AAAI. [https://doi.org/10.1145/3664191](https://doi.org/10.1145/3664191).
- <span id="ref-davalos-zhang-2026"></span>Davalos, Eduardo, and Yike Zhang. 2026. “AI Misuse in Education Is a Measurement Problem: Toward a Learning Visibility Framework.” arXiv. [https://doi.org/10.48550/arxiv.2603.07834](https://doi.org/10.48550/arxiv.2603.07834).
- <span id="ref-fischer-et-al-2024"></span>Fischer, Björn, Berit Barthelmes, Sven Eric Panitz, Eva-Maria Iwer, and Ralf Dörner. 2024. “Seeking Consent for Programming Process Data Collection with Trustee-Based Encryption.” In *Proceedings of the 2024 ACM Conference on International Computing Education Research V.1*, 131–42. [https://doi.org/10.1145/3632620.3671125](https://doi.org/10.1145/3632620.3671125).
- <span id="ref-garcia-2025"></span>Garcia, Manuel B. 2025. “Self-Coded Digital Portfolios as an Authentic Project-Based Learning Assessment in Computing Education: Evidence from a Web Design and Development Course.” *Education Sciences* 15 (9): 1150. [https://doi.org/10.3390/educsci15091150](https://doi.org/10.3390/educsci15091150).
- <span id="ref-heckman-et-al-2022"></span>Heckman, Sarah, Jeffrey C. Carver, Mark Sherriff, and Ahmed Al-Zubidy. 2022. “A Systematic Literature Review of Empiricism and Norms of Reporting in Computing Education Research Literature.” *ACM Transactions on Computing Education* 22 (1): Article 3. [https://doi.org/10.1145/3470652](https://doi.org/10.1145/3470652).
- <span id="ref-liu-fan-pan-2026"></span>Liu, Dandan, Guangrui Fan, and Lihu Pan. 2026. “Tool, Tutor, or Crutch?: A Grounded Theory of Cognitive Scaffolding and Offloading in AI-Assisted Programming Education.” *International Journal of STEM Education* 13: 10. [https://doi.org/10.1186/s40594-025-00592-w](https://doi.org/10.1186/s40594-025-00592-w).
- <span id="ref-lopez-pernas-et-al-2025"></span>López-Pernas, Sonsoles, Kamila Misiejuk, Eduardo Oliveira, and Mohammed Saqr. 2025. “The Dynamics of the Self-Regulation Process in Student-AI Interactions: The Case of Problem-Solving in Programming Education.” In *Proceedings of the 25th Koli Calling International Conference on Computing Education Research*. [https://doi.org/10.1145/3769994.3770043](https://doi.org/10.1145/3769994.3770043).
- <span id="ref-mcgill-et-al-2023"></span>McGill, Monica M., Sarah Heckman, Christos Chytas, et al. 2023. “Conducting Sound, Equity-Enabling Computing Education Research.” In *Proceedings of the 2023 Working Group Reports on Innovation and Technology in Computer Science Education*, 30–56. [https://doi.org/10.1145/3623762.3633495](https://doi.org/10.1145/3623762.3633495).
- <span id="ref-nikolic-basta-nikolic-2026"></span>Nikolić, Dragan, and Marijana Basta Nikolić. 2026. “Designing AI-Resilient Assessment in Higher Education: A Four-Pillar Conceptual Framework.” *Frontiers in Artificial Intelligence* 9. [https://doi.org/10.3389/frai.2026.1841682](https://doi.org/10.3389/frai.2026.1841682).
- <span id="ref-prather-et-al-2024"></span>Prather, James, et al. 2024. “The Widening Gap: The Benefits and Harms of Generative AI for Novice Programmers.” In *Proceedings of the 2024 ACM Conference on International Computing Education Research V.1*. [https://doi.org/10.1145/3632620.3671116](https://doi.org/10.1145/3632620.3671116).
- <span id="ref-runeson-host-2009"></span>Runeson, Per, and Martin Höst. 2009. “Guidelines for Conducting and Reporting Case Study Research in Software Engineering.” *Empirical Software Engineering* 14 (2): 131–64. [https://doi.org/10.1007/s10664-008-9102-8](https://doi.org/10.1007/s10664-008-9102-8).
- <span id="ref-runeson-et-al-2012"></span>Runeson, Per, Martin Höst, Austen Rainer, and Björn Regnell. 2012. *Case Study Research in Software Engineering: Guidelines and Examples*. Hoboken, NJ: Wiley. [https://doi.org/10.1002/9781118181034](https://doi.org/10.1002/9781118181034).
- <span id="ref-shihab-et-al-2025"></span>Shihab, Md Istiak Hossain, Christopher Hundhausen, Ahsun Tariq, Summit Haque, Yunhan Qiao, and Brian Wise Mulanda. 2025. “The Effects of GitHub Copilot on Computing Students’ Programming Effectiveness, Efficiency, and Processes in Brownfield Coding Tasks.” In *Proceedings of the 2025 ACM Conference on International Computing Education Research V.1*. [https://doi.org/10.1145/3702652.3744219](https://doi.org/10.1145/3702652.3744219).
- <span id="ref-wohlin-et-al-2012"></span>Wohlin, Claes, Per Runeson, Martin Höst, Magnus C. Ohlsson, Björn Regnell, and Anders Wesslén. 2012. *Experimentation in Software Engineering*. Berlin: Springer. [https://doi.org/10.1007/978-3-642-29044-2](https://doi.org/10.1007/978-3-642-29044-2).
