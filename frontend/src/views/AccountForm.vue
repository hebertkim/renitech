<!-- src/views/AccountForm.vue -->
<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold">
      {{ isEdit ? 'Editar Conta' : 'Nova Conta' }}
    </h1>

    <form @submit.prevent="submitForm" class="space-y-4 max-w-md">
      <div>
        <label class="block mb-1">Nome da Conta</label>
        <input
          v-model="form.name"
          type="text"
          placeholder="Ex.: Conta Corrente"
          class="border rounded px-3 py-2 w-full"
          required
        />
      </div>

      <div>
        <label class="block mb-1">Saldo Inicial</label>
        <input
          v-model.number="form.balance"
          type="number"
          step="0.01"
          placeholder="0.00"
          class="border rounded px-3 py-2 w-full"
          required
        />
      </div>

      <div class="flex gap-4">
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
import { useAccountStore } from '@/stores/account'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const accountsStore = useAccountStore()

const isEdit = ref(false)
const form = ref({
  name: '',
  balance: 0
})

const accountId = route.params.id

onMounted(async () => {
  if (accountId) {
    isEdit.value = true
    await accountsStore.fetchAccounts()
    const acc = accountsStore.accounts.find(a => a.id == accountId)
    if (acc) {
      form.value.name = acc.name
      form.value.balance = acc.balance
    }
  }
})

const submitForm = async () => {
  try {
    if (isEdit.value) {
      await accountsStore.editAccount(accountId, form.value)
    } else {
      await accountsStore.addAccount(form.value)
    }
    router.push('/accounts')
  } catch (err) {
    alert('Erro ao salvar a conta: ' + err.message)
  }
}

const cancel = () => {
  router.push('/accounts')
}
</script>

<style scoped>
/* ajustes visuais se necessário */
</style>
