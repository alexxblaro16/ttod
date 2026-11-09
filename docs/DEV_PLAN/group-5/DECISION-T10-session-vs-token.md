# Tarea 10 — Decisión de diseño: dos credenciales, una sesión web y un token de API

> Ficha: `docs/DEV_PLAN/ASSIGNMENTS/ASSIGNMENT-accounts-task10.md` · módulo Accounts (Equipo 5)
> Las rutas y líneas citadas se refieren a la punta de este PR, que parte de `main` con la fase Z
> (Redis) ya integrada. Se pueden abrir en este mismo commit.

## Contexto

La costura de cuentas tiene dos tipos de cliente:

- **El navegador**, que entra con correo y contraseña y luego navega por páginas renderizadas en el
  servidor (Astro SSR): cuenta, biblioteca, cola del revisor, proponer una cita.
- **Un programa**, que llama a la API pública `GET /api/v1/wisdom/random` sin navegador (la guía de
  la Tarea 6, `docs/public/guides/api.md`, y su `api_client`).

Los dos necesitan demostrar quién son. La decisión es si lo demuestran con **la misma credencial**
o con **dos credenciales que no se pueden intercambiar**.

## Opciones consideradas

1. **Una sola credencial: un token Bearer para todo.** El login devuelve un token, el frontend lo
   guarda en una cookie legible (`ttod_access_token`) y lo manda como `Authorization: Bearer` en
   cada petición, tanto en las páginas como en la API pública.
2. **Dos credenciales separadas.** El navegador recibe una **sesión** que solo viaja en la cookie
   `ttod_session` (`httpOnly`, `SameSite=Lax`). Un programa pide aparte un **PAT** con
   `POST /api/v1/auth/token` (que exige sesión) y lo manda como Bearer. Cada ruta acepta una sola
   de las dos.

La opción 1 no es teórica: es la que había en nuestra rama antes del commit `11ef3c7`
(«separate the web session from bearer tokens and unify SSR guards», 08/10/2026). Ahí estaban el
`auth.ts` del frontend con `ttod_access_token` mandado como Bearer y un `AuthService` con un único
serializador para todo.

## Decisión

Se eligió la **opción 2**. Dónde vive cada pieza:

| Pieza | Fichero | Qué garantiza |
| --- | --- | --- |
| Secretos y sales distintos | `services/backend/app/auth.py:53-74` | El constructor se niega a arrancar si `pat_secret == session_secret`; cada serializador tiene su sal (`ttod-web-session-v1`, `ttod-api-pat-v1`) y su `typ`. |
| La sesión solo desde la cookie | `services/backend/app/auth.py:181-194` (`RequireSession`) | Lee el parámetro `Cookie`, nunca la cabecera `Authorization`. |
| El PAT solo desde la cabecera | `services/backend/app/auth.py:197-218` (`RequireAccessToken`) | Lee `Authorization: Bearer`, nunca una cookie. |
| Qué ruta pide qué | `services/backend/app/main.py:163-280` | Favoritos, propuestas, sesión y emisión del PAT piden sesión; solo `wisdom/random` pide PAT. |
| El frontend no ve la sesión | `services/frontend/src/pages/[locale]/login.astro` (cookie `httpOnly`) y `src/lib/auth.server.ts` | Astro reenvía la cookie al backend y no interpreta su contenido. |

## Por qué

- **Robo por XSS.** Con la opción 1 el token tenía que poder leerlo el JavaScript de la página
  para ponerlo en la cabecera. Un script inyectado se lo podía llevar y usarlo desde cualquier sitio
  y durante toda su vida. La cookie `httpOnly` de la opción 2 no la puede leer el JavaScript de la
  página.
- **CSRF.** Al revés: una cookie viaja sola, y por eso las rutas con sesión dependen de
  `SameSite=Lax` y de la comprobación de origen de Astro (los POST de otro origen reciben 403).
  Un PAT en la cabecera no viaja solo, así que la API pública no necesita esa defensa.
- **Dos vidas distintas.** Cada una tiene su propia caducidad (`TTOD_SESSION_TTL_SECONDS` y
  `TTOD_PAT_TTL_SECONDS`), y la sesión ahora se puede revocar al cerrar sesión. Un PAT lo guarda un
  script o una integración, y no tiene por qué morir cuando alguien cierra el navegador. Con una
  sola credencial, cerrar sesión en el navegador rompería también los scripts, o el script tendría
  una credencial capaz de abrir la biblioteca y la cola del revisor.
- **Una filtración no abre las dos puertas.** Un PAT copiado en un log de CI no sirve para entrar
  en la web, y una cookie robada no sirve contra la API pública. Lo comprueban los tests de rechazo
  de la tabla de abajo.

## Lo que cuesta

- **Más código:** dos dependencias, dos serializadores, dos secretos en `.env` y una ruta para
  emitir el PAT.
- **Más configuración:** quien despliega tiene que generar dos secretos y que sean distintos, y el
  backend no arranca si no lo son.
- **El PAT sigue sin revocación.** Es una firma con caducidad y no hay lista de PAT emitidos. La
  fase Z lo dejó aplazado de forma explícita (`PHASE-Z-COLD-REVIEW.md`, punto 5).

## La «fricción del cambio» (`arch-010`), comprobada después

La ficha pide justificar el límite por lo que habría costado cambiarlo. Hay dos cambios reales
posteriores que lo demuestran:

1. **Fase Z (27/10/2026, Rubén).** La sesión pasó de ser una firma a ser un identificador opaco
   guardado en Redis con TTL (`auth.py:121-138`, `sessions.py`). El PAT no se tocó:
   `issue_pat`/`read_pat` y los tests de la API pública siguen igual. Con la opción 1, mover «la
   sesión» a Redis habría cambiado también el contrato de los scripts que usan la API.
2. **Este PR: cerrar sesión.** `POST /{locale}/logout` llama a `POST /api/v1/auth/logout`, que borra
   la sesión de Redis. Un PAT emitido antes sigue funcionando hasta que caduca, que es lo que se
   quiere: cerrar sesión en el navegador no debe tumbar una integración. Con la opción 1 habría que
   haber elegido entre no revocar nada o revocarlo todo.

## Cómo comprobarlo

| Regla | Test |
| --- | --- |
| La cookie sola no vale en la API pública | `services/backend/tests/test_api.py::test_session_cookie_on_its_own_is_rejected`, `test_backend.py::test_random_wisdom_rejects_a_session_cookie_on_its_own` |
| La sesión mandada como Bearer no vale | `test_api.py::test_session_value_presented_as_bearer_is_rejected`, `test_backend.py::test_session_token_is_not_accepted_as_a_bearer_credential` |
| El PAT no es el valor de la sesión | `test_backend.py::test_token_endpoint_issues_a_pat_that_is_not_the_session_value` |
| Cerrar sesión revoca la sesión en el backend y borra la cookie | `services/frontend/src/tests/account-pages.test.ts` («logging out») |
| Si el backend no puede revocar, la cookie se conserva y se avisa | Mismo fichero, «keeps the cookie and says so…» |

## Qué cambiaría ahora

- **Revocar PAT:** guardar en Redis un identificador por PAT (`ttod:pat:{jti}`) para poder
  revocarlos sin cambiar el formato del Bearer. Encaja con la fase Z y no toca la sesión.
- **Quitar la compatibilidad con la sesión firmada** (`auth.py:137-138`), que solo usan los tests.
  Una cookie firmada no se puede revocar al cerrar sesión (hallazgo F7 de la revisión de la
  fase Z).
