<template>
  <MainLayout>
    <div class="space-y-8">
      <!-- Cabeçalho -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <h1 class="text-2xl font-semibold text-gray-900">Despesas</h1>
        <button
          @click="openExpenseModal()"
          class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 mt-2 sm:mt-0"
        >
          + Nova Despesa
        </button>
      </div>

      <!-- KPI Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="bg-white shadow rounded-lg p-5">
          <h2 class="text-sm font-medium text-gray-500">Total Despesas</h2>
          <p class="mt-1 text-2xl font-semibold text-gray-900">
            R$ {{ totalExpenses.toFixed(2) }}
          </p>
        </div>
        <div class="bg-white shadow rounded-lg p-5" v-if="expenseByCategory.length">
          <h2 class="text-sm font-medium text-gray-500 mb-2">Despesas por Categoria</h2>
          <CategoryPieChart :categories="expenseByCategory" />
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

      <!-- Tabela de despesas -->
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
            <tr v-for="exp in filteredExpenses" :key="exp.id">
              <td class="border px-2 py-1">{{ exp.description }}</td>
              <td class="border px-2 py-1 text-right">R$ {{ Number(exp.amount).toFixed(2) }}</td>
              <td class="border px-2 py-1">{{ formatDate(exp.date) }}</td>
              <td class="border px-2 py-1">
                {{ categoriesStore.categories.find(c => c.id === exp.category_id)?.name || '—' }}
              </td>
              <td class="border px-2 py-1 flex gap-2 justify-center">
                <button
                  @click="openExpenseModal(exp)"
                  class="bg-yellow-400 px-2 py-1 rounded hover:bg-yellow-500"
                >
                  Editar
                </button>
                <button
                  @click="deleteExpense(exp.id)"
                  class="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                >
                  Remover
                </button>
              </td>
            </tr>
            <tr v-if="filteredExpenses.length === 0">
              <td colspan="5" class="text-center py-2">Nenhuma despesa cadastrada.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Modal Fullscreen Despesa -->
      <transition name="fade">
        <div
          v-if="showModal"
          class="fixed inset-0 z-50 bg-black bg-opacity-70 flex justify-center items-start overflow-auto p-4"
        >
          <div
            class="bg-white w-full max-w-4xl rounded-lg shadow-lg p-6 mt-8 mb-8 flex flex-col min-h-[80vh]"
          >
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-semibold">
                {{ expenseModal.id ? "Editar Despesa" : "Nova Despesa" }}
              </h2>
              <button
                @click="closeExpenseModal"
                class="text-gray-600 hover:text-gray-900 text-xl font-bold"
              >
                ✕
              </button>
            </div>

            <div class="space-y-4 flex-1 overflow-auto">
              <!-- Informações básicas -->
              <div>
                <label class="block mb-1 font-medium">Descrição</label>
                <input v-model="expenseModal.description" type="text" class="w-full border px-3 py-2 rounded"/>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block mb-1 font-medium">Valor</label>
                  <input v-model.number="expenseModal.amount" type="number" class="w-full border px-3 py-2 rounded"/>
                </div>
                <div>
                  <label class="block mb-1 font-medium">Moeda</label>
                  <input v-model="expenseModal.currency" type="text" class="w-full border px-3 py-2 rounded"/>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block mb-1 font-medium">Data</label>
                  <input v-model="expenseModal.date" type="date" class="w-full border px-3 py-2 rounded"/>
                </div>
                <div>
                  <label class="block mb-1 font-medium">Vencimento</label>
                  <input v-model="expenseModal.due_date" type="date" class="w-full border px-3 py-2 rounded"/>
                </div>
              </div>

              <!-- Conta -->
              <div>
                <label class="block mb-1 font-medium">Conta</label>
                <select v-model="expenseModal.account_id" class="w-full border px-3 py-2 rounded">
                  <option :value="null">— Selecione uma conta —</option>
                  <option v-for="acc in accountStore.accounts" :key="acc.id" :value="acc.id">
                    {{ acc.name }}
                  </option>
                </select>
              </div>

              <!-- Pagamento -->
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block mb-1 font-medium">Pago</label>
                  <input type="checkbox" v-model="expenseModal.paid" />
                </div>
                <div>
                  <label class="block mb-1 font-medium">Método de Pagamento</label>
                  <select v-model="expenseModal.payment_method" class="w-full border px-3 py-2 rounded">
                    <option value="CASH">Dinheiro</option>
                    <option value="PIX">PIX</option>
                    <option value="TED">TED</option>
                    <option value="CARD">Cartão</option>
                    <option value="OTHER">Outro</option>
                  </select>
                </div>
              </div>

              <!-- Categoria e fiscal -->
              <div>
                <label class="block mb-1 font-medium">Categoria</label>
                <select v-model="expenseModal.category_id" class="w-full border px-3 py-2 rounded">
                  <option :value="null">— Sem categoria —</option>
                  <option v-for="cat in categoriesStore.categories" :key="cat.id" :value="cat.id">
                    {{ cat.name }}
                  </option>
                </select>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block mb-1 font-medium">Classe Fiscal</label>
                  <input v-model="expenseModal.fiscal_class" type="text" class="w-full border px-3 py-2 rounded"/>
                </div>
                <div>
                  <label class="block mb-1 font-medium">Imposto</label>
                  <input v-model.number="expenseModal.tax_amount" type="number" class="w-full border px-3 py-2 rounded"/>
                </div>
              </div>

              <!-- Recorrência e anexos -->
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block mb-1 font-medium">Recorrente</label>
                  <input type="checkbox" v-model="expenseModal.recurring"/>
                </div>
                <div>
                  <label class="block mb-1 font-medium">Regra de Recorrência (JSON)</label>
                  <textarea v-model="expenseModal.recurrence_rule" class="w-full border px-3 py-2 rounded h-24" placeholder='{"freq":"monthly"}'></textarea>
                </div>
              </div>
              <div>
                <label class="block mb-1 font-medium">Anexos (JSON)</label>
                <textarea v-model="expenseModal.attachment" class="w-full border px-3 py-2 rounded h-24"></textarea>
              </div>

              <!-- Conciliação -->
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block mb-1 font-medium">Status Conciliação</label>
                  <select v-model="expenseModal.reconciliation_status" class="w-full border px-3 py-2 rounded">
                    <option value="PENDING">Pendente</option>
                    <option value="RECONCILED">Conciliada</option>
                    <option value="DIVERGENT">Divergente</option>
                  </select>
                </div>
                <div>
                  <label class="block mb-1 font-medium">Data Conciliação</label>
                  <input v-model="expenseModal.reconciliation_date" type="date" class="w-full border px-3 py-2 rounded"/>
                </div>
              </div>

              <!-- Notas e IA -->
              <div>
                <label class="block mb-1 font-medium">Notas</label>
                <textarea v-model="expenseModal.notes" class="w-full border px-3 py-2 rounded h-24"></textarea>
              </div>
              <div class="grid grid-cols-2 gap-4 items-center">
                <div>
                  <label class="block mb-1 font-medium">Flag de Risco IA</label>
                  <input type="checkbox" v-model="expenseModal.ai_risk_flag" />
                </div>
                <div>
                  <label class="block mb-1 font-medium">Sugestão de Categoria IA</label>
                  <input v-model="expenseModal.ai_category_suggestion" type="text" class="w-full border px-3 py-2 rounded"/>
                </div>
              </div>
            </div>

            <!-- Ações do modal -->
            <div class="flex justify-end gap-3 mt-6 flex-shrink-0">
              <button @click="closeExpenseModal" class="bg-gray-300 px-6 py-2 rounded hover:bg-gray-400">
                Cancelar
              </button>
              <button @click="saveExpense" class="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600">
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
import CategoryPieChart from "@/components/CategoryPieChart.vue";
import { reactive, ref, onMounted, computed } from "vue";
import { useExpenseStore } from "@/stores/expense";
import { useCategoryStore } from "@/stores/category";
import { useAccountStore } from "@/stores/account";

const expenseStore = useExpenseStore();
const categoriesStore = useCategoryStore();
const accountStore = useAccountStore();

const showModal = ref(false);
const expenseModal = reactive({
  id: null,
  description: "",
  amount: 0,
  currency: "BRL",
  date: new Date().toISOString().substr(0, 10),
  due_date: "",
  paid: false,
  payment_method: "CASH",
  invoice_number: "",
  supplier: "",
  fiscal_class: "",
  tax_amount: 0,
  recurring: false,
  recurrence_rule: "",
  attachment: "",
  reconciliation_status: "PENDING",
  reconciliation_date: "",
  notes: "",
  ai_risk_flag: false,
  ai_category_suggestion: "",
  category_id: null,
  account_id: null
});

const dateFrom = ref("");
const dateTo = ref("");

const totalExpenses = computed(() =>
  expenseStore.expenses.reduce((sum, e) => sum + Number(e.amount || 0), 0)
);

const expenseByCategory = computed(() => {
  const map = {};
  expenseStore.expenses.forEach(e => {
    const cat = categoriesStore.categories.find(c => c.id === e.category_id)?.name || '—';
    map[cat] = (map[cat] || 0) + Number(e.amount || 0);
  });
  return Object.entries(map).map(([category, total]) => ({ category, total }));
});

const filteredExpenses = computed(() => {
  return expenseStore.expenses.filter(e => {
    const date = new Date(e.date);
    const from = dateFrom.value ? new Date(dateFrom.value) : null;
    const to = dateTo.value ? new Date(dateTo.value) : null;
    return (!from || date >= from) && (!to || date <= to);
  });
});

const openExpenseModal = (exp = null) => {
  if (exp) {
    Object.assign(expenseModal, {
      ...exp,
      amount: Number(exp.amount || 0),
      date: exp.date?.substr(0, 10) || new Date().toISOString().substr(0, 10),
      due_date: exp.due_date?.substr(0, 10) || "",
      reconciliation_date: exp.reconciliation_date?.substr(0,10) || "",
      attachment: JSON.stringify(exp.attachment || {}, null, 2),
      recurrence_rule: JSON.stringify(exp.recurrence_rule || {}, null, 2)
    });
  } else {
    Object.assign(expenseModal, {
      id: null,
      description: "",
      amount: 0,
      currency: "BRL",
      date: new Date().toISOString().substr(0, 10),
      due_date: "",
      paid: false,
      payment_method: "CASH",
      invoice_number: "",
      supplier: "",
      fiscal_class: "",
      tax_amount: 0,
      recurring: false,
      recurrence_rule: "",
      attachment: "",
      reconciliation_status: "PENDING",
      reconciliation_date: "",
      notes: "",
      ai_risk_flag: false,
      ai_category_suggestion: "",
      category_id: null,
      account_id: null
    });
  }
  showModal.value = true;
};

const closeExpenseModal = () => (showModal.value = false);

const saveExpense = async () => {
  try {
    if (!expenseModal.description || !expenseModal.amount || !expenseModal.account_id) {
      return alert("Preencha todos os campos obrigatórios!");
    }

    const payload = {
      ...expenseModal,
      date: new Date(expenseModal.date).toISOString(),
      due_date: expenseModal.due_date ? new Date(expenseModal.due_date).toISOString() : null,
      reconciliation_date: expenseModal.reconciliation_date ? new Date(expenseModal.reconciliation_date).toISOString() : null,
      recurrence_rule: expenseModal.recurrence_rule ? JSON.parse(expenseModal.recurrence_rule) : null,
      attachment: expenseModal.attachment ? JSON.parse(expenseModal.attachment) : null
    };

    if (payload.id) await expenseStore.editExpense(payload.id, payload);
    else await expenseStore.addExpense(payload);

    closeExpenseModal();
  } catch (err) {
    console.error(err);
    alert("Erro ao salvar despesa! Verifique os campos JSON e datas.");
  }
};

const deleteExpense = async (id) => {
  if (confirm("Deseja realmente remover esta despesa?")) {
    await expenseStore.removeExpense(id);
  }
};

const formatDate = (dateStr) => dateStr ? new Date(dateStr).toLocaleDateString("pt-BR") : "";

const applyFilters = () => {};
const resetFilters = () => {
  dateFrom.value = '';
  dateTo.value = '';
};

onMounted(async () => {
  await categoriesStore.fetchCategories();
  await accountStore.fetchAccounts();
  await expenseStore.fetchExpenses();
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
