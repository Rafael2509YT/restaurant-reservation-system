<script setup>
import AdminDashboard from '../components/AdminDashboard.vue';
</script>

<template>
  <div class="admin-page">
    <!-- Navegación de Acceso Rápido -->
    <nav class="admin-sticky-nav">
      <div class="nav-inner">
        <div class="admin-brand">
          <span class="badge">Admin</span>
          <span class="divider">/</span>
          <span class="current">Dashboard Operativo</span>
        </div>
        <div class="nav-anchors">
          <a href="#config">Ajustes</a>
          <a href="#tables">Mesas</a>
          <a href="#calendar">Calendario</a>
        </div>
      </div>
    </nav>

    <main class="admin-content-flow">
      <AdminDashboard />
    </main>
  </div>
</template>

<style scoped>
.admin-page {
  background-color: #f1f5f9;
  min-height: 100vh;
}

.admin-sticky-nav {
  position: sticky;
  top: 72px; /* Debajo del navbar principal de App.vue */
  z-index: 50;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid #e2e8f0;
  padding: 0.75rem 1rem;
}

@media (max-width: 1024px) {
  .admin-sticky-nav {
    top: 60px; /* Ajuste para el navbar en móviles si cambia de altura */
    padding: 0.5rem 1rem;
  }
}

.nav-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.admin-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
}

.badge {
  background: #0f172a;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.divider { color: #cbd5e1; }
.current { color: #64748b; }

.nav-anchors {
  display: flex;
  gap: 1.5rem;
}

.nav-anchors a {
  text-decoration: none;
  color: #64748b;
  font-size: 0.85rem;
  font-weight: 600;
  transition: color 0.2s;
}

.nav-anchors a:hover {
  color: #6366f1;
}

  padding: 1.5rem 1rem;
}

@media (max-width: 768px) {
  .nav-anchors { display: none; }
}
</style>