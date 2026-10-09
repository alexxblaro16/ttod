---
title: Usar la API
eyebrow: Guía de la API
description: La superficie HTTP de TTOD, sus dos credenciales separadas, y un cliente de ejemplo ejecutable que demuestra que no son intercambiables.
permalink: /es/guides/api/
lang: es
---

# Dos credenciales, y por qué son dos

TTOD emite dos credenciales y no son intercambiables. Entender eso es casi todo
lo que hay que saber de la API.

Una **cookie de sesión** (`ttod_session`) es la que usan las páginas
renderizadas en servidor. Es `HttpOnly`, viaja solo en la cabecera `Cookie` e
identifica a una persona navegando por el sitio.

Un **token de acceso personal** (PAT) es el que usa un script. Viaja en
`Authorization: Bearer …`, se emite desde una sesión ya existente en
`POST /api/v1/auth/token`, y va firmado con un secreto y una sal distintos de
los de la sesión.

La consecuencia es deliberada: una cookie robada no se puede presentar como
token, y un PAT filtrado no abre una sesión de navegador. Cualquier uso cruzado
responde `401`. El cliente de ejemplo comprueba exactamente eso.

## Endpoints

La URL base es la propia aplicación — `http://localhost:8080` en una ejecución
local con Compose — porque Caddy redirige `/api/*` al backend.

| Método y ruta | Credencial | Respuesta |
| --- | --- | --- |
| `POST /api/v1/auth/login` | ninguna (correo + contraseña) | `200` con `AuthLoginResponse`; `401` si las credenciales no valen |
| `GET /api/v1/auth/session` | cookie de sesión | `200` con `AuthUser`; `401` sin cookie válida |
| `POST /api/v1/auth/token` | cookie de sesión | `200` con `access_token`, `token_type: "Bearer"` y `expires_in` |
| `GET /api/v1/wisdom/random` | **solo Bearer** | `200` con un `WisdomEntry`; `401` a cualquier otra cosa |
| `GET /api/v1/wisdom/sample` | ninguna | `200` con el corpus público |
| `POST /api/v1/proposals` | cookie de sesión | `201` con `{ proposal_id, status }` |
| `GET /api/v1/schema/definitions` | ninguna | `200` con las definiciones del esquema |
| `GET /health` | ninguna | `200` con `{ status, ttod_version }` |

## Las formas son los tipos compartidos

El JSON que viaja por el cable es el mismo contrato contra el que compila el
frontend, en `services/frontend/src/types/domain.ts`. Aquí no se inventa nada.

`AuthUser` — lo que devuelve `GET /api/v1/auth/session`, y lo que va bajo
`user` en la respuesta del login:

```json
{ "id": "usr-001", "email": "<la dirección de la cuenta>", "roles": ["reviewer", "instructor"] }
```

`roles` es una lista de `SessionRole`: `student`, `reviewer` o `instructor`.
No existe un `role` en singular ni un rol `admin` — un cliente que ramifique
por cualquiera de los dos está leyendo un contrato antiguo.

`AuthLoginResponse` añade el material de sesión alrededor de ese usuario:

```json
{ "session_token": "…", "token_type": "Session", "expires_in": 3600, "user": { … } }
```

`WisdomEntry` es una cita del corpus: `id`, `section`, `level`, `text`,
`teaches`, `tags`, más `subsection` opcional y un bloque `rights`.
`POST /api/v1/proposals` responde con `proposal_id` y `status` y nada más: el
servidor es el dueño de `origin` y de la identidad de quien propone, así que
enviarlos se rechaza con `422`.

## Recorrerlo con curl

Inicia sesión y guarda el token:

```bash
SESSION=$(curl -s -X POST http://localhost:8080/api/v1/auth/login \
  -H 'content-type: application/json' \
  -d '{"email":"'"$TTOD_ADMIN_EMAIL"'","password":"'"$TTOD_ADMIN_PASSWORD"'"}' \
  | python -c 'import json,sys; print(json.load(sys.stdin)["session_token"])')
```

Emite un token a partir de ella y llama a la ruta que solo acepta Bearer:

```bash
PAT=$(curl -s -X POST http://localhost:8080/api/v1/auth/token \
  -b "ttod_session=$SESSION" \
  | python -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')

curl -s http://localhost:8080/api/v1/wisdom/random -H "Authorization: Bearer $PAT"
```

Ahora intenta usar cada credencial donde va la otra. Las cuatro dan `401`:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/api/v1/wisdom/random -b "ttod_session=$SESSION"
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/api/v1/wisdom/random -H "Authorization: Bearer $SESSION"
curl -s -o /dev/null -w '%{http_code}\n' -X POST http://localhost:8080/api/v1/auth/token -H "Authorization: Bearer $PAT"
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/api/v1/wisdom/random
```

Enviar una propuesta exige la sesión, y responde `201`:

```bash
curl -s -X POST http://localhost:8080/api/v1/proposals \
  -b "ttod_session=$SESSION" -H 'content-type: application/json' \
  -d '{"text":"Una cita que merece la pena proponer.","section":"wisdom","level":"intermediate","lang":"es"}'
# {"proposal_id":"7b0445e8-92f4-436e-a5b3-8b43594d6a57","status":"proposed"}
```

Una propuesta es un borrador. Desde aquí nunca llega a `ttod.yml`: publicar pasa
por el pipeline de revisión y por `cli.py proposal accept --reviewer-id …`, que
describe la [guía de contribución]({{ '/es/guides/contributing/' | relative_url }}).

## Cómo verificarlo

`examples/api_client.py` es el mismo recorrido en un único script, sin más
dependencias que la biblioteca estándar. Ejecútalo contra una instancia viva:

```bash
python examples/api_client.py \
  --base-url http://localhost:8080 \
  --email "$TTOD_ADMIN_EMAIL" \
  --password "$TTOD_ADMIN_PASSWORD"
```

Salida esperada:

```
1. logged in as <la dirección de la cuenta> with roles ['reviewer', 'instructor']
2. the cookie resolves to AuthUser usr-001
3. minted a bearer token valid for 3600s
4. rrp-019 (remote-repo): Un informe para gobernarlos a todos, un gráfico para hallarlos...
5. all four cross-credential attempts were refused with 401

The API honours the documented contract.
```

La cita del paso 4 cambia en cada ejecución: ese endpoint es aleatorio por
diseño. Si algún paso no coincide con esta página, el script imprime
`CONTRACT BROKEN:` con el estado que recibió y termina con código distinto de
cero, de modo que sirve como prueba de humo en un pipeline y no solo para que
lo lea una persona.
