<!--
Paquete institucional (distinto del CEI).
Autorización pedagógica + solicitud de fondos de producción.
-->

# Paquete institucional — autorización pedagógica y fondos

**Distinto del paquete CEI.** Este pack va a dirección/coordinación de grados, IP ECSIT
y (si procede) oficina de investigación / transferencia. El CEI recibe el Word +
`PAQUETE-REMISION-CEI-UDIT-ES.pdf`.

| Destinatario | Rol | Email |
| ------------ | --- | ----- |
| Sandra Garrido | Coordinación grados tecnológicos | `sandra.garrido@udit.es` |
| Fernando Blázquez Piñeiro | Dirección Full-Stack / Ciencia de Datos e IA | `fernando.blazquez@udit.es` |
| Rafael Conde Melguizo, PhD | IP grupo ECSIT | `rafael.conde@udit.es` |
| Dra. Adiela Batista Delgado | Directora OTRI / OTC | `otc@udit.es` |

## Dónde estaba el «draft» pedagógico

El encuadre interno ya existía aquí (no es el acta firmada):

- [`../DEPARTMENT-DECISION-BRIEF.md`](../DEPARTMENT-DECISION-BRIEF.md) — breve de decisión departamental
- Modelo corto en [`../ethics/AUTORIZACIONES-INSTITUCIONALES-ES.md`](../ethics/AUTORIZACIONES-INSTITUCIONALES-ES.md) §3

Lo que **faltaba** para enviar y firmar es la carta formal + hoja de conformidad
(este directorio) y el PDF tipográfico.

## Documentos

| Archivo | Uso |
| ------- | --- |
| [`SOLICITUD-AUTORIZACION-PEDAGOGICA-ES.md`](SOLICITUD-AUTORIZACION-PEDAGOGICA-ES.md) | Carta a Sandra + Fernando (A1) |
| [`SOLICITUD-PRESUPUESTO-PRODUCCION-ES.md`](SOLICITUD-PRESUPUESTO-PRODUCCION-ES.md) | Fondos ≥24 meses · caso agentico con gobernanza de procedencia / vía *DevOps* |
| [`PAQUETE-INSTITUCIONAL-DEPT-INVESTIGACION-ES.pdf`](PAQUETE-INSTITUCIONAL-DEPT-INVESTIGACION-ES.pdf) | Blend tipográfico (logos UDIT/ECSIT) + A1 + fondos + **Anexo 4 fundamentación / columna metodológica** + autoría IA/MIT |
| [`../ethics/DECLARACION-AUTORIA-ASISTIDA-POR-IA-ES.md`](../ethics/DECLARACION-AUTORIA-ASISTIDA-POR-IA-ES.md) | Fuente MD de la transparencia del PI |

```bash
cd docs/research/ethics/latex && make institucional
```
