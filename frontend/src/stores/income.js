import { defineStore } from "pinia";
import { ref } from "vue";
import { listIncomes, createIncome, updateIncome, deleteIncome } from "@/services/api.js";

export const useIncomeStore = defineStore("income", () => {
  const incomes = ref([]);

  // ========================
  // FETCH
  // ========================
  const fetchAll = async (filters = {}) => {
    try {
      incomes.value = await listIncomes(filters);
    } catch (err) {
      console.error("Erro ao buscar receitas:", err);
      incomes.value = [];
    }
  };

  // ========================
  // ADD
  // ========================
  const addIncome = async (payload) => {
    try {
      const newInc = await createIncome(payload); // payload já sem id
      incomes.value.push(newInc);
      return newInc;
    } catch (err) {
      console.error("Erro ao adicionar receita:", err);
      throw new Error("Falha ao adicionar receita");
    }
  };

  // ========================
  // EDIT
  // ========================
  const editIncome = async (id, payload) => {
    try {
      const updated = await updateIncome(id, payload);
      const idx = incomes.value.findIndex(i => i.id === id);
      if (idx !== -1) incomes.value[idx] = updated;
      return updated;
    } catch (err) {
      console.error("Erro ao atualizar receita:", err);
      throw new Error("Falha ao atualizar receita");
    }
  };

  // ========================
  // DELETE
  // ========================
  const removeIncome = async (id) => {
    try {
      await deleteIncome(id);
      incomes.value = incomes.value.filter(i => i.id !== id);
    } catch (err) {
      console.error("Erro ao remover receita:", err);
      throw new Error("Falha ao remover receita");
    }
  };

  return {
    incomes,
    fetchAll,
    addIncome,
    editIncome,
    removeIncome
  };
});
