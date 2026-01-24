<template>
  <MainLayout>
    <div class="p-6 relative space-y-6">
      <!-- Spinner com overlay -->
      <div v-if="loading" class="fixed inset-0 bg-white/80 flex items-center justify-center z-50">
        <div class="animate-spin h-10 w-10 border-4 border-blue-600 border-t-transparent rounded-full"></div>
        <span class="ml-2 text-blue-600 font-semibold">Carregando categorias...</span>
      </div>

      <h1 class="text-3xl font-bold text-gray-800">Gerenciar Categorias</h1>

      <div class="grid md:grid-cols-2 gap-6">
        <!-- Formulário de criação/edição -->
        <div class="p-6 bg-white rounded-xl shadow-md border border-gray-200">
          <h2 class="text-xl font-semibold mb-4">
            {{ editMode ? 'Editar Categoria' : 'Nova Categoria' }}
          </h2>
          <form @submit.prevent="saveCategory" class="space-y-4">
            <div>
              <label class="block mb-1 font-medium text-gray-700">Nome</label>
              <input
                v-model="categoryForm.name"
                type="text"
                class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            <div>
              <label class="block mb-1 font-medium text-gray-700">Código</label>
              <input
                v-model="categoryForm.code"
                type="text"
                class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label class="block mb-1 font-medium text-gray-700">Descrição</label>
              <textarea
                v-model="categoryForm.description"
                class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows="3"
              ></textarea>
            </div>

            <div class="flex items-center gap-2">
              <input type="checkbox" v-model="categoryForm.is_active" id="isActive" class="h-4 w-4 text-blue-600 rounded"/>
              <label for="isActive" class="text-gray-700 font-medium">Ativa</label>
            </div>

            <div class="flex gap-2">
              <button
                type="submit"
                class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
              >
                {{ editMode ? 'Atualizar' : 'Criar' }}
              </button>
              <button
                v-if="editMode"
                type="button"
                @click="cancelEdit"
                class="px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-100 transition"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>

        <!-- Lista de categorias -->
        <div class="p-6 bg-white rounded-xl shadow-md border border-gray-200 overflow-x-auto">
          <h2 class="text-xl font-semibold mb-4">Categorias Cadastradas</h2>
          <table class="min-w-full border-collapse">
            <thead>
              <tr class="bg-gray-100 text-left">
                <th class="px-4 py-2 font-medium text-gray-700">Nome</th>
                <th class="px-4 py-2 font-medium text-gray-700">Código</th>
                <th class="px-4 py-2 font-medium text-gray-700">Ativa</th>
                <th class="px-4 py-2 font-medium text-gray-700">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="cat in categories"
                :key="cat.id"
                class="hover:bg-gray-50 transition"
              >
                <td class="px-4 py-2">{{ cat.name }}</td>
                <td class="px-4 py-2">{{ cat.code }}</td>
                <td class="px-4 py-2">{{ cat.is_active ? 'Sim' : 'Não' }}</td>
                <td class="px-4 py-2 flex gap-2">
                  <button
                    @click="editCategory(cat)"
                    class="text-blue-600 hover:text-blue-800 font-medium"
                  >
                    Editar
                  </button>
                  <button
                    @click="deleteCategory(cat.id)"
                    class="text-red-600 hover:text-red-800 font-medium"
                  >
                    Excluir
                  </button>
                </td>
              </tr>
              <tr v-if="categories.length === 0 && !loading">
                <td colspan="4" class="text-center py-4 text-gray-500">Nenhuma categoria cadastrada</td>
              </tr>
            </tbody>
          </table>
        </div>
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
const loading = ref(true)
const categoryForm = reactive({
  id: null,
  name: '',
  code: '',
  description: '',
  is_active: true,
})

const loadCategories = async () => {
  loading.value = true
  const start = Date.now()
  categories.value = await categoryStore.fetchCategories()
  const elapsed = Date.now() - start
  const remaining = 3000 - elapsed
  if (remaining > 0) await new Promise(r => setTimeout(r, remaining))
  loading.value = false
}

onMounted(loadCategories)

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
    console.error(err)
  }
}

const editCategory = (cat) => {
  Object.assign(categoryForm, cat)
  editMode.value = true
}

const cancelEdit = () => {
  categoryForm.id = null
  categoryForm.name = ''
  categoryForm.code = ''
  categoryForm.description = ''
  categoryForm.is_active = true
  editMode.value = false
}

const deleteCategory = async (id) => {
  if (!confirm('Deseja realmente excluir esta categoria?')) return
  await categoryStore.deleteCategory(id)
  await loadCategories()
}
</script>
