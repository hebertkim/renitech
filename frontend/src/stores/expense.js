import { defineStore } from "pinia";
import { ref } from "vue";
import { listExpenses, createExpense, updateExpense, deleteExpense } from "@/services/api.js";

export const useExpenseStore = defineStore("expense", () => {
  const expenses = ref([]);

  // ========================
  // FETCH
  // ========================
  const fetchExpenses = async (filters = {}) => {
    try {
      const data = await listExpenses(filters);
      // Ajusta tipos de dados
      expenses.value = data.map(e => ({
        ...e,
        amount: Number(e.amount || 0),
        date: e.date?.substr(0, 10) || new Date().toISOString().substr(0, 10)
      }));
    } catch (err) {
      console.error("Erro ao buscar despesas:", err);
    }
  };

  // ========================
  // ADD
  // ========================
  const addExpense = async (payload) => {
    try {
      const newExp = await createExpense(payload);
      expenses.value.push({
        ...newExp,
        amount: Number(newExp.amount || 0),
        date: newExp.date?.substr(0, 10) || new Date().toISOString().substr(0, 10)
      });
      return newExp;
    } catch (err) {
      console.error("Erro ao adicionar despesa:", err);
      throw err;
    }
  };

  // ========================
  // EDIT
  // ========================
  const editExpense = async (id, payload) => {
    try {
      const updated = await updateExpense(id, payload);
      const idx = expenses.value.findIndex(e => e.id === id);
      if (idx !== -1) expenses.value[idx] = {
        ...updated,
        amount: Number(updated.amount || 0),
        date: updated.date?.substr(0, 10) || new Date().toISOString().substr(0, 10)
      };
      return updated;
    } catch (err) {
      console.error("Erro ao editar despesa:", err);
      throw err;
    }
  };

  // ========================
  // DELETE
  // ========================
  const removeExpense = async (id) => {
    try {
      await deleteExpense(id);
      expenses.value = expenses.value.filter(e => e.id !== id);
    } catch (err) {
      console.error("Erro ao remover despesa:", err);
      throw err;
    }
  };

  return {
    expenses,
    fetchExpenses,
    addExpense,
    editExpense,
    removeExpense
  };
});
