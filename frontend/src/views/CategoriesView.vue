<template>
  <MainLayout>
  <div class="p-6 relative">
    <!-- Spinner com overlay -->
    <div v-if="loading" class="fixed inset-0 bg-white/80 flex items-center justify-center z-50">
      <div class="animate-spin h-10 w-10 border-4 border-blue-600 border-t-transparent rounded-full"></div>
      <span class="ml-2 text-blue-600 font-semibold">Carregando categorias...</span>
    </div>

    <h1 class="text-2xl font-bold mb-4">Gerenciar Categorias</h1>

    <!-- Formulário de criação/edição -->
    <div class="mb-6 p-4 border rounded shadow-sm bg-white">
      <h2 class="text-xl font-semibold mb-2">
        {{ editMode ? 'Editar Categoria' : 'Nova Categoria' }}
      </h2>
      <form @submit.prevent="saveCategory">
        <div class="mb-2">
          <label class="block mb-1 font-medium">Nome</label>
          <input v-model="categoryForm.name" type="text" class="w-full border rounded px-2 py-1" required />
        </div>
        <div class="mb-2">
          <label class="block mb-1 font-medium">Código</label>
          <input v-model="categoryForm.code" type="text" class="w-full border rounded px-2 py-1" />
        </div>
        <div class="mb-2">
          <label class="block mb-1 font-medium">Descrição</label>
          <textarea v-model="categoryForm.description" class="w-full border rounded px-2 py-1" rows="2"></textarea>
        </div>
        <div class="mb-2 flex items-center gap-2">
          <input type="checkbox" v-model="categoryForm.is_active" id="isActive" />
          <label for="isActive">Ativa</label>
        </div>
        <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          {{ editMode ? 'Atualizar' : 'Criar' }}
        </button>
        <button v-if="editMode" type="button" @click="cancelEdit" class="ml-2 px-4 py-2 rounded border hover:bg-gray-100">
          Cancelar
        </button>
      </form>
    </div>

    <!-- Lista de categorias -->
    <div class="bg-white p-4 border rounded shadow-sm">
      <h2 class="text-xl font-semibold mb-2">Categorias Cadastradas</h2>
      <table class="w-full border-collapse border">
        <thead>
          <tr class="bg-gray-100">
            <th class="border px-2 py-1 text-left">Nome</th>
            <th class="border px-2 py-1 text-left">Código</th>
            <th class="border px-2 py-1 text-left">Ativa</th>
            <th class="border px-2 py-1 text-left">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cat in categories" :key="cat.id">
            <td class="border px-2 py-1">{{ cat.name }}</td>
            <td class="border px-2 py-1">{{ cat.code }}</td>
            <td class="border px-2 py-1">{{ cat.is_active ? 'Sim' : 'Não' }}</td>
            <td class="border px-2 py-1">
              <button @click="editCategory(cat)" class="text-blue-600 hover:underline mr-2">Editar</button>
              <button @click="deleteCategory(cat.id)" class="text-red-600 hover:underline">Excluir</button>
            </td>
          </tr>
          <tr v-if="categories.length === 0 && !loading">
            <td colspan="4" class="text-center py-2 text-gray-500">Nenhuma categoria cadastrada</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  </MainLayout>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useCategoryStore } from '@/stores/category'
import MainLayout from '@/layouts/MainLayout.vue'

const categoryStore = useCategoryStore()

const categories = ref([])
const editMode = ref(false)
const loading = ref(true)  // spinner
const categoryForm = reactive({
  id: null,
  name: '',
  code: '',
  description: '',
  is_active: true,
})

// Função para carregar categorias com delay mínimo de 3s
const loadCategories = async () => {
  loading.value = true
  const start = Date.now()
  
  categories.value = await categoryStore.fetchCategories()
  
  const elapsed = Date.now() - start
  const remaining = 3000 - elapsed  // 3000ms = 3s
  if (remaining > 0) {
    await new Promise(resolve => setTimeout(resolve, remaining))
  }

  loading.value = false
}

onMounted(loadCategories)

// Criar ou atualizar categoria
const saveCategory = async () => {
  try {
    if (editMode.value) {
      await categoryStore.updateCategory(categoryForm.id, categoryForm)
    } else {
      await categoryStore.createCategory(categoryForm)
    }
    await loadCategories()
    cancelEdit()
  } catch (err) {
    console.error('Erro ao salvar categoria:', err)
  }
}

// Editar
const editCategory = (cat) => {
  categoryForm.id = cat.id
  categoryForm.name = cat.name
  categoryForm.code = cat.code
  categoryForm.description = cat.description
  categoryForm.is_active = cat.is_active
  editMode.value = true
}

// Cancelar edição
const cancelEdit = () => {
  categoryForm.id = null
  categoryForm.name = ''
  categoryForm.code = ''
  categoryForm.description = ''
  categoryForm.is_active = true
  editMode.value = false
}

// Excluir
const deleteCategory = async (id) => {
  if (!confirm('Deseja realmente excluir esta categoria?')) return
  await categoryStore.deleteCategory(id)
  await loadCategories()
}
</script>