import type { AstroGlobal } from 'astro';

// Interfaz para definir la estructura del usuario autenticado
export interface AuthUser {
  id: string;
  email: string;
  role: 'admin' | 'user';
}

const SESSION_COOKIE_NAME = 'session';
const SEEDED_SESSION_TOKEN = 'seeded-user-token';

/**
 * Obtiene y valida el usuario actual desde la cookie de sesión httpOnly en el servidor.
 * NUNCA debe leerse desde localStorage para proteger rutas SSR.
 */
export async function getSessionUser(cookies: AstroGlobal['cookies']): Promise<AuthUser | null> {
  const token = cookies.get(SESSION_COOKIE_NAME)?.value;

  if (!token) {
    return null;
  }

  try {
    // No se acepta un prefijo como prueba de autenticación: cualquier cadena podría falsificarlo.
    if (token !== SEEDED_SESSION_TOKEN) {
      return null;
    }

    return {
      id: 'usr-001',
      email: 'admin@ttod.local',
      role: 'admin'
    };
  } catch (error) {
    console.error('Error validando la sesión SSR:', error);
    return null;
  }
}

/**
 * Guarda SSR (Server-Side Rendering) obligatoria para rutas protegidas.
 * Si no hay usuario autenticado, redirige inmediatamente al login y corta la renderización.
 */
export async function requireUser(astro: AstroGlobal): Promise<AuthUser | Response> {
  const user = await getSessionUser(astro.cookies);

  if (!user) {
    // Redirección SSR estricta: un curl o cliente sin sesión recibe la redirección y cero HTML protegido
    return astro.redirect('/es/login');
  }

  return user;
}

/**
 * Guarda basada en roles (ej. asegurar que el usuario es admin).
 */
export async function requireRole(astro: AstroGlobal, requiredRole: 'admin' | 'user'): Promise<AuthUser | Response> {
  const user = await requireUser(astro);

  // Si requireUser devolvió una Response (redirección), la propagamos
  if (user instanceof Response) {
    return user;
  }

  if (user.role !== requiredRole) {
    return astro.redirect('/es/unauthorized');
  }

  return user;
}