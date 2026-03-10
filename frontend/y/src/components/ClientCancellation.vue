<template>
  <div class="cancel-container">
    <div class="cancel-card">
      <!-- CABECERA -->
      <header class="card-header">
        <div class="icon-box">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><line x1="17" y1="8" x2="22" y2="13"></line><line x1="22" y1="8" x2="17" y2="13"></line></svg>
        </div>
        <div class="header-text">
          <h2>Gestión de Reservación</h2>
          <p>Cancela tu mesa de forma segura</p>
        </div>
      </header>

      <!-- VISTA DE ÉXITO -->
      <transition name="fade">
        <div v-if="success" class="state-view success-view">
          <div class="success-illustration">
            <div class="check-circle">
              <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
            </div>
          </div>
          <h3>Cancelación Exitosa</h3>
          <p>Tu reservación ha sido liberada. Hemos actualizado nuestro sistema y la mesa ya está disponible para otros clientes.</p>
          <button @click="resetForm" class="btn-outline">Entendido</button>
        </div>

        <!-- FORMULARIO -->
        <div v-else class="state-view">
          <div class="warning-box">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
            <span>Esta acción no se puede deshacer. Tu mesa será liberada inmediatamente.</span>
          </div>

          <form @submit.prevent="submitCancel" class="cancel-form">
            <div class="form-group">
              <label for="resId">ID de la Reservación</label>
              <div class="input-relative">
                <input 
                  type="number" 
                  id="resId" 
                  v-model="form.id" 
                  required 
                  placeholder="Ej: 12345"
                  class="custom-input"
                />
              </div>
              <small class="input-hint">El número que aparece en tu correo de confirmación.</small>
            </div>

            <div class="form-group">
              <label for="code">Código de Cancelación</label>
              <div class="input-relative">
                <input 
                  type="text" 
                  id="code" 
                  v-model="form.code" 
                  required 
                  placeholder="Ingresa el código único"
                  class="custom-input code-font"
                />
              </div>
              <small class="input-hint">Código de seguridad de 36 caracteres.</small>
            </div>

            <div v-if="error" class="error-banner">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
              <span>{{ error }}</span>
            </div>

            <button type="submit" :disabled="loading" class="btn-danger">
              <span v-if="!loading">Anular Reservación</span>
              <span v-else class="btn-loader"></span>
            </button>
          </form>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useReservationStore } from '../stores/reservationStore';

const store = useReservationStore();
const success = ref(false);
const loading = ref(false);
const error = ref(null);

const form = ref({
  id: '',
  code: ''
});

const submitCancel = async () => {
    loading.value = true;
    error.value = null;
    try {
        await store.cancelReservation(form.value.id, form.value.code);
        success.value = true;
    } catch (e) {
        error.value = e.response?.data?.error || e.message || "Error al procesar la cancelación";
    } finally {
        loading.value = false;
    }
};

const resetForm = () => {
    success.value = false;
    form.value.id = '';
    form.value.code = '';
    error.value = null;
};
</script>

<style scoped>
/* Contenedor Principal con fondo suave */
.cancel-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem 1rem;
  min-height: 400px;
}

/* Tarjeta Estilo Neumórfico Suave */
.cancel-card {
  width: 100%;
  max-width: 480px;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
  border: 1px solid #f1f5f9;
  overflow: hidden;
  font-family: 'Inter', system-ui, sans-serif;
}

/* Cabecera */
.card-header {
  padding: 2rem;
  background: #fffcfc;
  border-bottom: 1px solid #fff1f1;
  display: flex;
  gap: 1.25rem;
  align-items: center;
}

.icon-box {
  width: 48px;
  height: 48px;
  background: #fff1f1;
  color: #e11d48;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-text h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 800;
  color: #1e293b;
}

.header-text p {
  margin: 0;
  font-size: 0.875rem;
  color: #64748b;
}

/* Vistas de Estado */
.state-view {
  padding: 2rem;
}

/* Advertencia */
.warning-box {
  background: #fffbeb;
  border: 1px solid #fef3c7;
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  gap: 0.75rem;
  margin-bottom: 2rem;
  color: #92400e;
  font-size: 0.875rem;
  line-height: 1.4;
}

/* Formulario e Inputs */
.cancel-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
}

.custom-input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.2s;
  background: #f8fafc;
}

.custom-input:focus {
  outline: none;
  border-color: #f43f5e;
  background: white;
  box-shadow: 0 0 0 4px rgba(244, 63, 94, 0.1);
}

.code-font {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.9rem;
  letter-spacing: 0.05em;
}

.input-hint {
  font-size: 0.75rem;
  color: #94a3b8;
}

/* Botones */
.btn-danger {
  width: 100%;
  padding: 1rem;
  background: #e11d48;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1rem;
}

.btn-danger:hover:not(:disabled) {
  background: #be123c;
  transform: translateY(-1px);
  box-shadow: 0 10px 15px -3px rgba(225, 29, 72, 0.3);
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-outline {
  width: 100%;
  padding: 0.875rem;
  background: white;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

/* Vista de Éxito */
.success-view {
  text-align: center;
  padding: 3rem 2rem;
}

.success-illustration {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.check-circle {
  width: 80px;
  height: 80px;
  background: #f0fdf4;
  color: #22c55e;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4px solid #dcfce7;
}

.success-view h3 {
  font-size: 1.5rem;
  color: #0f172a;
  margin-bottom: 0.75rem;
}

.success-view p {
  color: #64748b;
  margin-bottom: 2rem;
  line-height: 1.6;
}

/* Error Banner */
.error-banner {
  background: #fff1f2;
  border: 1px solid #fecdd3;
  color: #be123c;
  padding: 0.875rem;
  border-radius: 10px;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
}

/* Loader */
.btn-loader {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
  40%, 60% { transform: translate3d(4px, 0, 0); }
}

/* Transiciones */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 480px) {
  .cancel-card { border-radius: 0; box-shadow: none; border: none; }
  .cancel-container { padding: 0; }
}
</style>