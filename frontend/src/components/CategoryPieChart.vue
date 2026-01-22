<template>
  <div class="bg-white shadow rounded-lg p-5">
    <h2 class="text-sm font-medium text-gray-500 mb-3">{{ title }}</h2>
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from "vue";
import { Chart, registerables } from "chart.js";

// Registrar todos os componentes do Chart.js
Chart.register(...registerables);

// Props do componente
const props = defineProps({
  title: { type: String, default: "Categorias" },
  categories: { type: Array, default: () => [] }, // [{ name, total }]
  colors: { 
    type: Array, 
    default: () => ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"] 
  }
});

const canvas = ref(null);
let chart = null;

// Função para criar/atualizar o gráfico
const updateChart = () => {
  if (!canvas.value) return;

  const data = props.categories.map(c => c.total);
  const labels = props.categories.map(c => c.name);

  if (!chart) {
    chart = new Chart(canvas.value, {
      type: "pie",
      data: { 
        labels, 
        datasets: [{ data, backgroundColor: props.colors }] 
      },
      options: { 
        responsive: true,
        plugins: {
          legend: { position: 'bottom' },
          tooltip: { enabled: true }
        },
        animation: {
          animateScale: true,
          animateRotate: true
        }
      }
    });
  } else {
    chart.data.labels = labels;
    chart.data.datasets[0].data = data;
    chart.update();
  }
};

// Inicializa o gráfico ao montar o componente
onMounted(updateChart);

// Atualiza o gráfico sempre que categories mudarem
watch(() => props.categories, updateChart, { deep: true });

// Destrói o gráfico ao desmontar o componente para liberar memória
onBeforeUnmount(() => {
  if (chart) {
    chart.destroy();
    chart = null;
  }
});
</script>

<style scoped>
/* Nenhuma alteração visual necessária, TailwindCSS já estiliza o container */
</style>
