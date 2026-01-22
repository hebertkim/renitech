<template>
  <MainLayout>
    <div class="space-y-6">

      <!-- Filtros -->
      <div class="bg-white p-4 rounded-lg shadow flex flex-wrap gap-4 items-end">
        <div>
          <label class="block mb-1 font-medium">Tipo</label>
          <select v-model="filters.type" class="border px-3 py-2 rounded">
            <option value="">Todos</option>
            <option value="expense">Despesa</option>
            <option value="income">Receita</option>
          </select>
        </div>

        <div>
          <label class="block mb-1 font-medium">Categoria</label>
          <select v-model="filters.category_id" class="border px-3 py-2 rounded">
            <option value="">Todas</option>
            <option v-for="cat in categoriesStore.categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>

        <div>
          <label class="block mb-1 font-medium">Data Inicial</label>
          <input type="date" v-model="filters.date_start" class="border px-3 py-2 rounded"/>
        </div>

        <div>
          <label class="block mb-1 font-medium">Data Final</label>
          <input type="date" v-model="filters.date_end" class="border px-3 py-2 rounded"/>
        </div>

        <div>
          <label class="block mb-1 font-medium">Valor Mínimo</label>
          <input type="number" v-model.number="filters.amount_min" class="border px-3 py-2 rounded"/>
        </div>

        <div>
          <label class="block mb-1 font-medium">Valor Máximo</label>
          <input type="number" v-model.number="filters.amount_max" class="border px-3 py-2 rounded"/>
        </div>

        <div>
          <button @click="applyFilters" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            Filtrar
          </button>
        </div>
      </div>

      <!-- Header e botão novo -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <h1 class="text-2xl font-semibold text-gray-900">Movimentações Financeiras</h1>
        <button
          @click="openModal()"
          class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        >
          + Nova {{ filters.type || 'Transação' }}
        </button>
      </div>

      <!-- Tabela -->
      <div class="bg-white shadow rounded-lg p-5 overflow-x-auto">
        <table class="w-full border-collapse border">
          <thead class="bg-gray-100">
            <tr>
              <th class="border px-2 py-1 text-left">Descrição</th>
              <th class="border px-2 py-1 text-right">Valor</th>
              <th class="border px-2 py-1 text-left">Data</th>
              <th class="border px-2 py-1 text-left">Categoria</th>
              <th class="border px-2 py-1 text-left">Tipo</th>
              <th class="border px-2 py-1 text-center">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tx in transactionStore.transactions" :key="tx.id">
              <td class="border px-2 py-1">{{ tx.description }}</td>
              <td class="border px-2 py-1 text-right">R$ {{ Number(tx.amount).toFixed(2) }}</td>
              <td class="border px-2 py-1">{{ formatDate(tx.date) }}</td>
              <td class="border px-2 py-1">{{ categoriesStore.categories.find(c => c.id === tx.category_id)?.name || '—' }}</td>
              <td class="border px-2 py-1 capitalize">{{ tx.type }}</td>
              <td class="border px-2 py-1 flex gap-2 justify-center">
                <button @click="openModal(tx)" class="bg-yellow-400 px-2 py-1 rounded hover:bg-yellow-500">Editar</button>
                <button @click="deleteTransaction(tx.id)" class="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600">Remover</button>
              </td>
            </tr>
            <tr v-if="transactionStore.transactions.length === 0">
              <td colspan="6" class="text-center py-2">Nenhuma transação encontrada.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Modal -->
      <ModalView v-model="showModal" :title="modalTitle" @save="saveTransaction">
        <template #body>
          <div class="space-y-3">
            <div>
              <label class="block mb-1 font-medium">Descrição</label>
              <input v-model="modal.description" type="text" class="w-full border px-3 py-2 rounded"/>
            </div>
            <div>
              <label class="block mb-1 font-medium">Valor</label>
              <input v-model.number="modal.amount" type="number" class="w-full border px-3 py-2 rounded"/>
            </div>
            <div>
              <label class="block mb-1 font-medium">Data</label>
              <input v-model="modal.date" type="date" class="w-full border px-3 py-2 rounded"/>
            </div>
            <div>
              <label class="block mb-1 font-medium">Categoria</label>
              <select v-model="modal.category_id" class="w-full border px-3 py-2 rounded">
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
import { reactive, ref, onMounted, computed } from "vue";
import { useTransactionStore } from "@/stores/transactions";
import { useCategoryStore } from "@/stores/category";

const transactionStore = useTransactionStore();
const categoriesStore = useCategoryStore();

const showModal = ref(false);
const modal = reactive({
  id: null,
  description: "",
  amount: 0,
  date: new Date().toISOString().substr(0,10),
  category_id: null,
  type: 'expense'
});

const filters = reactive({
  type: '',
  category_id: '',
  date_start: '',
  date_end: '',
  amount_min: null,
  amount_max: null
});

const modalTitle = computed(() =>
  modal.id
    ? (modal.type === 'expense' ? 'Editar Despesa' : 'Editar Receita')
    : (modal.type === 'expense' ? 'Nova Despesa' : 'Nova Receita')
);

const openModal = (tx = null) => {
  if(tx){
    Object.assign(modal, {...tx, amount: Number(tx.amount), date: tx.date?.substr(0,10)});
  } else {
    Object.assign(modal, { id: null, description: '', amount: 0, date: new Date().toISOString().substr(0,10), category_id: null, type: filters.type || 'expense' });
  }
  showModal.value = true;
};

const saveTransaction = async () => {
  if(!modal.description || !modal.amount) return alert("Campos obrigatórios!");
  try {
    if(modal.id) await transactionStore.editTransaction(modal.id, modal);
    else await transactionStore.addTransaction(modal);
    showModal.value = false;
    applyFilters();
  } catch(err) {
    console.error(err);
    alert("Erro ao salvar transação!");
  }
};

const deleteTransaction = async (id) => {
  if(confirm("Deseja realmente remover esta transação?")) await transactionStore.removeTransaction(id);
};

const applyFilters = async () => {
  await transactionStore.fetchAll(filters);
};

const formatDate = dateStr => new Date(dateStr).toLocaleDateString("pt-BR");

onMounted(async () => {
  await categoriesStore.fetchCategories();
  await transactionStore.fetchAll();
});
</script>
