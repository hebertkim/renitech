<template>
  <MainLayout>
    <div class="space-y-8">
      <!-- Cabeçalho -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <h1 class="text-2xl font-semibold text-gray-900">Categorias</h1>
        <button
          @click="openCategoryModal()"
          class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 mt-2 sm:mt-0"
        >
          + Nova Categoria
        </button>
      </div>

      <!-- Tabela de Categorias -->
      <div class="bg-white shadow rounded-lg p-5 overflow-x-auto">
        <table class="w-full border-collapse border">
          <thead>
            <tr class="bg-gray-200">
              <th class="border px-2 py-1">Nome</th>
              <th class="border px-2 py-1">Tipo</th>
              <th class="border px-2 py-1">Pai</th>
              <th class="border px-2 py-1">Descrição</th>
              <th class="border px-2 py-1">Classe Fiscal</th>
              <th class="border px-2 py-1">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cat in categoryStore.categories" :key="cat.id">
              <td class="border px-2 py-1">{{ cat.name }}</td>
              <td class="border px-2 py-1 capitalize">{{ cat.type }}</td>
              <td class="border px-2 py-1">{{ getParentName(cat.parent_id) }}</td>
              <td class="border px-2 py-1">{{ cat.description || "-" }}</td>
              <td class="border px-2 py-1">{{ cat.fiscal_class || "-" }}</td>
              <td class="border px-2 py-1 flex gap-2">
                <button
                  @click="openCategoryModal(cat)"
                  class="bg-yellow-400 px-2 py-1 rounded hover:bg-yellow-500"
                >
                  Editar
                </button>
                <button
                  @click="deleteCategory(cat.id)"
                  class="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                >
                  Remover
                </button>
              </td>
            </tr>
            <tr v-if="categoryStore.categories.length === 0">
              <td colspan="6" class="text-center py-2">Nenhuma categoria cadastrada.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Modal Fullscreen Categoria -->
      <transition name="fade">
        <div
          v-if="showCategoryModal"
          class="fixed inset-0 z-50 bg-black bg-opacity-70 flex justify-center items-start overflow-auto p-4"
        >
          <div
            class="bg-white w-full max-w-4xl rounded-lg shadow-lg p-6 mt-8 mb-8 flex flex-col min-h-[80vh]"
          >
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-semibold">
                {{ categoryModal.id ? "Editar Categoria" : "Nova Categoria" }}
              </h2>
              <button
                @click="closeCategoryModal"
                class="text-gray-600 hover:text-gray-900 text-xl font-bold"
              >
                ✕
              </button>
            </div>

            <div class="space-y-4 flex-1 overflow-auto">
              <!-- Nome -->
              <div>
                <label class="block mb-1 font-medium">Nome</label>
                <input
                  v-model="categoryModal.name"
                  type="text"
                  placeholder="Nome da categoria"
                  class="w-full border px-3 py-2 rounded"
                />
              </div>

              <!-- Tipo -->
              <div>
                <label class="block mb-1 font-medium">Tipo</label>
                <select v-model="categoryModal.type" class="w-full border px-3 py-2 rounded">
                  <option value="expense">Despesa</option>
                  <option value="income">Receita</option>
                  <option value="transfer">Transferência</option>
                </select>
              </div>

              <!-- Categoria Pai -->
              <div>
                <label class="block mb-1 font-medium">Categoria Pai</label>
                <select v-model="categoryModal.parent_id" class="w-full border px-3 py-2 rounded">
                  <option :value="null">Nenhuma</option>
                  <option
                    v-for="cat in categoryStore.categories"
                    :key="cat.id"
                    :value="cat.id"
                    :disabled="cat.id === categoryModal.id"
                  >
                    {{ cat.name }}
                  </option>
                </select>
              </div>

              <!-- Descrição -->
              <div>
                <label class="block mb-1 font-medium">Descrição</label>
                <textarea
                  v-model="categoryModal.description"
                  placeholder="Descrição ou regras fiscais"
                  class="w-full border px-3 py-2 rounded"
                ></textarea>
              </div>

              <!-- Classe Fiscal -->
              <div>
                <label class="block mb-1 font-medium">Classe Fiscal</label>
                <input
                  v-model="categoryModal.fiscal_class"
                  type="text"
                  placeholder="Ex: ICMS, ISS..."
                  class="w-full border px-3 py-2 rounded"
                />
              </div>

              <!-- Regras de IA -->
              <div>
                <label class="block mb-1 font-medium">Regras de IA</label>
                <textarea
                  v-model="categoryModal.ai_rules"
                  placeholder='Ex: {"suggestion": "expense"}'
                  class="w-full border px-3 py-2 rounded h-32"
                ></textarea>
              </div>
            </div>

            <div class="flex justify-end gap-3 mt-6 flex-shrink-0">
              <button
                @click="closeCategoryModal"
                class="bg-gray-300 px-6 py-2 rounded hover:bg-gray-400"
              >
                Cancelar
              </button>
              <button
                @click="saveCategory"
                class="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600"
              >
                Salvar
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </MainLayout>
</template>

<script setup>
import MainLayout from "@/layouts/MainLayout.vue";
import { reactive, ref, onMounted } from "vue";
import { useCategoryStore } from "@/stores/category";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const categoryStore = useCategoryStore();

const showCategoryModal = ref(false);
const categoryModal = reactive({
  id: null,
  name: "",
  type: "expense",
  parent_id: null,
  description: "",
  fiscal_class: "",
  ai_rules: "",
});

const openCategoryModal = (cat = null) => {
  if (cat) {
    Object.assign(categoryModal, {
      id: cat.id,
      name: cat.name,
      type: cat.type,
      parent_id: cat.parent_id,
      description: cat.description || "",
      fiscal_class: cat.fiscal_class || "",
      ai_rules: JSON.stringify(cat.ai_rules || {}, null, 2),
    });
  } else {
    Object.assign(categoryModal, {
      id: null,
      name: "",
      type: "expense",
      parent_id: null,
      description: "",
      fiscal_class: "",
      ai_rules: "",
    });
  }
  showCategoryModal.value = true;
};

const closeCategoryModal = () => (showCategoryModal.value = false);

const saveCategory = async () => {
  if (!categoryModal.name) return alert("Nome obrigatório!");

  let aiRulesParsed = {};
  try {
    aiRulesParsed = categoryModal.ai_rules ? JSON.parse(categoryModal.ai_rules) : {};
  } catch (err) {
    return alert("Formato de Regras de IA inválido! Use JSON válido.");
  }

  const payload = {
    ...categoryModal,
    ai_rules: aiRulesParsed,
  };

  try {
    if (categoryModal.id) {
      await categoryStore.editCategory(categoryModal.id, payload);
    } else {
      await categoryStore.addCategory(payload);
    }
    closeCategoryModal();
  } catch (err) {
    console.error("Erro ao salvar categoria:", err);
    alert("Falha ao salvar categoria!");
  }
};

const deleteCategory = async (id) => {
  if (confirm("Deseja realmente remover esta categoria?")) {
    await categoryStore.removeCategory(id);
  }
};

const getParentName = (parentId) => {
  if (!parentId) return "-";
  const parent = categoryStore.categories.find((c) => c.id === parentId);
  return parent ? parent.name : "-";
};

onMounted(async () => {
  if (!auth.user) await auth.fetchUser();
  await categoryStore.fetchCategories();
});
</script>

<style scoped>
/* Fade animation para abrir/fechar full screen */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
