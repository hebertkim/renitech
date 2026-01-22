<template>
  <MainLayout>
    <div class="space-y-8">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <h1 class="text-2xl font-semibold text-gray-900">Receitas</h1>
        <button
          @click="openModal()"
          class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        >
          + Nova Receita
        </button>
      </div>

      <!-- Tabela de receitas -->
      <div class="bg-white shadow rounded-lg p-5 overflow-x-auto">
        <table class="w-full border-collapse border">
          <thead class="bg-gray-100">
            <tr>
              <th class="border px-2 py-1 text-left">Descrição</th>
              <th class="border px-2 py-1 text-right">Valor</th>
              <th class="border px-2 py-1 text-left">Data</th>
              <th class="border px-2 py-1 text-left">Categoria</th>
              <th class="border px-2 py-1 text-center">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="inc in incomeStore.incomes" :key="inc.id">
              <td class="border px-2 py-1">{{ inc.description }}</td>
              <td class="border px-2 py-1 text-right">R$ {{ Number(inc.amount).toFixed(2) }}</td>
              <td class="border px-2 py-1">{{ formatDate(inc.date) }}</td>
              <td class="border px-2 py-1">
                {{ categoriesStore.categories.find(c => c.id === inc.category_id)?.name || '—' }}
              </td>
              <td class="border px-2 py-1 flex gap-2 justify-center">
                <button @click="openModal(inc)" class="bg-yellow-400 px-2 py-1 rounded hover:bg-yellow-500">
                  Editar
                </button>
                <button @click="deleteIncome(inc.id)" class="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600">
                  Remover
                </button>
              </td>
            </tr>
            <tr v-if="incomeStore.incomes.length === 0">
              <td colspan="5" class="text-center py-2">Nenhuma receita cadastrada.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Modal Genérico -->
      <ModalView
        v-model="showModal"
        :title="incomeModal.id ? 'Editar Receita' : 'Nova Receita'"
        @save="saveIncome"
      >
        <template #body>
          <div class="space-y-3">
            <div>
              <label class="block mb-1 font-medium">Descrição</label>
              <input v-model="incomeModal.description" type="text" class="w-full border px-3 py-2 rounded" />
            </div>
            <div>
              <label class="block mb-1 font-medium">Valor</label>
              <input v-model.number="incomeModal.amount" type="number" class="w-full border px-3 py-2 rounded" />
            </div>
            <div>
              <label class="block mb-1 font-medium">Data</label>
              <input v-model="incomeModal.date" type="date" class="w-full border px-3 py-2 rounded" />
            </div>
            <div>
              <label class="block mb-1 font-medium">Categoria</label>
              <select v-model="incomeModal.category_id" class="w-full border px-3 py-2 rounded">
                <option :value="null">— Sem categoria —</option>
                <option v-for="cat in categoriesStore.categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
              </select>
            </div>
          </div>
        </template>
      </ModalView>
    </div>
  </MainLayout>
</template>

<script setup>
import MainLayout from "@/layouts/MainLayout.vue";
import ModalView from "@/components/ModalView.vue";
import { reactive, ref, onMounted } from "vue";
import { useIncomeStore } from "@/stores/income";
import { useCategoryStore } from "@/stores/category";

const incomeStore = useIncomeStore();
const categoriesStore = useCategoryStore();

// Modal
const showModal = ref(false);
const incomeModal = reactive({
  id: null,
  description: "",
  amount: 0,
  date: new Date().toISOString().substr(0, 10),
  category_id: null,
});

const openModal = (inc = null) => {
  if (inc) {
    Object.assign(incomeModal, {
      ...inc,
      amount: Number(inc.amount),
      date: inc.date?.substr(0, 10) || new Date().toISOString().substr(0, 10)
    });
  } else {
    Object.assign(incomeModal, {
      id: null,
      description: "",
      amount: 0,
      date: new Date().toISOString().substr(0, 10),
      category_id: null,
    });
  }
  showModal.value = true;
};

const saveIncome = async () => {
  if (!incomeModal.description || !incomeModal.amount) return alert("Campos obrigatórios!");
  
  try {
    // 🔹 Remover 'id' no POST
    const { id, ...payload } = incomeModal;

    if (id) await incomeStore.editIncome(id, payload);
    else await incomeStore.addIncome(payload);

    showModal.value = false;
  } catch (err) {
    console.error(err);
    alert("Erro ao salvar receita!");
  }
};

const deleteIncome = async (id) => {
  if (confirm("Deseja realmente remover esta receita?")) {
    await incomeStore.removeIncome(id);
  }
};

const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString("pt-BR");

onMounted(async () => {
  await categoriesStore.fetchCategories();
  await incomeStore.fetchAll();
});
</script>
