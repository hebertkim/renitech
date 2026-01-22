<!-- src/components/ChartCard.vue -->
<template>
  <div class="bg-white shadow rounded-lg p-5">
    <h2 class="text-sm font-medium text-gray-500">{{ title }}</h2>
    <div class="mt-3">
      <canvas ref="canvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

const props = defineProps({
  title: String,
  labels: Array,
  data: Array,
  type: { type: String, default: "bar" },
  colors: { type: Array, default: () => ["#3B82F6", "#10B981", "#F59E0B"] }
});

const canvas = ref(null);
let chart = null;

onMounted(() => {
  chart = new Chart(canvas.value, {
    type: props.type,
    data: {
      labels: props.labels,
      datasets: [{
        label: props.title,
        data: props.data,
        backgroundColor: props.colors
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
});

watch(() => props.data, (newData) => {
  if (chart) {
    chart.data.datasets[0].data = newData;
    chart.update();
  }
});
</script>
