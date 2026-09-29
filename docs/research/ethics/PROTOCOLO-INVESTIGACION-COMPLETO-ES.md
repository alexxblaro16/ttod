<!--
Protocolo de investigación completo — remisión Comité de Ética.
Strand B · TTOD / Front-End II · ES · 2026-09-26.
-->

# Protocolo de investigación completo

**Título:** Aprendizaje haciendo: participación como desarrollador/a en una aplicación real
asistida por IA agentica, en grupo, como actividad formativa  
(**Producto:** 道 The Tao of Development (TTOD) / Oráculo)

**Acrónimo / código interno:** TTOD-Strand-B-FEII-2026-27  

**Investigador principal:** Rubén Vega Balbás, PhD  
**Afiliación:** UDIT — Área de Tecnología · Grupo ECSIT  
(*Tecnología e Innovación desde y para la Educación, la Cultura y la Sociedad*)  
**Contacto:** `ruben.vega@udit.es`  
**Grupo:** https://www.udit.es/lineas-de-investigacion/grupo-de-investigacion-innovacion-y-tecnologia-desde-y-para-la-educacion-la-cultura-y-la-sociedad/  

**Tipo de estudio:** Estudio de caso educativo / investigación basada en diseño (cualitativo
dominante, datos ricos de proceso). **No** es ensayo clínico, **no** es experimento controlado,
**no** pretende tamaños de efecto ni inferencia poblacional.

**Versión del protocolo:** 2026-09-26  

---

## 1. Antecedentes y justificación

La asistencia cotidiana de IA generativa en el desarrollo de software obliga a distinguir
*código producido* de *aprendizaje demostrado*, en especial en cursos **post-introductorios**
de ingeniería front-end. Este estudio observa un grupo real que construye un producto
auténtico (plataforma Oráculo de *The Tao of Development*) con asistencia agentica, trabajo
colaborativo y defensa oral.

**Justificación metodológica:** caso acotado con evidencia de proceso (Runeson y Höst 2009;
Runeson et al. 2012), datos ricos frente a grandes (Brown y Guzdial 2024), normas de informe
CER (Heckman et al. 2022; McGill et al. 2023), consentimiento para datos de proceso de
programación (Fischer et al. 2024). Se usa Wohlin et al. (2012) para situar el diseño como
**estudio de caso**, no como experimento.

Una línea filosófica paralela (Strand A) está **aparada** y **no** usa datos de estudiantes.

**Producción y procedencia (vía operativa).** Mantener Oráculo **en producción** no es solo
continuidad docente: TTOD es un **caso a escala reducida** de **aplicación agentica con
gobernanza de procedencia** — la plataforma consulta un **corpus autorizado** propio (la
colección de aforismos Tao), no un corpus abierto indiferenciado. Eso abre investigación
**operativa** sobre la infraestructura y las prácticas *DevOps* que exige un sistema de
conocimiento agentico con **IA local en producción**, complementaria a la vía filosófica
(Strand A) y a este estudio pedagógico (Strand B). Sin despliegue estable, esa evidencia
queda en demos locales efímeras. El apoyo presupuestario de producción se tramita por
canal institucional distinto del CEI
([`../institutional/SOLICITUD-PRESUPUESTO-PRODUCCION-ES.md`](../institutional/SOLICITUD-PRESUPUESTO-PRODUCCION-ES.md)).

---

## 2. Objetivos

### 2.1 Objetivo general

Comprender si — y cómo — la participación como desarrollador/a en un producto real, asistido
por IA agentica y en grupo, constituye una actividad de *aprender haciendo* con resultados
pedagógicos observables.

### 2.2 Objetivos específicos

1. Identificar qué trazas de proceso hacen explicables y revisables las contribuciones asistidas
   por IA.
2. Describir cómo el alumnado negocia autoría, agencia y responsabilidad.
3. Proponer principios de diseño situados (no un marco causal validado) del andamiaje
   walking-skeleton + revisión / fusión humana.
4. Documentar divergencias entre producto entregado y aprendizaje demostrado (defensa ↔
   artefacto).

---

## 3. Preguntas de investigación

**Principal:** ¿Puede la participación como desarrollador/a en una aplicación real, con
asistencia agentica y en grupo, constituir una actividad de aprendizaje con resultados
pedagógicos observables (*aprender haciendo*)?

**Subsidiarias (RQ-B1–B4):** ver diseño canónico
[`../STRAND-B-PEDAGOGICAL-DESIGN.md`](../STRAND-B-PEDAGOGICAL-DESIGN.md) §1.

---

## 4. Diseño y método

| Elemento | Definición |
| -------- | ---------- |
| Diseño | Caso único acotado / DBR cualitativo dominante |
| Caso | Cohorte Front-End II 2026–27 · producto TTOD Oráculo |
| Unidad de análisis | Trayectorias de pareja/solo (PRs) anidadas en el sistema del grupo |
| Muestreo | Conveniencia / censo del grupo de la asignatura; n pequeño |
| Análisis | Codificación temática + trazado descriptivo de proceso; triangulación producto / registro / defensa; casos negativos retenidos |
| Inicio del análisis investigador | Tras autorización ética + consentimiento + cierre de notas relevantes |

---

## 5. Participantes

| Aspecto | Descripción |
| ------- | ----------- |
| Inclusión | Matriculados en Front-End II que participan en la entrega del grupo TTOD y otorgan consentimiento B (uso investigador) |
| Exclusión del corpus investigador | Quienes no consienten; menores/vulnerables sin salvaguarda adicional aprobada |
| n | **8** estudiantes-desarrolladores (*README* del proyecto, 2026-09; excluido el PI). Corpus: n_consent ≤ 8 |
| Reclutamiento | No externo; la actividad es la asignatura. El consentimiento investigador es opt-in |

---

## 6. Procedimiento

1. Actividad docente ordinaria (desarrollo, PRs, declaración de IA, defensa).
2. Información y consentimiento (pedagógico A + investigador B).
3. Tras dictamen favorable y consentimientos válidos: ensamblaje de corpus **seudonimizado**.
4. Análisis cualitativo / de diseño.
5. Difusión agregada o con extractos no identificativos (consentimiento F / C4 si procede).

Instrumentos opcionales (encuesta, entrevista, grabación) **no** forman parte de esta versión
del protocolo.

---

## 7. Instrumentos

Ver anexo obligatorio [`INSTRUMENTOS-RECOLECCION-DATOS-ES.md`](INSTRUMENTOS-RECOLECCION-DATOS-ES.md).

---

## 8. Aspectos éticos

- Voluntariedad; nota **no** condicionada al consentimiento investigador.
- Separación docente / investigador; ceguera temporal preferible hasta cerrar notas.
- Minimización; sin categorías especiales de datos.
- Retirada sin consecuencia académica.
- Strand A excluida.

Consentimiento: [`PARTICIPANT-INFORMATION-SHEET-ES.md`](PARTICIPANT-INFORMATION-SHEET-ES.md),
[`PARTICIPANT-CONSENT-FORM-ES.md`](PARTICIPANT-CONSENT-FORM-ES.md).

---

## 9. Manejo de datos

Ver [`PLAN-MANEJO-DATOS-ES.md`](PLAN-MANEJO-DATOS-ES.md) y
[`DATA-MINIMIZATION-STATEMENT.md`](DATA-MINIMIZATION-STATEMENT.md).

---

## 10. Cronograma (orientativo)

| Fase | Ventana |
| ---- | ------- |
| Docencia / recolección ordinaria de artefactos | Curso 2026–27 (calendario FE II) |
| Dictamen ético | Remisión 2026-09 / según del comité |
| Análisis del corpus seudonimizado | Tras notas relevantes |
| Redacción / congreso (JENUI → ITiCSE) | Tras análisis |

---

## 11. Resultados esperados y difusión

Principios de diseño situados; informe de experiencia; hallazgos nulos o mixtos incluidos.
Sin pretensiones de causalidad. Plan de publicación:
[`../STRAND-B-CONGRESS-PUBLICATION-PLAN.md`](../STRAND-B-CONGRESS-PUBLICATION-PLAN.md).

---

<!-- Chicago author–date -->
## 12. Referencias principales (columna metodológica)

- Brown, Neil C. C., and Mark Guzdial. 2024. “Confidence vs Insight: Big and Rich Data in Computing Education Research.” In *Proceedings of the 55th ACM Technical Symposium on Computer Science Education V. 1*, 158–64. https://doi.org/10.1145/3626252.3630813.
- Fischer, Björn, Berit Barthelmes, Sven Eric Panitz, Eva-Maria Iwer, and Ralf Dörner. 2024. “Seeking Consent for Programming Process Data Collection with Trustee-Based Encryption.” In *Proceedings of the 2024 ACM Conference on International Computing Education Research V.1*, 131–42. https://doi.org/10.1145/3632620.3671125.
- Heckman, Sarah, Jeffrey C. Carver, Mark Sherriff, and Ahmed Al-Zubidy. 2022. “A Systematic Literature Review of Empiricism and Norms of Reporting in Computing Education Research Literature.” *ACM Transactions on Computing Education* 22 (1): Article 3. https://doi.org/10.1145/3470652.
- McGill, Monica M., Sarah Heckman, Christos Chytas, et al. 2023. “Conducting Sound, Equity-Enabling Computing Education Research.” In *Proceedings of the 2023 Working Group Reports on Innovation and Technology in Computer Science Education*, 30–56. https://doi.org/10.1145/3623762.3633495.
- Runeson, Per, and Martin Höst. 2009. “Guidelines for Conducting and Reporting Case Study Research in Software Engineering.” *Empirical Software Engineering* 14 (2): 131–64. https://doi.org/10.1007/s10664-008-9102-8.
- Runeson, Per, Martin Höst, Austen Rainer, and Björn Regnell. 2012. *Case Study Research in Software Engineering: Guidelines and Examples*. Hoboken, NJ: Wiley. https://doi.org/10.1002/9781118181034.
- Wohlin, Claes, Per Runeson, Martin Höst, Magnus C. Ohlsson, Björn Regnell, and Anders Wesslén. 2012. *Experimentation in Software Engineering*. Berlin: Springer. https://doi.org/10.1007/978-3-642-29044-2.

Lista ampliada: `docs/public/research/methodology.md` (y versión ES).

---

## 13. Anexos de este protocolo

1. Instrumentos — `INSTRUMENTOS-RECOLECCION-DATOS-ES.md`  
2. Consentimiento e información — `PARTICIPANT-*-ES.md`  
3. Plan de manejo de datos — `PLAN-MANEJO-DATOS-ES.md`  
4. Autorizaciones — `AUTORIZACIONES-INSTITUCIONALES-ES.md`  
5. Solicitud al comité — `ETHICS-COMMITTEE-SUBMISSION-ES.md`  
6. Checklist del comunicado — `CHECKLIST-COMITE-ETICA-ES.md`
