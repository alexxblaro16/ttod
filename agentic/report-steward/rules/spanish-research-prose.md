# Spanish research / institutional prose

Applies to `docs/research/ethics/`, `docs/research/institutional/`, and Spanish LaTeX
packs under `docs/research/ethics/latex/` (`*-ES.tex`, `*-ES.md`).

## Columna metodológica (not «espina»)

In Spanish, call the methods backbone **columna metodológica**. Never write
«espina metodológica» (sounds odd). English internal comments may still say
“methods spine / backbone.”

## Citation style label (invisible)

Do **not** put «Chicago», «Chicago author–date», or «(Chicago)» in visible headings
or running text — readers see author–date entries and do not need the label.
Keep the style name only in HTML/Markdown/LaTeX **comments**, e.g.:

```html
<!-- Chicago author–date -->
```

```latex
% Chicago author–date
\subsection*{Referencias principales}
```

## Foreign / English terms → italics

Any English or otherwise non-Spanish word left in Spanish prose must be in italics
(`*word*` in Markdown; `\emph{word}` in LaTeX). Examples: *vault*, *harness*,
*README*, *Development Team*, *cohort starter*, *inbound*, *outbound*, *pull request*
(or keep *PR* if already established). Proper nouns that are brands/URLs
(`crea-comm.net`, `udit.es`) stay upright. Institutional Spanish acronyms already
in Spanish use (CEI, RGPD, OTRI, ECSIT, UDIT) stay upright. File names and paths
in monospace (`\texttt{…}` / backticks) do not also need italics.
