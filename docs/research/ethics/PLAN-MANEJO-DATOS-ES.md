<!--
Plan de manejo de datos — anexo Comité de Ética / DPO.
Strand B · 2026-09-26.
-->

# Plan de manejo de datos (PMD)

**Estudio:** TTOD-Strand-B-FEII-2026-27  
**Versión:** 2026-09-26  
**Complemento técnico:** [`DATA-MINIMIZATION-STATEMENT.md`](DATA-MINIMIZATION-STATEMENT.md)

---

## 1. Resumen

Los datos de investigación son **trazas de proceso de programación y textos pedagógicos**
(commits/PRs, declaraciones de IA, notas estructuradas de defensa), seudonimizados. **No** se
recogen cuestionarios ni entrevistas en esta versión. Las calificaciones e identidades académicas
permanecen en sistemas docentes y **fuera** del corpus investigador.

---

## 2. Datos que se recogen / reutilizan

| Conjunto | Descripción | Identificadores |
| -------- | ------------ | --------------- |
| Corpus investigador | I1–I4 (ver instrumentos) | Seudónimos `P01…Pn`; sin nombre, email, DNI |
| Mapa seudónimo ↔ identidad | Solo para custodia / retirada | **Offline**, cifrado; no en git |
| Consentimientos firmados | Formularios | Custodia privada; no en git público |
| Datos docentes (notas) | Evaluación ordinaria | Sistemas UDIT; no se copian al corpus |

**Categorías especiales (Art. 9 RGPD):** no se recogen.

---

## 3. Base jurídica (propuesta a confirmar con DPO)

| Tratamiento | Base |
| ----------- | ---- |
| Docencia / evaluación | Relación académica / interés público educativo (marco institucional) |
| Uso investigador secundario del corpus seudonimizado | **Consentimiento** informado (Art. 6.1.a RGPD / LOPDGDD) |

---

## 4. Flujo de datos

```
Artefactos de evaluación (I1–I3)
        │
        ▼
Consentimiento B + dictamen ético
        │
        ▼
Seudonimización ──► Corpus investigador (acceso restringido)
        │
        ├── Análisis cualitativo / diseño
        │
        └── Difusión: agregados o extractos con consentimiento F/C4
```

---

## 5. Almacenamiento y seguridad

| Activo | Dónde | Medidas |
| ------ | ----- | ------- |
| Corpus seudonimizado | Almacenamiento institucional / cifrado del PI o custodio | Acceso mínimo; sin nube pública de estudiantes |
| Mapa seudónimo | Offline / *vault* cifrado | Separado del corpus |
| Consentimientos firmados | Archivo departamental / custodio | Ver `SIGNED-CONSENTS-CUSTODY.md` |
| Git del producto TTOD | Remotos del curso | No es el corpus investigador |

**Prohibido:** subir consentimientos firmados, mapas nominativos o notas al repositorio git
público/privado del proyecto TTOD documentado en este árbol.

---

## 6. Acceso

| Rol | Acceso |
| --- | ------ |
| PI | Análisis tras cierre de notas; preferible ceguera al consentimiento hasta entonces |
| Custodio independiente (si designado) | Consentimientos + mapa seudónimo |
| Co-investigación metodológica | Solo corpus seudonimizado, si autorizado |
| Comité / DPO | Bajo requerimiento institucional |

---

## 7. Conservación y destrucción

| Activo | Plazo propuesto (confirmar con institución) |
| ------ | --------------------------------------------- |
| Consentimientos | Fin del estudio + plazo institucional (p. ej. ≥5 años o norma UDIT) |
| Corpus seudonimizado | Hasta cierre de publicaciones del ciclo + archivo según política |
| Mapa seudónimo | Destruir cuando ya no sea necesario para retirada / auditoría |
| Publicaciones | Hallazgos agregados / no identificativos — permanentes |

---

## 8. Compartición y apertura

- **No** open data de repositorios estudiantiles ni de corpus nominativo.
- Artículos: agregados y extractos no identificativos.
- FAIR se aplica a **metadatos del estudio y artefactos docentes saneados**, no a datos
  personales de estudiantes.

---

## 9. Derechos de las personas participantes

Informados en la hoja de información: acceso, rectificación, retirada del consentimiento
investigador, limitación, reclamación ante autoridad de control. Contacto DPO:
`dpd@udit.es` / `proteccion.datos@udit.es`. CEI:
`comite.etica.investigacion@udit.es`.

---

## 10. Incidentes

Cualquier fuga o reidentificación se comunicará según protocolo institucional de seguridad /
protección de datos y se documentará para el comité si así se requiere.
