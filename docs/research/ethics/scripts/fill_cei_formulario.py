#!/usr/bin/env python3
"""Fill the UDIT CEI Word template from Strand B field values (iterable).

Usage:
  python3 fill_cei_formulario.py \\
    --template "/path/to/Formulario ..._WORD.docx" \\
    --out "/path/to/FORMULARIO-SOLICITUD-CEI-UDIT-RELLENO.docx"

Defaults point at the studio paths used for the 2026-09-26 Strand B remisión.
Re-run after editing FIELDS below (or pass --fields JSON later).
"""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
ETHICS_DIR = REPO_ROOT / "docs" / "research" / "ethics"
TEMPLATE_NAME = "Formulario de Solicitud de Evaluacion Etica_WORD.docx"

# ---------------------------------------------------------------------------
# Field values — keep in sync with FORMULARIO-SOLICITUD-CEI-UDIT-ES.md
# ---------------------------------------------------------------------------

FIELDS: dict = {
    "fecha_presentacion": "26 septiembre 2026",
    "codigo_proyecto": "TTOD (TTOD-Strand-B-FEII-2026-27)",
    "nombre": "Rubén Vega Balbás",
    "cargo": "Profesor Adjunto; Investigador grupo ECSIT",
    "departamento": "Área de Tecnología",
    "email": "ruben.vega@udit.es",
    "telefono": "659 340 115",
    "titulo_proyecto": (
        "The Tao of Development (TTOD) — investigación pedagógica "
        "asociada a la asignatura Front-End II (Strand B)."
    ),
    "titulo_estudio": (
        "Aprendizaje haciendo: participación como desarrollador/a en una "
        "aplicación real asistida por IA agentica, en grupo, como actividad formativa."
    ),
    "investigador_principal": (
        "No aplica — el solicitante es el investigador principal (PI)."
    ),
    "otros_investigadores": (
        "Ninguno en esta versión del protocolo. "
        "(Si se incorporara co-investigación metodológica, se notificará al CEI.)"
    ),
    "resumen": (
        "Se solicita evaluación ética de un estudio de caso educativo / investigación "
        "basada en diseño, acotado a Front-End II (curso 2026–27). El alumnado participa "
        "como desarrolladores en un producto real (plataforma TTOD Oráculo), con asistencia "
        "de IA agentica, trabajo en grupo, revisiones por pull request y defensa oral. "
        "La actividad docente fue autorizada pedagógicamente por el departamento con "
        "antelación; la participación en investigación (uso secundario seudonimizado de "
        "artefactos de proceso) es voluntaria e independiente de la calificación. "
        "Objetivo: describir cómo se aprende haciendo en este entorno y qué principios de "
        "diseño pedagógico se desprenden — no demostrar causalmente que la IA «mejora el "
        "aprendizaje», ni estimar tamaños de efecto poblacionales. "
        "Metodología: caso único acotado, cualitativo dominante, con datos ricos de proceso "
        "de programación (commits/PRs, declaraciones de uso de IA, notas estructuradas de "
        "defensa), seudonimizados tras consentimiento. Sin cuestionarios ni entrevistas en "
        "el diseño mínimo. El análisis investigador comienza tras dictamen ético, "
        "consentimiento válido y cierre de las calificaciones relevantes. "
        "Relevancia: contribuye a la educación informática post-introductoria con GenAI y "
        "documenta un diseño de studio / learning-by-doing transferible a grupos similares. "
        "Una línea filosófica paralela (Strand A) está aparada y no usa datos de estudiantes "
        "ni forma parte de esta solicitud."
    ),
    "n_participantes": (
        "8 estudiantes-desarrolladores del grupo TTOD (Front-End II / entrega "
        "de producto), auto-listados en el README del repositorio del proyecto "
        "(excluido el PI/docente). El corpus investigador incluirá solo a quienes "
        "otorguen consentimiento B (n_consent ≤ 8)."
    ),
    "inclusion": (
        "Estudiantes matriculados en Front-End II que participan en la entrega del grupo "
        "TTOD y otorgan consentimiento informado para el uso investigador secundario "
        "seudonimizado de artefactos de proceso (ítem B)."
    ),
    "exclusion": (
        "Quienes no consienten el uso investigador; menores de edad o situaciones de "
        "especial vulnerabilidad sin salvaguarda adicional institucional aprobada; "
        "artefactos de compañeros no consentidos."
    ),
    "procedimientos": (
        "No se introducen entrevistas, cuestionarios ni pruebas médicas. Los sujetos "
        "realizan la actividad docente ordinaria (desarrollo del producto, PRs, declaración "
        "de uso de IA, defensa oral). El procedimiento investigador consiste en el uso "
        "secundario seudonimizado de esas trazas de proceso ya generadas para evaluación, "
        "solo tras consentimiento y dictamen del CEI. Instrumentos activos: I1 historial "
        "commits/PRs; I2 declaración de IA; I3 notas estructuradas de defensa (sin "
        "audio/vídeo); I4 extractos de código solo con consentimiento de difusión."
    ),
    "justificacion_sin_consentimiento": "No aplica (sí se solicita consentimiento escrito).",
    "medidas_proteccion": (
        "Seudonimización (P01…Pn); mapa seudónimo↔identidad offline/cifrado y separado; "
        "corpus de acceso restringido; sin nube pública de datos de estudiantes; sin "
        "publicación de nombres, emails, fotos ni handles identificables; extractos "
        "publicados solo con consentimiento de difusión; análisis preferente tras cierre "
        "de notas; retirada del consentimiento investigador sin efecto académico. "
        "No se recogen categorías especiales (art. 9 RGPD). Detalle en anexos "
        "PLAN-MANEJO-DATOS-ES y DATA-MINIMIZATION-STATEMENT."
    ),
    "periodo_conservacion": (
        "Consentimientos: fin del estudio + plazo institucional (propuesta ≥ 5 años o "
        "norma UDIT). Corpus seudonimizado: hasta cierre de publicaciones del ciclo + "
        "archivo según política. Mapa seudónimo: destruir cuando deje de ser necesario "
        "para retirada/auditoría. Confirmar con DPO (dpd@udit.es / proteccion.datos@udit.es)."
    ),
    "riesgos_detalle": (
        "Riesgos bajos / no médicos: (1) conflicto docente–investigador — mitigado con "
        "ceguera al consentimiento hasta cerrar notas y retirada sin efecto en calificación; "
        "(2) coerción percibida — opt-in, nota no condicionada; (3) reidentificación — "
        "seudonimización y consentimiento de difusión para extractos; (4) vigilancia "
        "excesiva — minimización, sin telemetría encubierta ni grabación en el diseño mínimo."
    ),
    "beneficios": (
        "Mejora documentada del diseño docente; contribución a la literatura de educación "
        "informática sobre aprendizaje auténtico con IA agentica; ningún beneficio académico "
        "individual por consentir. Principios de diseño situados transferibles a grupos "
        "post-introductorios similares (sin inferencia causal poblacional)."
    ),
    "otra_documentacion": (
        "Solicitud narrativa ETHICS-COMMITTEE-SUBMISSION-ES; declaración Strand A aparada; "
        "brief / autorización departamental (adjunto firmado pendiente); extracto guía "
        "docente; checklist del comunicado."
    ),
    "firma_nota": "[firma manuscrita o electrónica del solicitante]",
    "fecha_firma": "26/09/2026",
}

# Paragraph indices that should be checked (☐ → ☑). Discovered from the UDIT template.
CHECK_PARAS = {
    36,  # humanos Sí
    46,  # consentimiento Sí
    51,  # Escrito
    59,  # datos personales Sí
    67,  # eliminación digital
    68,  # destrucción física
    76,  # riesgos Sí
    84,  # cumple normativas Sí
    87,  # otro CEI No
    94,
    95,
    96,
    97,
    98,
    99,  # anexos
}

# Append inline text after label (same paragraph).
APPEND_INLINE: dict[int, str] = {
    6: " {codigo_proyecto}",
    11: "{nombre}",
    12: "{cargo}",
    13: "{departamento}",
    14: " {email}",
    16: "{telefono}",
    21: " {titulo_proyecto}",
    23: " {investigador_principal}",
    25: " {otros_investigadores}",
    26: " — (no aplica en esta versión)",
    38: " {n_participantes}",
    39: " {inclusion}",
    40: " {exclusion}",
    48: " {justificacion_sin_consentimiento}",
    61: " {medidas_proteccion}",
    63: " {periodo_conservacion}",
    78: " {beneficios}",
    99: " {otra_documentacion}",
    107: " {firma_nota}",
}

# Replace placeholder patterns inside a paragraph.
REPLACE_IN_PARA: dict[int, list[tuple[str, str]]] = {
    5: [("//", "{fecha_presentacion}")],
    22: [
        (
            "_____________________________________",
            "{titulo_estudio}",
        )
    ],
    109: [("//", "{fecha_firma}")],
}

# Insert new body paragraphs AFTER these indices (content may be multi-paragraph).
INSERT_AFTER: dict[int, list[str]] = {
    30: ["{resumen}"],  # after the "(Explicar…)" hint
    41: ["{procedimientos}"],
    76: ["{riesgos_detalle}"],
}


def _esc(text: str) -> str:
    return html.escape(text, quote=False)


def _fmt(template: str) -> str:
    return template.format(**FIELDS)


def _run(text: str, *, bold: bool = False) -> str:
    b = "<w:b/>" if bold else ""
    return (
        "<w:r>"
        f"<w:rPr><w:rFonts w:ascii=\"Times New Roman\" w:hAnsi=\"Times New Roman\"/>"
        f"<w:color w:val=\"221F1F\"/><w:sz w:val=\"22\"/>{b}</w:rPr>"
        f'<w:t xml:space="preserve">{_esc(text)}</w:t>'
        "</w:r>"
    )


def _para(text: str) -> str:
    """Simple body paragraph matching the template's independent-text style."""
    return (
        '<w:p w14:paraId="F1LL0001" w14:textId="77777777" '
        'w:rsidR="009440F7" w:rsidRDefault="00236098">'
        "<w:pPr>"
        '<w:pStyle w:val="Textoindependiente"/>'
        '<w:spacing w:before="60" w:after="60"/>'
        '<w:rPr><w:sz w:val="22"/></w:rPr>'
        "</w:pPr>"
        f"{_run(text)}"
        "</w:p>"
    )


def _check_box(part: bytes) -> bytes:
    return part.replace("☐".encode("utf-8"), "☑".encode("utf-8"), 1)


def _append_run(part: bytes, text: str) -> bytes:
    return part + _run(text).encode("utf-8")


def _replace_in_part(part: bytes, old: str, new: str) -> bytes:
    return part.replace(_esc(old).encode("utf-8"), _esc(new).encode("utf-8")).replace(
        old.encode("utf-8"), _esc(new).encode("utf-8")
    )


def fill_document_xml(xml: bytes) -> bytes:
    parts = re.split(rb"(</w:p>)", xml)
    # parts alternate: content, </w:p>, content, </w:p>, ...
    # Reconstruct as list of (para_body, closer) pairs for real paragraphs.
    out: list[bytes] = []
    para_i = -1
    i = 0
    while i < len(parts):
        chunk = parts[i]
        if i + 1 < len(parts) and parts[i + 1] == b"</w:p>":
            para_i += 1
            body = chunk
            closer = parts[i + 1]

            if para_i in CHECK_PARAS:
                body = _check_box(body)

            if para_i in REPLACE_IN_PARA:
                for old, new_tmpl in REPLACE_IN_PARA[para_i]:
                    body = _replace_in_part(body, old, _fmt(new_tmpl))

            if para_i in APPEND_INLINE:
                body = _append_run(body, _fmt(APPEND_INLINE[para_i]))

            # GDPR acceptance: list bullet without ☐ — mark explicitly
            if para_i == 117:
                body = _append_run(body, "  ☑ Aceptado por el solicitante.")

            out.append(body)
            out.append(closer)

            if para_i in INSERT_AFTER:
                for tmpl in INSERT_AFTER[para_i]:
                    text = _fmt(tmpl)
                    # Split very long text into ~500-char soft paragraphs at sentence ends
                    for piece in _chunk_sentences(text, 550):
                        out.append(_para(piece).encode("utf-8"))

            i += 2
        else:
            out.append(chunk)
            i += 1

    return b"".join(out)


def _chunk_sentences(text: str, max_len: int) -> list[str]:
    if len(text) <= max_len:
        return [text]
    chunks: list[str] = []
    buf = ""
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if buf and len(buf) + 1 + len(sentence) > max_len:
            chunks.append(buf)
            buf = sentence
        else:
            buf = f"{buf} {sentence}".strip() if buf else sentence
    if buf:
        chunks.append(buf)
    return chunks


def fill_docx(template: Path, out: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        with zipfile.ZipFile(template, "r") as zin:
            zin.extractall(work)
        # Strip symlink entries (untrusted docx hygiene)
        for p in work.rglob("*"):
            if p.is_symlink():
                p.unlink()

        doc_xml = work / "word" / "document.xml"
        filled = fill_document_xml(doc_xml.read_bytes())
        doc_xml.write_bytes(filled)

        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            out.unlink()
        with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for path in sorted(work.rglob("*")):
                if path.is_file():
                    zout.write(path, path.relative_to(work).as_posix())


def default_template_path() -> Path:
    if env := os.environ.get("UDIT_CEI_TEMPLATE"):
        return Path(env).expanduser()
    return Path(os.path.expanduser("~")) / "projects" / "ruvebal" / "scholar" / "udit" / "research" / TEMPLATE_NAME


def main() -> None:
    default_template = default_template_path()
    default_out = ETHICS_DIR / "FORMULARIO-SOLICITUD-CEI-UDIT-RELLENO.docx"
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--template", type=Path, default=default_template)
    ap.add_argument("--out", type=Path, default=default_out)
    args = ap.parse_args()
    if not args.template.is_file():
        raise SystemExit(f"Template not found: {args.template}")
    fill_docx(args.template, args.out)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
