<template>
  <MainLayout>
    <div class="space-y-8">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-semibold text-gray-900">Contas</h1>
        <button @click="openModal()" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
          + Nova Conta
        </button>
      </div>

      <!-- Tabela de Contas -->
      <div class="bg-white shadow rounded-lg p-5 overflow-x-auto">
        <table class="w-full border-collapse border">
          <thead class="bg-gray-100">
            <tr>
              <th class="border px-2 py-1">Nome</th>
              <th class="border px-2 py-1">Saldo</th>
              <th class="border px-2 py-1">Descrição</th>
              <th class="border px-2 py-1 text-center">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="4" class="text-center py-2">Carregando...</td>
            </tr>
            <tr v-else v-for="acc in accountStore.accounts" :key="acc.id">
              <td class="border px-2 py-1">{{ acc.name }}</td>
              <td class="border px-2 py-1">R$ {{ acc.balance.toFixed(2) }}</td>
              <td class="border px-2 py-1">{{ acc.description || '—' }}</td>
              <td class="border px-2 py-1 flex gap-2 justify-center">
                <button @click="openModal(acc)" class="bg-yellow-400 px-2 py-1 rounded hover:bg-yellow-500">Editar</button>
                <button @click="deleteAccount(acc.id)" class="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600">Remover</button>
              </td>
            </tr>
            <tr v-if="!loading && accountStore.accounts.length === 0">
              <td colspan="4" class="text-center py-2">Nenhuma conta cadastrada.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Modal -->
      <ModalView v-model="showModal" :title="modalData.id ? 'Editar Conta' : 'Nova Conta'" @save="saveModal">
        <template #body>
          <div class="space-y-3">
            <div>
              <label class="block mb-1 font-medium">Nome</label>
              <input v-model="modalData.name" type="text" placeholder="Nome da conta" class="w-full border px-3 py-2 rounded" />
            </div>
            <div>
              <label class="block mb-1 font-medium">Saldo Inicial</label>
              <input v-model.number="modalData.balance" type="number" placeholder="0.00" class="w-full border px-3 py-2 rounded" />
            </div>
            <div>
              <label class="block mb-1 font-medium">Descrição</label>
              <textarea v-model="modalData.description" placeholder="Descrição opcional" class="w-full border px-3 py-2 rounded"></textarea>
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
import { ref, reactive, onMounted } from "vue";
import { useAccountStore } from "@/stores/account";

const accountStore = useAccountStore();
const loading = ref(true);

const showModal = ref(false);
const modalData = reactive({
  id: null,
  name: "",
  balance: 0,
  description: "",
});

const openModal = (acc = null) => {
  if (acc) Object.assign(modalData, acc);
  else Object.assign(modalData, { id: null, name: "", balance: 0, description: "" });
  showModal.value = true;
};

const saveModal = async () => {
  if (!modalData.name) return alert("O nome da conta é obrigatório!");
  try {
    if (modalData.id) await accountStore.editAccount(modalData.id, modalData);
    else await accountStore.addAccount(modalData);
    showModal.value = false;
  } catch (err) {
    console.error(err);
    alert("Erro ao salvar conta!");
  }
};

const deleteAccount = async (id) => {
  if (confirm("Deseja realmente remover esta conta?")) await accountStore.removeAccount(id);
};

// Init
onMounted(async () => {
  loading.value = true;
  await accountStore.fetchAccounts();
  loading.value = false;
});
</script>
