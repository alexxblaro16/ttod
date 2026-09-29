# Ethics PDFs — student pack + CEI remisión + paquete institucional (XeLaTeX for 道)
STUDENT := HOJA-INFORMACION-Y-CONSENTIMIENTO-ES
REMISION := PAQUETE-REMISION-CEI-UDIT-ES
INSTITUCIONAL := PAQUETE-INSTITUCIONAL-DEPT-INVESTIGACION-ES
ASSETS := ../assets/udit-logo-print.png ../assets/ecsit-logo-print.png
COMMON := cei-common.tex
XELATEX := xelatex -interaction=nonstopmode
INSTITUCIONAL_OUT := ../../institutional/$(INSTITUCIONAL).pdf

export PATH := /Library/TeX/texbin:$(PATH)

.PHONY: all student remision institucional clean

all: student remision institucional

student: ../$(STUDENT).pdf

remision: ../$(REMISION).pdf

institucional: $(INSTITUCIONAL_OUT)

../$(STUDENT).pdf: $(STUDENT).tex $(COMMON) $(ASSETS)
	$(XELATEX) $(STUDENT).tex
	$(XELATEX) $(STUDENT).tex
	cp -f $(STUDENT).pdf ../$(STUDENT).pdf
	@echo "Wrote ../$(STUDENT).pdf"

../$(REMISION).pdf: $(REMISION).tex $(COMMON) $(ASSETS)
	$(XELATEX) $(REMISION).tex
	$(XELATEX) $(REMISION).tex
	cp -f $(REMISION).pdf ../$(REMISION).pdf
	@echo "Wrote ../$(REMISION).pdf"

$(INSTITUCIONAL_OUT): $(INSTITUCIONAL).tex $(COMMON) $(ASSETS)
	$(XELATEX) $(INSTITUCIONAL).tex
	$(XELATEX) $(INSTITUCIONAL).tex
	mkdir -p ../../institutional
	cp -f $(INSTITUCIONAL).pdf $(INSTITUCIONAL_OUT)
	@echo "Wrote $(INSTITUCIONAL_OUT)"

clean:
	rm -f *.aux *.log *.out *.toc $(STUDENT).pdf $(REMISION).pdf $(INSTITUCIONAL).pdf
