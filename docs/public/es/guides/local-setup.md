---
title: Ejecutar la referencia en local
eyebrow: Guía de evaluación local
description: Un camino público y seguro desde el clon del repositorio hasta una experiencia TTOD local verificada.
permalink: /es/guides/local-setup/
lang: es
---

# Del clon a un hello world que se ve

La aplicación está pensada para ejecutarse en local mediante Docker Compose. Esta guía cubre solo las operaciones necesarias para la docencia y la evaluación de front-end.

## Requisitos previos

- Git
- Docker Desktop o un motor Docker compatible con Compose
- `make` (opcional pero recomendado — ver la nota sobre Windows más abajo si no estás seguro de tenerlo)
- Espacio libre suficiente para las imágenes de contenedor y el modelo de lenguaje local
- Un navegador

## Clonar

```bash
git clone https://github.com/ruvebal/ttod.git
cd ttod
```

## Arranque

Desde la raíz del repositorio (el directorio `ttod` recién clonado), el camino simple:

```bash
make up
make ollama-pull
```

`make up` copia `.env.example` a un `.env` local no versionado automáticamente si aún no existe
(no hace falta editar ningún valor — esta pila no necesita credenciales), construye y arranca todos
los servicios, incluido Redis y el contenedor propio de Ollama de la aplicación, e imprime la URL
que hay que abrir. Redis es el almacén de **orilla** (cuentas, sesiones, biblioteca personal y
borradores de propuestas; AOF en `./data/redis` en el host). No sustituye el corpus gobernado
`ttod.yml` — ese sigue siendo el templo, aceptado solo por la CLI de revisión humana.
`make ollama-pull` descarga los dos modelos locales que necesita la pila — el modelo de chat
pequeño para el Oráculo y `nomic-embed-text` para la recuperación de citas — hazlo una vez,
justo después de `make up`; puede tardar unos minutos en un volumen nuevo y solo hace falta
repetirlo si más adelante eliminas ese volumen.

**Sin `make`**, los mismos pasos a mano:

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
docker compose exec ollama ollama pull llama3.2:1b
docker compose exec ollama ollama pull nomic-embed-text
```

**¿Tienes `make` disponible?** macOS y Linux lo traen de serie. Windows no — pero Docker Desktop en
Windows necesita de todos modos el backend WSL2, y una terminal WSL2 (no PowerShell ni cmd.exe) ya
tiene `make`, o se instala con `sudo apt install make`. Si estás en un PC Windows compartido o del
centro educativo y no sabes si WSL2 está configurado, usa el bloque sin `make` de arriba desde
PowerShell — `docker compose` se comporta igual en ambos casos; solo cambia el atajo de conveniencia.

Usa el mapeo de puertos que informe `docker compose ps` (por defecto `http://localhost:8080`) para
abrir el servicio web. Nunca confirmes `.env`, credenciales ni coordenadas propias de una máquina.

## Verificar el recorrido

1. Abre la página de bienvenida localizada.
2. Visita una cita y confirma que se ven el texto, el idioma, el origen y los derechos.
3. Abre la documentación y una relación del grafo.
4. Si el modelo local del Oracle está listo, envía una pregunta breve y comprueba sus fuentes o la indicación de modo creativo.
5. Confirma el foco de teclado y la retroalimentación de estado o de error en los controles interactivos.

El contenido y el grafo siguen siendo útiles cuando el modelo opcional del Oracle no está disponible. Una respuesta generada plausible no es la fuente canónica y puede ser incompleta o errónea.

## Inspeccionar y detener

```bash
docker compose logs --tail=100
docker compose down
```

Detener contenedores no debería eliminar volúmenes de datos con nombre ni el directorio bind de
Redis (`./data/redis`). Bórralos solo cuando pretendas de propósito descartar datos locales del
modelo o de la orilla/aplicación y comprendas el coste de recuperación.

## Bloqueos habituales

- **Puerto ya en uso:** elige un mapeo alternativo documentado; no detengas a ciegas contenedores ajenos.
- **El Oráculo se queda colgado o falla en una instalación nueva:** probablemente el modelo de chat
  o el de embeddings aún no se ha descargado — ejecuta `make ollama-pull` (o las dos líneas
  `docker compose exec ollama ollama pull …` de arriba) una vez; no es automático en `make up`
  porque es una descarga de varios minutos que solo hace falta una vez.
- **El modelo sigue descargándose:** usa las áreas de contenido no generativo mientras termina.
- **Oracle no disponible:** verifica por separado la salud del servicio y que estén presentes tanto
  `llama3.2:1b` como `nomic-embed-text` (`docker compose exec ollama ollama list`).
- **Una ruta se renderiza pero los datos están vacíos:** inspecciona la respuesta de red del navegador y los registros del servicio sin pegar secretos en una incidencia.
- **Biblioteca / login / propuestas responden 503:** Redis no está disponible. Comprueba
  `docker compose ps redis` y `docker compose logs --tail=100 redis`; no sustituyas `REDIS_URL`
  por una credencial confirmada en el repositorio.

Para pedir apoyo, informa el comando, la ruta, el sistema operativo y el error exacto. Sustituye rutas personales, nombres de usuario, nombres de máquina, direcciones, tokens y valores de entorno por marcadores seguros.
