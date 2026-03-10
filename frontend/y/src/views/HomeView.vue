<script setup>
import { ref } from 'vue';
import AvailabilityChecker from '../components/AvailabilityChecker.vue';
import ReservationForm from '../components/ReservationForm.vue';
import ClientCancellation from '../components/ClientCancellation.vue';

// Variables y lógica original mantenida intacta
const selectedTableId = ref(null);
const showCancellation = ref(false);

const handleTableSelected = (tableId) => {
  selectedTableId.value = tableId;
  showCancellation.value = false;
};

const handleReset = () => {
    selectedTableId.value = null;
};
</script>

<template>
  <div class="home-page-layout">
    <!-- HERO SECTION / HEADER -->
    <header class="hero-section" :class="{ 'hero-compact': selectedTableId || showCancellation }">
      <div class="hero-content">
        <div class="brand-logo">
          <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"></path><path d="M7 2v20"></path><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"></path></svg>
        </div>
        <h1 class="main-title">Gastronomía & Confort</h1>
        <p class="main-subtitle">Reserva tu lugar en nuestra mesa y vive una experiencia inolvidable.</p>
      </div>
    </header>

    <main class="content-container">
      
      <!-- ESTADO 1: BÚSQUEDA DE DISPONIBILIDAD -->
      <Transition name="page-fade" mode="out-in">
        <div v-if="!selectedTableId && !showCancellation" class="view-step">
          <AvailabilityChecker @select-table="handleTableSelected" />
          
          <div class="footer-actions">
            <div class="cancellation-card">
              <span class="card-text">¿Ya tienes una reservación con nosotros?</span>
              <button @click="showCancellation = true" class="btn-cancel-link">
                Gestionar o Cancelar Reservación
              </button>
            </div>
          </div>
        </div>
        
        <!-- ESTADO 2: PROCESO DE CANCELACIÓN -->
        <div v-else-if="showCancellation" class="view-step reservation-section">
          <div class="step-header">
            <button @click="showCancellation = false" class="btn-back">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
              Volver a disponibilidad
            </button>
          </div>
          <ClientCancellation />
        </div>

        <!-- ESTADO 3: FORMULARIO DE RESERVA (Mesa Seleccionada) -->
        <div v-else class="view-step reservation-section">
          <div class="step-header">
            <button @click="handleReset" class="btn-back">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
              Cambiar de mesa
            </button>
          </div>
          <ReservationForm :tableId="selectedTableId" @reset="handleReset" />
        </div>
      </Transition>

    </main>

    <!-- FOOTER DECORATIVO -->
    <footer class="app-footer">
      <p>&copy; 2024 GastroManager Pro • Sistema de Reservas</p>
    </footer>
  </div>
</template>

<style scoped>
/* Layout Base */
.home-page-layout {
  min-height: 100vh;
  background-color: #fcfcfd;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: #1e293b;
}

/* Hero Section Refinada */
.hero-section {
  padding: 5rem 1rem 4rem;
  background: linear-gradient(to bottom, #0f172a, #1e293b);
  color: white;
  text-align: center;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.hero-section::after {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0);
  background-size: 24px 24px;
}

.hero-compact {
  padding: 2rem 1rem;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.brand-logo {
  width: 64px;
  height: 64px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: #818cf8;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.main-title {
  font-size: 3rem;
  font-weight: 900;
  letter-spacing: -0.04em;
  margin: 0;
  line-height: 1.1;
}

.main-subtitle {
  font-size: 1.15rem;
  color: #94a3b8;
  margin: 1rem auto 0;
  max-width: 500px;
}

.hero-compact .main-title { font-size: 1.5rem; }
.hero-compact .main-subtitle, 
.hero-compact .brand-logo { display: none; }

/* Contenedor de Contenido */
.content-container {
  max-width: 1000px;
  margin: -3rem auto 4rem;
  padding: 0 1.5rem;
  position: relative;
  z-index: 10;
}

.view-step {
  width: 100%;
}

.reservation-section {
  max-width: 650px;
  margin: 0 auto;
}

/* Cabecera de Pasos */
.step-header {
  margin-bottom: 1.5rem;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  border: 1px solid #e2e8f0;
  color: #475569;
  padding: 0.6rem 1rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.btn-back:hover {
  background: #f8fafc;
  color: #0f172a;
  border-color: #cbd5e1;
  transform: translateX(-4px);
}

/* Footer de Acciones (Cancelación) */
.footer-actions {
  margin-top: 3rem;
  display: flex;
  justify-content: center;
}

.cancellation-card {
  text-align: center;
  padding: 2rem;
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: 20px;
  width: 100%;
  max-width: 500px;
}

.card-text {
  display: block;
  font-size: 0.95rem;
  color: #64748b;
  margin-bottom: 0.75rem;
}

.btn-cancel-link {
  background: none;
  border: none;
  color: #6366f1;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  text-decoration: none;
  border-bottom: 2px solid rgba(99, 102, 241, 0.2);
  padding-bottom: 2px;
  transition: all 0.2s;
}

.btn-cancel-link:hover {
  color: #4338ca;
  border-bottom-color: #4338ca;
}

.app-footer {
  text-align: center;
  padding: 2rem;
  color: #94a3b8;
  font-size: 0.85rem;
}

/* Transiciones de Página */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: all 0.3s ease;
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Mobile Adjustments */
@media (max-width: 640px) {
  .main-title { font-size: 2.25rem; }
  .hero-section { padding: 4rem 1rem 3rem; }
  .content-container { margin-top: -2rem; padding: 0 1rem; }
}
</style>