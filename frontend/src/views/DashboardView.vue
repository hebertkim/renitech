<template>
  <MainLayout>
    <div class="space-y-6">

      <!-- ========================= -->
      <!-- Cards de KPIs -->
      <!-- ========================= -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="bg-blue-500 text-white p-6 rounded-lg shadow hover:shadow-lg transition">
          <h3 class="text-sm font-semibold">Total de Produtos</h3>
          <p class="text-3xl font-bold mt-2">{{ dashboard.stats.total_products }}</p>
        </div>

        <div class="bg-red-500 text-white p-6 rounded-lg shadow hover:shadow-lg transition">
          <h3 class="text-sm font-semibold">Total de Pedidos</h3>
          <p class="text-3xl font-bold mt-2">{{ dashboard.stats.total_orders }}</p>
        </div>

        <div class="bg-purple-500 text-white p-6 rounded-lg shadow hover:shadow-lg transition">
          <h3 class="text-sm font-semibold">Total de Clientes</h3>
          <p class="text-3xl font-bold mt-2">{{ dashboard.stats.total_customers }}</p>
        </div>

        <div class="bg-yellow-500 text-white p-6 rounded-lg shadow hover:shadow-lg transition col-span-1 sm:col-span-2 lg:col-span-1">
          <h3 class="text-sm font-semibold">Produtos com Estoque Baixo</h3>
          <p class="text-3xl font-bold mt-2">{{ dashboard.stats.low_stock_products }}</p>
        </div>
      </div>

      <!-- ========================= -->
      <!-- Filtros -->
      <!-- ========================= -->
      <div class="bg-white p-4 rounded-lg shadow flex flex-wrap gap-4 items-center">
        <label>
          Mês:
          <select v-model="filter.month" class="border rounded p-1">
            <option v-for="m in 12" :key="m" :value="m">{{ m }}</option>
          </select>
        </label>
        <label>
          Ano:
          <select v-model="filter.year" class="border rounded p-1">
            <option v-for="y in [2023, 2024, 2025, 2026]" :key="y" :value="y">{{ y }}</option>
          </select>
        </label>
        <button @click="applyFilters" class="bg-indigo-500 text-white px-4 py-2 rounded shadow hover:bg-indigo-600 transition">
          Aplicar
        </button>
      </div>

      <!-- ========================= -->
      <!-- Gráficos -->
      <!-- ========================= -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

        <!-- Evolução Mensal -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-gray-700 mb-4">Evolução Mensal</h3>
          <canvas id="evolutionChart"></canvas>
        </div>

        <!-- Pedidos Pagos, Reservados e Cancelados -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-gray-700 mb-4">Status de Pedidos</h3>
          <canvas id="ordersChart"></canvas>
        </div>

        <!-- Clientes Novos x Recorrentes -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-gray-700 mb-4">Clientes Novos x Recorrentes</h3>
          <canvas id="clientsChart"></canvas>
        </div>

        <!-- Faturamento Bruto -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-gray-700 mb-4">Faturamento Bruto</h3>
          <canvas id="revenueChart"></canvas>
        </div>

        <!-- Faturamento por Loja -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-gray-700 mb-4">Faturamento por Loja</h3>
          <canvas id="storeChart"></canvas>
        </div>

        <!-- Faturamento por Marketplaces -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h3 class="text-lg font-semibold text-gray-700 mb-4">Faturamento por Marketplaces</h3>
          <canvas id="marketplaceChart"></canvas>
        </div>
      </div>

      <!-- ========================= -->
      <!-- Tabela de Produtos com Estoque Baixo -->
      <!-- ========================= -->
      <div class="bg-white p-6 rounded-lg shadow mt-6">
        <h3 class="text-lg font-semibold text-gray-700 mb-4">Produtos com Estoque Baixo</h3>
        <div v-if="loading" class="text-center text-gray-600">Carregando...</div>
        <table v-if="!loading" class="min-w-full table-auto">
          <thead>
            <tr>
              <th class="px-4 py-2 text-left text-gray-600">Produto</th>
              <th class="px-4 py-2 text-left text-gray-600">Quantidade em Estoque</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in dashboard.low_stock_products" :key="p.product_id">
              <td class="px-4 py-2">{{ p.product_name }}</td>
              <td class="px-4 py-2">{{ p.stock_quantity }}</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </MainLayout>
</template>

<script>
import MainLayout from "@/layouts/MainLayout.vue";
import axios from "axios";
import Chart from "chart.js/auto";

export default {
  name: "DashboardView",
  components: { MainLayout },
  data() {
    return {
      dashboard: {
        stats: {
          total_products: 0,
          total_orders: 0,
          total_customers: 0,
          low_stock_products: 0,
        },
        low_stock_products: [],
      },
      loading: true,
      filter: {
        month: new Date().getMonth() + 1,
        year: new Date().getFullYear(),
      },
    };
  },
  methods: {
    async fetchDashboard() {
      try {
        const res = await axios.get("/api/dashboard", { params: this.filter });
        this.dashboard = res.data;
        this.loadCharts();
      } catch (err) {
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    applyFilters() {
      this.loading = true;
      this.fetchDashboard();
    },

    loadCharts() {
      // Evolução Mensal
      new Chart(document.getElementById("evolutionChart"), {
        type: "line",
        data: {
          labels: ["Jan","Feb","Mar","Apr","May","Jun"],
          datasets: [{
            label: "Pedidos",
            data: [12, 19, 3, 5, 2, 3],
            borderColor: "#3B82F6",
            backgroundColor: "rgba(59, 130, 246, 0.2)",
            fill: true,
            tension: 0.2
          }]
        },
        options: { responsive: true }
      });

      // Pedidos Pagos, Reservados e Cancelados
      new Chart(document.getElementById("ordersChart"), {
        type: "bar",
        data: {
          labels: ["Pagos","Reservados","Cancelados"],
          datasets: [{
            label: "Quantidade",
            data: [50, 30, 10],
            backgroundColor: ["#10B981", "#F59E0B", "#EF4444"]
          }]
        },
        options: { responsive: true }
      });

      // Clientes Novos x Recorrentes
      new Chart(document.getElementById("clientsChart"), {
        type: "doughnut",
        data: {
          labels: ["Novos","Recorrentes"],
          datasets: [{
            data: [70,30],
            backgroundColor: ["#8B5CF6","#F43F5E"]
          }]
        },
        options: { responsive: true }
      });

      // Faturamento Bruto
      new Chart(document.getElementById("revenueChart"), {
        type: "line",
        data: {
          labels: ["Jan","Feb","Mar","Apr","May","Jun"],
          datasets: [{
            label: "Faturamento Bruto",
            data: [1200, 1500, 900, 2000, 1800, 2200],
            borderColor: "#F59E0B",
            backgroundColor: "rgba(245, 158, 11, 0.2)",
            fill: true,
            tension: 0.2
          }]
        },
        options: { responsive: true }
      });

      // Faturamento por Loja
      new Chart(document.getElementById("storeChart"), {
        type: "bar",
        data: {
          labels: ["Loja A","Loja B","Loja C"],
          datasets: [{
            label: "Faturamento",
            data: [1000,1500,1200],
            backgroundColor: ["#3B82F6","#10B981","#F59E0B"]
          }]
        },
        options: { responsive: true }
      });

      // Faturamento por Marketplaces
      new Chart(document.getElementById("marketplaceChart"), {
        type: "bar",
        data: {
          labels: ["Amazon","Mercado Livre","Shopee"],
          datasets: [{
            label: "Faturamento",
            data: [2000,1500,1800],
            backgroundColor: ["#FF9900","#FFE600","#FF5722"]
          }]
        },
        options: { responsive: true }
      });
    }
  },
  mounted() {
    this.fetchDashboard();
  }
};
</script>

<style scoped>
/* Cards vibrantes */
.bg-blue-500 { background-color: #3B82F6; }
.bg-green-500 { background-color: #10B981; }
.bg-red-500 { background-color: #EF4444; }
.bg-purple-500 { background-color: #8B5CF6; }
.bg-yellow-500 { background-color: #F59E0B; }
</style>
