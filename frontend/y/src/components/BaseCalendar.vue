<template>
  <div class="custom-calendar">
    <header class="calendar-header">
      <div class="nav-controls">
        <button type="button" @click="changeMonth(-1)" class="nav-btn">‹</button>
        <div class="month-year-display">
          <span class="month-name">{{ monthNames[currentMonth] }}</span>
          <span class="year-val">{{ currentYear }}</span>
        </div>
        <button type="button" @click="changeMonth(1)" class="nav-btn">›</button>
      </div>
    </header>

    <div class="calendar-grid">
      <div v-for="day in weekDays" :key="day" class="weekday-label">{{ day }}</div>
      
      <!-- Empty slots for previous month padding -->
      <div v-for="p in paddingDays" :key="'p'+p" class="day-cell padding"></div>
      
      <!-- Days of the month -->
      <button 
        v-for="date in daysInMonth" 
        :key="date" 
        type="button"
        class="day-cell date-btn"
        :class="{ 
          'selected': isSelected(date), 
          'today': isToday(date),
          'disabled': isPast(date)
        }"
        :disabled="isPast(date)"
        @click="selectDate(date)"
      >
        {{ date }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update:modelValue']);

const todayDate = new Date();
todayDate.setHours(0,0,0,0);

const currentMonth = ref(todayDate.getMonth());
const currentYear = ref(todayDate.getFullYear());

const monthNames = [
  "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
];

const weekDays = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"];

// Compute days in the current month
const daysInMonth = computed(() => {
  return new Date(currentYear.value, currentMonth.value + 1, 0).getDate();
});

// Compute padding days (starting on Monday)
const paddingDays = computed(() => {
  const firstDay = new Date(currentYear.value, currentMonth.value, 1).getDay();
  // day 0 is Sunday, we want 0 for Monday.
  return firstDay === 0 ? 6 : firstDay - 1;
});

const changeMonth = (delta) => {
  currentMonth.value += delta;
  if (currentMonth.value > 11) {
    currentMonth.value = 0;
    currentYear.value++;
  } else if (currentMonth.value < 0) {
    currentMonth.value = 11;
    currentYear.value--;
  }
};

const selectDate = (date) => {
  const d = new Date(currentYear.value, currentMonth.value, date);
  // Format as YYYY-MM-DD local
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  emit('update:modelValue', `${year}-${month}-${day}`);
};

const isSelected = (date) => {
  if (!props.modelValue) return false;
  const parts = props.modelValue.split('-');
  return parseInt(parts[0]) === currentYear.value && 
         parseInt(parts[1]) === currentMonth.value + 1 && 
         parseInt(parts[2]) === date;
};

const isToday = (date) => {
  const d = new Date();
  return d.getDate() === date && d.getMonth() === currentMonth.value && d.getFullYear() === currentYear.value;
};

const isPast = (date) => {
  const d = new Date(currentYear.value, currentMonth.value, date);
  return d < todayDate;
};

// Auto-initialize if modelValue is set
onMounted(() => {
  if (props.modelValue) {
    const parts = props.modelValue.split('-');
    currentYear.value = parseInt(parts[0]);
    currentMonth.value = parseInt(parts[1]) - 1;
  }
});
</script>

<style scoped>
.custom-calendar {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 0.75rem;
  user-select: none;
}

.calendar-header {
  margin-bottom: 0.75rem;
}

.nav-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.month-year-display {
  font-weight: 700;
  color: #1e293b;
  display: flex;
  gap: 0.4rem;
}

.month-name { font-size: 0.85rem; }
.year-val { color: #6366f1; font-size: 0.85rem; }

.nav-btn {
  background: #f1f5f9;
  border: none;
  width: 26px;
  height: 26px;
  border-radius: 6px;
  cursor: pointer;
  color: #475569;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.nav-btn:hover { background: #e2e8f0; color: #1e293b; }

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
}

.weekday-label {
  text-align: center;
  font-size: 0.6rem;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
  padding: 0.4rem 0;
}

.day-cell {
  aspect-ratio: 1/1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 8px;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: all 0.2s;
}

.date-btn:hover:not(.disabled) {
  background: #f1f5f9;
  color: #6366f1;
}

.date-btn.selected {
  background: #6366f1 !important;
  color: white !important;
  box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
}

.date-btn.today {
  color: #6366f1;
  text-decoration: underline;
  text-underline-offset: 4px;
}

.date-btn.disabled {
  color: #cbd5e1;
  cursor: not-allowed;
  font-weight: 400;
}

.padding {
  cursor: default;
}
</style>
