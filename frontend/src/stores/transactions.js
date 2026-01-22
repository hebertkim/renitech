import { defineStore } from "pinia";
import { ref } from "vue";
import {
  listExpenses,
  listIncomes,
  createExpense,
  createIncome,
  updateExpense,
  updateIncome,
  deleteExpense,
  deleteIncome
} from "@/services/api.js";

export const useTransactionStore = defineStore("transactions", () => {
  const transactions = ref([]);

  // ========================
  // FETCH
  // ========================
  const fetchAll = async (filters = {}) => {
    try {
      let data = [];

      if (!filters.type || filters.type === "expense") {
        const expenses = await listExpenses(filters);
        data = data.concat(expenses.map(e => ({ ...e, type: "expense" })));
      }

      if (!filters.type || filters.type === "income") {
        const incomes = await listIncomes(filters);
        data = data.concat(incomes.map(i => ({ ...i, type: "income" })));
      }

      // Ordenar por data decrescente
      transactions.value = data.sort((a, b) => new Date(b.date) - new Date(a.date));
    } catch (err) {
      console.error("Erro ao buscar transações:", err);
    }
  };

  // ========================
  // ADD
  // ========================
  const addTransaction = async (payload) => {
    try {
      let newTx;
      if (payload.type === "expense") newTx = await createExpense(payload);
      else if (payload.type === "income") newTx = await createIncome(payload);

      newTx.type = payload.type;
      transactions.value.push(newTx);
      return newTx;
    } catch (err) {
      console.error("Erro ao adicionar transação:", err);
      throw err;
    }
  };

  // ========================
  // EDIT
  // ========================
  const editTransaction = async (id, payload) => {
    try {
      let updated;
      if (payload.type === "expense") updated = await updateExpense(id, payload);
      else if (payload.type === "income") updated = await updateIncome(id, payload);

      updated.type = payload.type;
      const idx = transactions.value.findIndex((t) => t.id === id);
      if (idx !== -1) transactions.value[idx] = updated;
      return updated;
    } catch (err) {
      console.error("Erro ao atualizar transação:", err);
      throw err;
    }
  };

  // ========================
  // DELETE
  // ========================
  const removeTransaction = async (id) => {
    try {
      const tx = transactions.value.find(t => t.id === id);
      if (!tx) return;

      if (tx.type === "expense") await deleteExpense(id);
      else if (tx.type === "income") await deleteIncome(id);

      transactions.value = transactions.value.filter(t => t.id !== id);
    } catch (err) {
      console.error("Erro ao remover transação:", err);
      throw err;
    }
  };

  return {
    transactions,
    fetchAll,
    addTransaction,
    editTransaction,
    removeTransaction,
  };
});
