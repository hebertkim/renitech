<template>
  <div class="p-6 space-y-6 max-w-lg mx-auto">
    <h1 class="text-2xl font-bold">
      {{ isEditMode ? "Editar Despesa" : "Nova Despesa" }}
    </h1>

    <form @submit.prevent="handleSubmit" class="space-y-4">

      <!-- Descrição -->
      <div>
        <label class="block mb-1 font-semibold">Descrição</label>
        <input
          v-model="form.description"
          type="text"
          placeholder="Digite a descrição"
          class="w-full border rounded px-3 py-2"
          required
          minlength="3"
        />
      </div>

      <!-- Valor -->
      <div>
        <label class="block mb-1 font-semibold">Valor (R$)</label>
        <input
          v-model.number="form.amount"
          type="number"
          min="0.01"
          step="0.01"
          placeholder="Digite o valor"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>

      <!-- Data -->
      <div>
        <label class="block mb-1 font-semibold">Data</label>
        <input
          v-model="form.date"
          type="date"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>

      <!-- Categoria -->
      <div>
        <label class="block mb-1 font-semibold">Categoria</label>
        <select v-model="form.category_id" class="w-full border rounded px-3 py-2">
          <option value="">Selecione a categoria</option>
          <option
            v-for="cat in categories"
            :key="cat.id"
            :value="cat.id"
          >
            {{ cat.name }}
          </option>
        </select>
      </div>

      <!-- Botões -->
      <div class="flex justify-end space-x-2">
        <button
          type="button"
          @click="cancel"
          class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
        >
          Cancelar
        </button>
        <button
          type="submit"
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          {{ isEditMode ? "Atualizar" : "Criar" }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useExpenseStore } from "@/stores/expense"
import { useCategoriesStore } from "@/stores/categories"

const router = useRouter()
const route = useRoute()
const expensesStore = useExpenseStore()
const categoriesStore = useCategoriesStore()

const categories = ref([])

const isEditMode = ref(false)
const expenseId = route.params.id || null

const form = ref({
  description: "",
  amount: 0,
  date: new Date().toISOString().substr(0,10),
  category_id: ""
})

// Carregar categorias
const fetchCategories = async () => {
  categories.value = await categoriesStore.fetchAll()
}

// Se estiver editando, carregar dados da despesa
const loadExpense = async () => {
  if (!expenseId) return
  isEditMode.value = true
  const exp = expensesStore.expenses.find(e => e.id == expenseId)
  if (!exp) {
    alert("Despesa não encontrada")
    router.push("/expenses")
    return
  }
  form.value = {
    description: exp.description,
    amount: exp.amount,
    date: exp.date,
    category_id: exp.category_id || ""
  }
}

// Salvar despesa
const handleSubmit = async () => {
  try {
    if (isEditMode.value) {
      await expensesStore.editExpense(expenseId, form.value)
      alert("Despesa atualizada com sucesso")
    } else {
      await expensesStore.addExpense(form.value)
      alert("Despesa criada com sucesso")
    }
    router.push("/expenses")
  } catch (err) {
    console.error(err)
    alert("Ocorreu um erro ao salvar a despesa")
  }
}

// Cancelar
const cancel = () => {
  router.push("/expenses")
}

onMounted(() => {
  fetchCategories()
  loadExpense()
})
</script>

<style scoped>
/* ajustes de UI se necessário */
</style>
