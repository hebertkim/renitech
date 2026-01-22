<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold">Receitas</h1>

    <!-- Filtros -->
    <div class="flex flex-wrap gap-4 items-end">
      <input
        v-model="filters.text"
        type="text"
        placeholder="Buscar descrição..."
        class="border rounded px-3 py-2"
      />
      <input
        v-model="filters.date_from"
        type="date"
        class="border rounded px-3 py-2"
      />
      <input
        v-model="filters.date_to"
        type="date"
        class="border rounded px-3 py-2"
      />
      <select v-model="filters.category_id" class="border rounded px-3 py-2">
        <option value="">Todas categorias</option>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
          {{ cat.name }}
        </option>
      </select>
      <button
        @click="fetchIncomes"
        class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
      >
        Filtrar
      </button>
      <button
        @click="resetFilters"
        class="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400"
      >
        Limpar
      </button>
    </div>

    <!-- Tabela -->
    <div class="overflow-x-auto">
      <table class="min-w-full border">
        <thead class="bg-gray-100">
          <tr>
            <th class="px-4 py-2 text-left">Descrição</th>
            <th class="px-4 py-2 text-right">Valor</th>
            <th class="px-4 py-2 text-left">Categoria</th>
            <th class="px-4 py-2 text-left">Data</th>
            <th class="px-4 py-2 text-center">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="income in incomes" :key="income.id" class="border-t">
            <td class="px-4 py-2">{{ income.description }}</td>
            <td class="px-4 py-2 text-right">
              {{ formatCurrency(income.amount) }}
            </td>
            <td class="px-4 py-2">{{ income.category?.name || '-' }}</td>
            <td class="px-4 py-2">{{ formatDate(income.date) }}</td>
            <td class="px-4 py-2 text-center space-x-2">
              <button
                @click="editIncome(income.id)"
                class="text-blue-500 hover:underline"
              >
                Editar
              </button>
              <button
                @click="deleteIncome(income.id)"
                class="text-red-500 hover:underline"
              >
                Excluir
              </button>
            </td>
          </tr>
          <tr v-if="incomes.length === 0">
            <td colspan="5" class="text-center py-4">
              Nenhuma receita encontrada.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Paginação -->
    <div class="flex justify-between items-center mt-4">
      <button
        @click="prevPage"
        :disabled="offset === 0"
        class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
      >
        Anterior
      </button>
      <span>Página {{ currentPage }}</span>
      <button
        @click="nextPage"
        :disabled="incomes.length < limit"
        class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
      >
        Próxima
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useIncomeStore } from "@/stores/income";
import { useCategoriesStore } from "@/stores/categories";
import { useRouter } from "vue-router";

const router = useRouter();
const incomeStore = useIncomeStore();
const categoriesStore = useCategoriesStore();

const incomes = ref([]);
const categories = ref([]);
const limit = 10;
const offset = ref(0);
const currentPage = ref(1);

const filters = ref({
  text: "",
  date_from: "",
  date_to: "",
  category_id: ""
});

// ========================
// FUNÇÕES
// ========================
const fetchIncomes = async () => {
  const params = {
    limit,
    offset: offset.value,
    text: filters.value.text || undefined,
    date_from: filters.value.date_from || undefined,
    date_to: filters.value.date_to || undefined,
    category_id: filters.value.category_id || undefined
  };
  incomes.value = await incomeStore.fetchAll(params);
};

const fetchCategories = async () => {
  categories.value = await categoriesStore.fetchAll();
};

const resetFilters = () => {
  filters.value = { text: "", date_from: "", date_to: "", category_id: "" };
  offset.value = 0;
  currentPage.value = 1;
  fetchIncomes();
};

const editIncome = (id) => {
  router.push(`/incomes/${id}/edit`);
};

const deleteIncome = async (id) => {
  if (confirm("Deseja realmente excluir esta receita?")) {
    await incomeStore.deleteIncome(id);
    fetchIncomes();
  }
};

const prevPage = () => {
  if (offset.value >= limit) {
    offset.value -= limit;
    currentPage.value--;
    fetchIncomes();
  }
};

const nextPage = () => {
  offset.value += limit;
  currentPage.value++;
  fetchIncomes();
};

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString("pt-BR");
};

const formatCurrency = (value) => {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL"
  }).format(value);
};

// ========================
// MOUNTED
// ========================
onMounted(() => {
  fetchCategories();
  fetchIncomes();
});
</script>

<style scoped>
/* ajustes visuais se necessário */
</style>
