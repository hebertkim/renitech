<!-- src/views/DashboardView.vue -->
<template>
  <MainLayout>
    <div class="space-y-8">
      <h1 class="text-2xl font-semibold text-gray-900">Dashboard</h1>

      <!-- KPI Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="bg-white shadow rounded-lg p-5">
          <h2 class="text-sm font-medium text-gray-500">Total Despesas</h2>
          <p class="mt-1 text-2xl font-semibold text-gray-900">
            R$ {{ totalExpenses.toFixed(2) }}
          </p>
        </div>
        <div class="bg-white shadow rounded-lg p-5">
          <h2 class="text-sm font-medium text-gray-500">Total Receitas</h2>
          <p class="mt-1 text-2xl font-semibold text-gray-900">
            R$ {{ totalIncomes.toFixed(2) }}
          </p>
        </div>
        <div class="bg-white shadow rounded-lg p-5">
          <h2 class="text-sm font-medium text-gray-500">Saldo</h2>
          <p class="mt-1 text-2xl font-semibold text-gray-900">
            R$ {{ balance.toFixed(2) }}
          </p>
        </div>
        <div class="bg-white shadow rounded-lg p-5">
          <h2 class="text-sm font-medium text-gray-500">Contas</h2>
          <p class="mt-1 text-2xl font-semibold text-gray-900">
            {{ accounts.length }}
          </p>
        </div>
      </div>

      <!-- Filtros de período -->
      <div class="bg-white shadow rounded-lg p-5 flex flex-wrap gap-4 items-end">
        <div>
          <label class="block text-sm font-medium text-gray-700">Data Inicial</label>
          <input type="date" v-model="dateFrom" class="border px-3 py-2 rounded"/>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Data Final</label>
          <input type="date" v-model="dateTo" class="border px-3 py-2 rounded"/>
        </div>
        <button @click="applyFilters" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Aplicar Filtros</button>
        <button @click="resetFilters" class="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400">Limpar Filtros</button>
      </div>

      <!-- Gráficos -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <ChartCard
          title="Receitas x Despesas x Saldo"
          :labels="['Receitas', 'Despesas', 'Saldo']"
          :data="[totalIncomes, totalExpenses, balance]"
          type="bar"
        />
        <CategoryPieChart
          title="Despesas por Categoria"
          :categories="expenseByCategory"
        />
        <CategoryPieChart
          title="Receitas por Categoria"
          :categories="incomeByCategory"
        />
      </div>

      <!-- Top Categorias -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        <ChartCard
          title="Top Categorias de Despesa"
          :labels="topExpenseCategories.map(c => c.category_name)"
          :data="topExpenseCategories.map(c => c.total)"
          type="bar"
        />
        <ChartCard
          title="Top Categorias de Receita"
          :labels="topIncomeCategories.map(c => c.category_name)"
          :data="topIncomeCategories.map(c => c.total)"
          type="bar"
        />
      </div>

      <!-- Anomalias / Alertas -->
      <div class="bg-white shadow rounded-lg p-5 mt-6">
        <h2 class="text-lg font-semibold text-gray-700 mb-3">Anomalias Detectadas</h2>
        <ul>
          <li v-for="a in anomalies" :key="a.id" class="border-b py-2">
            <span class="font-medium">{{ a.type }}:</span> {{ a.description }} -
            R$ {{ a.amount }} em {{ a.date }}
          </li>
        </ul>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import MainLayout from "@/layouts/MainLayout.vue";
import ChartCard from "@/components/ChartCard.vue";
import CategoryPieChart from "@/components/CategoryPieChart.vue";
import DashboardService from "@/services/dashboard";

// ========================
// Filtros
// ========================
const dateFrom = ref('');
const dateTo = ref('');

// ========================
// Dados
// ========================
const dashboardSummary = ref(null);
const accounts = ref([]);
const topExpenseCategories = ref([]);
const topIncomeCategories = ref([]);
const anomalies = ref([]);

// ========================
// KPIs Computed
// ========================
const totalExpenses = computed(() => dashboardSummary.value?.total_expense || 0);
const totalIncomes = computed(() => dashboardSummary.value?.total_income || 0);
const balance = computed(() => dashboardSummary.value?.balance || 0);

const expenseByCategory = computed(() => dashboardSummary.value?.expenses_by_category || []);
const incomeByCategory = computed(() => dashboardSummary.value?.incomes_by_category || []);

// ========================
// Funções
// ========================
const fetchDashboard = async () => {
  dashboardSummary.value = await DashboardService.getSummary();
};

const fetchAccounts = async () => {
  accounts.value = await DashboardService.getByAccount();
};

const fetchTopCategories = async () => {
  [topExpenseCategories.value, topIncomeCategories.value] = await Promise.all([
    DashboardService.getTopExpenseCategories(),
    DashboardService.getTopIncomeCategories()
  ]);
};

const fetchAnomalies = async () => {
  anomalies.value = await DashboardService.getAnomalies();
};

// ========================
// Filtros
// ========================
const applyFilters = async () => {
  const month = dateFrom.value ? new Date(dateFrom.value).getMonth() + 1 : null;
  const year = dateFrom.value ? new Date(dateFrom.value).getFullYear() : null;
  dashboardSummary.value = await DashboardService.getSummary(month, year);
};

const resetFilters = async () => {
  dateFrom.value = '';
  dateTo.value = '';
  await fetchDashboard();
};

// ========================
// Init
// ========================
onMounted(async () => {
  await Promise.all([
    fetchDashboard(),
    fetchAccounts(),
    fetchTopCategories(),
    fetchAnomalies()
  ]);
});
</script>
