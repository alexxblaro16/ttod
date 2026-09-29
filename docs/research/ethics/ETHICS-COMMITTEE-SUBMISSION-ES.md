<!--
Dossier para el comité de ética / comisión ética de la universidad.
Strand B únicamente. No incluye Strand A.
Autor: Rubén Vega Balbás, PhD · 2026-09-25.
-->

# Solicitud de evaluación ética — Strand B (TTOD / Front-End II)

**Título del estudio:** Aprendizaje haciendo: participación como desarrollador/a en una aplicación real asistida por IA agentica, en grupo, como actividad formativa  
**Investigador principal:** Rubén Vega Balbás, PhD — Profesor de Desarrollo Web Front-End I/II, UDIT · ECSIT — `ruben.vega@udit.es`  
**Documento de diseño:** [`../STRAND-B-PEDAGOGICAL-DESIGN.md`](../STRAND-B-PEDAGOGICAL-DESIGN.md)  
**Protocolo completo (ES, remisión):** [`PROTOCOLO-INVESTIGACION-COMPLETO-ES.md`](PROTOCOLO-INVESTIGACION-COMPLETO-ES.md)  
**Checklist del comunicado:** [`CHECKLIST-COMITE-ETICA-ES.md`](CHECKLIST-COMITE-ETICA-ES.md)  
**Formulario CEI (relleno):** [`FORMULARIO-SOLICITUD-CEI-UDIT-ES.md`](FORMULARIO-SOLICITUD-CEI-UDIT-ES.md)  
**Minimización de datos:** [`DATA-MINIMIZATION-STATEMENT.md`](DATA-MINIMIZATION-STATEMENT.md)  
**Plan de manejo de datos:** [`PLAN-MANEJO-DATOS-ES.md`](PLAN-MANEJO-DATOS-ES.md)  
**Instrumentos:** [`INSTRUMENTOS-RECOLECCION-DATOS-ES.md`](INSTRUMENTOS-RECOLECCION-DATOS-ES.md)  
**Autorizaciones:** [`AUTORIZACIONES-INSTITUCIONALES-ES.md`](AUTORIZACIONES-INSTITUCIONALES-ES.md)  
**Plantillas de información y consentimiento:** `PARTICIPANT-*-ES.md`

---

## 1. Resumen ejecutivo (para el comité)

Se solicita evaluación ética de un **estudio de caso educativo / investigación basada en diseño**,
acotado a la asignatura Front-End II (curso 2026–27). El alumnado participa como **desarrolladores
en un producto real** (plataforma TTOD Oráculo), con asistencia de IA agentica y trabajo en
grupo. La actividad docente fue **autorizada pedagógicamente por el departamento** con
antelación al inicio. El alumnado ha recibido información y ha **firmado el consentimiento**
correspondiente (custodia fuera de este repositorio; ver
[`SIGNED-CONSENTS-CUSTODY.md`](SIGNED-CONSENTS-CUSTODY.md)).

**No se pretende** demostrar causalmente que la IA “mejora el aprendizaje”. Se pretende
describir, con trazas de proceso y defensa oral ya propias de la evaluación, **cómo se aprende
haciendo** en este entorno, y qué principios de diseño pedagógico se desprenden.

Una segunda línea de investigación **filosófica** (ontología / epistemología / cibernética /
Tao of Development) existe en el proyecto pero está **aparada** y **no forma parte** de esta
solicitud ni usa datos de estudiantes
([`../STRAND-A-PHILOSOPHICAL-PARKED.md`](../STRAND-A-PHILOSOPHICAL-PARKED.md)).

En paralelo, mantener Oráculo **en producción** sostiene una vía **operativa**: TTOD es un
**caso a escala reducida** de **aplicación agentica con gobernanza de procedencia** y
**corpus autorizado** propio (aforismos Tao). Eso permite estudiar, con datos reales de
operación, la infraestructura / *DevOps* de un sistema de conocimiento agentico con IA
local en producción — complementaria a la vía filosófica y a este estudio pedagógico.
Esa línea de fondos/producción **no** se tramita ante el CEI; se documenta en el paquete
institucional.

---

## 2. Pregunta de investigación

¿Puede la participación como desarrollador/a en una aplicación real, desarrollada con
asistencia agentica y en grupo de pares, constituir una actividad de aprendizaje con
resultados pedagógicos observables — *aprender haciendo*?

Preguntas subsidiarias: ver §1 de `STRAND-B-PEDAGOGICAL-DESIGN.md` (RQ-B1–B4).

**Tipo de estudio (para el comité):** estudio de caso educativo / investigación basada en
diseño, con **datos ricos de proceso de programación** (no ensayo clínico; no ensayo A/B de
herramienta; no inferencia poblacional). Plan de publicación: informe de experiencia / principios
de diseño en congreso (JENUI → ITiCSE), ver `STRAND-B-CONGRESS-PUBLICATION-PLAN.md`.

**Posicionamiento:** computación **post-introductoria** asistida por GenAI (laguna documentada
frente a la literatura centrada en CS1).

---

## 3. Participantes

| Aspecto | Descripción |
| ------- | ----------- |
| Población | Estudiantes matriculados en Front-End II que participan en la entrega del grupo TTOD |
| Tamaño | **n = 8** estudiantes-desarrolladores (*README* del proyecto, excluido el PI). Corpus investigador: solo consentimiento B (**n_consent ≤ 8**) |
| Menores / vulnerables | Si hubiera menores de edad o situaciones de especial vulnerabilidad, se aplicarán salvaguardas adicionales institucionales antes de incluir sus artefactos en el corpus investigador |
| Reclutamiento | No hay reclutamiento externo; la actividad es la propia asignatura. La **participación en investigación** (uso secundario de artefactos) es **voluntaria** e independiente de la nota |

---

## 4. Procedimiento

1. El alumnado desarrolla el producto según el plan docente (esqueleto aislado, PRs, pruebas,
   declaraciones de uso de IA, defensa).
2. La docencia y la evaluación discurren con normalidad **con o sin** consentimiento
   investigador.
3. Solo tras la autorización del comité y con consentimiento válido, se construye un **corpus
   pseudonimizado** de artefactos de proceso para análisis cualitativo / de diseño.
4. El análisis de ese corpus se inicia **después** de cerrar las calificaciones de los
   componentes relevantes, para reducir el conflicto docente–investigador.
5. Instrumentos adicionales (encuesta, entrevista, grabación) **no** se activan por defecto;
   si se activaran, requerirían ítems de consentimiento separados y, en su caso, una
   modificación de esta solicitud.

---

## 5. Datos personales: postura ante el comité

**Afirmación central:** el proyecto de investigación **no pone en riesgo datos personales de
estudiantes** como objeto de interés: no recoge categorías especiales, no indaga en la vida
privada, no publica identificadores, y limita el uso investigador a **trazas de proceso
pseudonimizadas** ya generadas por la evaluación ordinaria.

Detalle técnico-jurídico: [`DATA-MINIMIZATION-STATEMENT.md`](DATA-MINIMIZATION-STATEMENT.md).
Las calificaciones e identidades académicas permanecen en los sistemas docentes habituales y
**fuera** del corpus investigador.

---

## 6. Riesgos y beneficios

| Tipo | Descripción | Mitigación |
| ---- | ----------- | ---------- |
| Conflicto docente–investigador | El PI califica a quienes podrían consentir | Consentimiento y custodia preferiblemente independientes; ceguera del docente hasta cerrar notas; retirada sin efecto académico |
| Coerción percibida | Presión por jerarquía | Información clara; opt-in; nota no condicionada |
| Reidentificación | Texto de PRs o código | Pseudonimización; extractos publicados solo con consentimiento de difusión (C4) |
| Vigilancia excesiva | Telemetría de proceso | Minimización; no monitorización encubierta; ver Davalos & Zhang (2026) como advertencia de diseño |

**Beneficios:** mejora documentada del diseño docente; contribución a la literatura de
educación informática sobre aprendizaje auténtico con IA; ningún beneficio académico
individual por consentir.

---

## 7. Consentimiento informado

- Hoja de información: [`PARTICIPANT-INFORMATION-SHEET-ES.md`](PARTICIPANT-INFORMATION-SHEET-ES.md)
- Formulario: [`PARTICIPANT-CONSENT-FORM-ES.md`](PARTICIPANT-CONSENT-FORM-ES.md)
- Versiones EN disponibles para transparencia bilingüe.
- Firmados: custodia privada — [`SIGNED-CONSENTS-CUSTODY.md`](SIGNED-CONSENTS-CUSTODY.md)

Se distinguen explícitamente:

1. participación pedagógica en el proyecto del grupo;
2. consentimiento para uso investigador secundario y pseudonimizado.

---

## 8. Autorización pedagógica previa

La actividad como **práctica docente del grupo** fue presentada y respaldada en el marco
departamental **antes** de comenzar (ver
[`../DEPARTMENT-DECISION-BRIEF.md`](../DEPARTMENT-DECISION-BRIEF.md) y documentación de
asignatura). Esta solicitud ética **no** sustituye esa autorización docente; la complementa
para el uso investigador.

Adjuntar a la remisión institucional (fuera de git si contienen sellos o firmas):

- [ ] Confirmación / acta o correo de apoyo departamental
- [ ] Guía docente / encargo de la entrega (extracto)
- [ ] Esta solicitud + anexos de información y consentimiento
- [ ] Declaración de minimización de datos

---

## 9. Qué no se solicita aquí

- Aprobación de Strand A (filosófico).
- Autorización de publicación open-data de repositorios estudiantiles.
- Ensayo clínico, experimentación biomédica, o intervención psicológica clínica.
- Recogida de datos de menores sin protocolo específico.

---

## 10. Decisión solicitada al comité

1. Evaluar y, en su caso, **autorizar** el protocolo Strand B descrito.
2. Confirmar que el enfoque de **minimización / sin datos personales en riesgo** es adecuado
   o indicar condiciones adicionales.
3. Indicar si se requiere dictamen del delegado/a de protección de datos en paralelo.

---

## Anexos (rutas en repositorio — paquete del comunicado)

1. Protocolo completo: `PROTOCOLO-INVESTIGACION-COMPLETO-ES.md`
2. Consentimiento + información: `PARTICIPANT-CONSENT-FORM-ES.md`, `PARTICIPANT-INFORMATION-SHEET-ES.md`
3. Instrumentos: `INSTRUMENTOS-RECOLECCION-DATOS-ES.md`
4. Autorizaciones: `AUTORIZACIONES-INSTITUCIONALES-ES.md` (+ adjuntos firmados fuera de git)
5. Plan de manejo de datos: `PLAN-MANEJO-DATOS-ES.md`
6. Minimización: `DATA-MINIMIZATION-STATEMENT.md`
7. Checklist: `CHECKLIST-COMITE-ETICA-ES.md`
8. Diseño EN detalle: `docs/research/STRAND-B-PEDAGOGICAL-DESIGN.md`
9. Strand A aparada: `docs/research/STRAND-A-PHILOSOPHICAL-PARKED.md`
