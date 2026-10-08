<!--
Ethics package index — Strand B only. Signed PII never enters git.
Aligned with COMUNICADO DEL COMITÉ DE ÉTICA DE INVESTIGACIÓN requirements.
-->

# Ethics package — Strand B (pedagogical case)

**Canonical research design (EN detail):** [`../STRAND-B-PEDAGOGICAL-DESIGN.md`](../STRAND-B-PEDAGOGICAL-DESIGN.md)  
**Parked philosophical strand:** [`../STRAND-A-PHILOSOPHICAL-PARKED.md`](../STRAND-A-PHILOSOPHICAL-PARKED.md)  
**Checklist vs comité comunicado:** [`CHECKLIST-COMITE-ETICA-ES.md`](CHECKLIST-COMITE-ETICA-ES.md)

## Remisión al Comité (documentos ES)

| Requisito del comunicado | Archivo |
| ------------------------ | ------- |
| Protocolo completo | [`PROTOCOLO-INVESTIGACION-COMPLETO-ES.md`](PROTOCOLO-INVESTIGACION-COMPLETO-ES.md) |
| Consentimiento informado | [`PARTICIPANT-CONSENT-FORM-ES.md`](PARTICIPANT-CONSENT-FORM-ES.md) + [`PARTICIPANT-INFORMATION-SHEET-ES.md`](PARTICIPANT-INFORMATION-SHEET-ES.md) |
| PDF estudiante (info + consentimiento) | [`HOJA-INFORMACION-Y-CONSENTIMIENTO-ES.pdf`](HOJA-INFORMACION-Y-CONSENTIMIENTO-ES.pdf) · fuente LaTeX [`latex/`](latex/) |
| Instrumentos de recolección | [`INSTRUMENTOS-RECOLECCION-DATOS-ES.md`](INSTRUMENTOS-RECOLECCION-DATOS-ES.md) |
| Autorizaciones institucionales | [`AUTORIZACIONES-INSTITUCIONALES-ES.md`](AUTORIZACIONES-INSTITUCIONALES-ES.md) + adjuntos firmados |
| Plan de manejo de datos | [`PLAN-MANEJO-DATOS-ES.md`](PLAN-MANEJO-DATOS-ES.md) |
| Otra documentación | [`ETHICS-COMMITTEE-SUBMISSION-ES.md`](ETHICS-COMMITTEE-SUBMISSION-ES.md), [`AUTORIA-LICENCIA-COHORTE-ES.md`](AUTORIA-LICENCIA-COHORTE-ES.md), [`DECLARACION-AUTORIA-ASISTIDA-POR-IA-ES.md`](DECLARACION-AUTORIA-ASISTIDA-POR-IA-ES.md), [`DATA-MINIMIZATION-STATEMENT.md`](DATA-MINIMIZATION-STATEMENT.md), Strand A parked |
| Formulario CEI (campos MD) | [`FORMULARIO-SOLICITUD-CEI-UDIT-ES.md`](FORMULARIO-SOLICITUD-CEI-UDIT-ES.md) |
| Formulario CEI (Word relleno) | [`FORMULARIO-SOLICITUD-CEI-UDIT-RELLENO.docx`](FORMULARIO-SOLICITUD-CEI-UDIT-RELLENO.docx) |
| **PDF remisión CEI (anexos blended)** | [`PAQUETE-REMISION-CEI-UDIT-ES.pdf`](PAQUETE-REMISION-CEI-UDIT-ES.pdf) |

## Qué enviar al CEI (mínimo)

1. **Formulario** — `FORMULARIO-SOLICITUD-CEI-UDIT-RELLENO.docx`
2. **Anexos blended** — `PAQUETE-REMISION-CEI-UDIT-ES.pdf` (carta, protocolo, instrumentos, PMD, autorizaciones, consentimiento, exclusión filosófica, **autoría asistida por IA del PI**, **autoría/MIT del grupo**; mismos logos UDIT/ECSIT)
3. **Adjuntos firmados** fuera de git (A1 departamental; consentimientos según vía del CEI)

```bash
cd docs/research/ethics/latex && make remision   # anexos
cd docs/research/ethics/latex && make student    # PDF estudiante (opcional aparte)
python3 docs/research/ethics/scripts/fill_cei_formulario.py  # regenerar Word
```

## Repository policy

- **In git:** templates, protocol, instruments inventory, DMP, checklists.
- **Never in git:** signed PDFs, student names, emails, grade sheets, interview audio.

## Dual consent (do not conflate)

1. **Project / pedagogical participation** (form items A + **H**): develop the product; MIT code
   license; named authorship in README by area.  
2. **Research consent** for secondary pseudonymized use (form item B).  
3. **Optional image** (form item G) — separate from README product credit.
