<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold">Despesas</h1>

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
        <option
          v-for="cat in categories"
          :key="cat.id"
          :value="cat.id"
        >
          {{ cat.name }}
        </option>
      </select>
      <button
        @click="fetchExpenses"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
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
          <tr
            v-for="expense in expenses"
            :key="expense.id"
            class="border-t"
          >
            <td class="px-4 py-2">{{ expense.description }}</td>
            <td class="px-4 py-2 text-right">R$ {{ expense.amount.toFixed(2) }}</td>
            <td class="px-4 py-2">{{ expense.category?.name || '-' }}</td>
            <td class="px-4 py-2">{{ formatDate(expense.date) }}</td>
            <td class="px-4 py-2 text-center space-x-2">
              <button
                @click="editExpense(expense.id)"
                class="text-blue-500 hover:underline"
              >
                Editar
              </button>
              <button
                @click="deleteExpense(expense.id)"
                class="text-red-500 hover:underline"
              >
                Excluir
              </button>
            </td>
          </tr>
          <tr v-if="expenses.length === 0">
            <td colspan="5" class="text-center py-4">Nenhuma despesa encontrada.</td>
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
        :disabled="expenses.length < limit"
        class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
      >
        Próxima
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useExpenseStore } from '@/stores/expense'   // ← seu store corrigido
import { useCategoriesStore } from '@/stores/categories'
import { useRouter } from 'vue-router'

const router = useRouter()
const expensesStore = useExpenseStore()
const categoriesStore = useCategoriesStore()

const expenses = ref([])
const categories = ref([])
const limit = 10
const offset = ref(0)
const filters = ref({
  text: '',
  date_from: '',
  date_to: '',
  category_id: ''
})

const currentPage = ref(1)

const fetchExpenses = async () => {
  const params = {
    limit,
    offset: offset.value,
    text: filters.value.text || undefined,
    date_from: filters.value.date_from || undefined,
    date_to: filters.value.date_to || undefined,
    category_id: filters.value.category_id || undefined
  }
  expenses.value = await expensesStore.fetchExpenses(params) // ← corrigido
}

const fetchCategories = async () => {
  categories.value = await categoriesStore.fetchAll()
}

const resetFilters = () => {
  filters.value = { text: '', date_from: '', date_to: '', category_id: '' }
  offset.value = 0
  currentPage.value = 1
  fetchExpenses()
}

const editExpense = (id) => {
  router.push(`/expenses/${id}/edit`)
}

const deleteExpense = async (id) => {
  if (confirm('Deseja realmente excluir esta despesa?')) {
    await expensesStore.removeExpense(id)  // ← corrigido
    fetchExpenses()
  }
}

const prevPage = () => {
  if (offset.value >= limit) {
    offset.value -= limit
    currentPage.value--
    fetchExpenses()
  }
}

const nextPage = () => {
  offset.value += limit
  currentPage.value++
  fetchExpenses()
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('pt-BR')
}

onMounted(() => {
  fetchCategories()
  fetchExpenses()
})
</script>

<style scoped>
/* ajustes visuais se necessário */
</style>
