<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app-shell">
    <!-- HEADER GLOBAL PREMIUM -->
    <header class="navbar">
      <div class="navbar-container">
        <!-- Logo / Marca -->
        <div class="navbar-brand">
          <div class="brand-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"></path><path d="M7 2v20"></path><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"></path></svg>
          </div>
          <span class="brand-text">GastroReserve<span class="dot">.</span></span>
        </div>

        <!-- Navegación Principal -->
        <nav class="nav-menu">
          <RouterLink to="/" class="nav-link">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="nav-icon"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
            <span>Reservar Mesa</span>
          </RouterLink>
          
          <RouterLink to="/admin" class="nav-link">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="nav-icon"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
            <span>Administración</span>
          </RouterLink>
        </nav>

        <!-- Acción Rápida (Decorativa) -->
        <div class="navbar-actions">
          <button class="btn-support">Soporte</button>
        </div>
      </div>
    </header>

    <!-- ÁREA DE CONTENIDO DINÁMICO -->
    <main class="main-viewport">
      <RouterView v-slot="{ Component }">
        <transition name="route-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>
  </div>
</template>

<style>
/* Estilos Globales del Sistema */
:root {
  --primary: #6366f1;
  --primary-hover: #4f46e5;
  --bg-app: #f8fafc;
  --text-main: #0f172a;
  --text-muted: #64748b;
  --navbar-height: 72px;
}

body {
  margin: 0;
  padding: 0;
  background-color: var(--bg-app);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
}

/* Shell del App */
.app-shell {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Navbar con efecto Glassmorphism */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--navbar-height);
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.8);
  z-index: 1000;
}

.navbar-container {
  max-width: 1400px;
  height: 100%;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Brand/Logo */
.navbar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.brand-icon {
  width: 34px;
  height: 34px;
  background: var(--primary);
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
}

.brand-text {
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.02em;
}

.brand-text .dot {
  color: var(--primary);
}

/* Navegación */
.nav-menu {
  display: flex;
  gap: 0.5rem;
  background: #f1f5f9;
  padding: 0.4rem;
  border-radius: 12px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.5rem 1.25rem;
  text-decoration: none;
  color: var(--text-muted);
  font-size: 0.9rem;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: var(--text-main);
  background: rgba(255, 255, 255, 0.5);
}

.nav-link.router-link-exact-active {
  background: white;
  color: var(--primary);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.nav-icon {
  opacity: 0.7;
}

.router-link-exact-active .nav-icon {
  opacity: 1;
}

/* Acciones */
.btn-support {
  background: transparent;
  border: 1px solid #e2e8f0;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-support:hover {
  border-color: var(--primary);
  color: var(--primary);
}

/* Main Viewport */
.main-viewport {
  margin-top: var(--navbar-height);
  flex-grow: 1;
}

/* Transiciones de Rutas */
.route-fade-enter-active,
.route-fade-leave-active {
  transition: all 0.3s ease;
}

.route-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.route-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Responsive */
@media (max-width: 768px) {
  .navbar-container {
    padding: 0 1rem;
  }
  .brand-text, .navbar-actions, .nav-link span {
    display: none;
  }
  .nav-menu {
    gap: 0.25rem;
  }
  .nav-link {
    padding: 0.6rem;
  }
}
</style>