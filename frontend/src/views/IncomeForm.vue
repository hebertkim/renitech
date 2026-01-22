<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold">{{ isEdit ? 'Editar Receita' : 'Nova Receita' }}</h1>

    <form @submit.prevent="submitForm" class="space-y-4 max-w-md">
      <!-- Descrição -->
      <div>
        <label class="block mb-1 font-medium">Descrição</label>
        <input
          v-model="form.description"
          type="text"
          class="w-full border rounded px-3 py-2"
          placeholder="Digite a descrição"
          required
        />
      </div>

      <!-- Valor -->
      <div>
        <label class="block mb-1 font-medium">Valor</label>
        <input
          v-model.number="form.amount"
          type="number"
          step="0.01"
          min="0"
          class="w-full border rounded px-3 py-2"
          placeholder="0.00"
          required
        />
      </div>

      <!-- Data -->
      <div>
        <label class="block mb-1 font-medium">Data</label>
        <input
          v-model="form.date"
          type="date"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>

      <!-- Categoria -->
      <div>
        <label class="block mb-1 font-medium">Categoria</label>
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
      <div class="flex gap-4 mt-4">
        <button
          type="submit"
          class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        >
          {{ isEdit ? 'Atualizar' : 'Criar' }}
        </button>
        <button
          type="button"
          @click="cancel"
          class="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400"
        >
          Cancelar
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useIncomeStore } from '@/stores/income'
import { useCategoriesStore } from '@/stores/categories'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const incomeStore = useIncomeStore()
const categoriesStore = useCategoriesStore()

const form = ref({
  description: '',
  amount: 0,
  date: '',
  category_id: ''
})

const categories = ref([])
const isEdit = ref(false)
const incomeId = ref(null)

const fetchCategories = async () => {
  categories.value = await categoriesStore.fetchAll()
}

const fetchIncome = async (id) => {
  const data = await incomeStore.fetchById(id)
  if (!data) {
    alert('Receita não encontrada.')
    router.push('/incomes')
    return
  }
  form.value = {
    description: data.description,
    amount: data.amount,
    date: data.date,
    category_id: data.category_id || ''
  }
}

const submitForm = async () => {
  try {
    if (isEdit.value) {
      await incomeStore.update(incomeId.value, form.value)
      alert('Receita atualizada com sucesso!')
    } else {
      await incomeStore.create(form.value)
      alert('Receita criada com sucesso!')
    }
    router.push('/incomes')
  } catch (err) {
    alert('Erro ao salvar receita: ' + err.message)
  }
}

const cancel = () => {
  router.push('/incomes')
}

onMounted(async () => {
  await fetchCategories()
  if (route.params.id) {
    incomeId.value = parseInt(route.params.id)
    isEdit.value = true
    await fetchIncome(incomeId.value)
  }
})
</script>

<style scoped>
/* ajustes visuais se necessário */
</style>
