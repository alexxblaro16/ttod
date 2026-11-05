import { entintar } from './letras';

/** Comportamiento común de las páginas de entrar y de crear cuenta. */
export function prepararAcceso(): void {
  // El título se entinta letra a letra, como en el oráculo (kit de estilo).
  entintar(document.querySelector('.acceso h1'), { retraso: .15 });

  const form = document.querySelector<HTMLFormElement>('.acceso-form');
  const ver = form?.querySelector<HTMLButtonElement>('.ver-clave');
  const clave = form?.querySelector<HTMLInputElement>('#password');

  if (ver && clave) {
    // Sin JS el botón no existe: no promete lo que no puede hacer.
    ver.hidden = false;
    ver.addEventListener('click', () => {
      const visible = clave.type === 'password';
      clave.type = visible ? 'text' : 'password';
      ver.setAttribute('aria-pressed', String(visible));
      ver.textContent = visible ? ver.dataset.hide! : ver.dataset.show!;
      clave.focus();
    });
  }

  form?.addEventListener('submit', (ev) => {
    const boton = form.querySelector<HTMLButtonElement>('.acceso-entrar');
    if (!boton) return;
    // Un segundo toque no manda el formulario dos veces.
    if (boton.getAttribute('aria-disabled') === 'true') { ev.preventDefault(); return; }
    if (clave) clave.type = 'password';
    boton.setAttribute('aria-disabled', 'true');
    boton.textContent = boton.dataset.busy!;
  });
}
