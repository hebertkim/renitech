// src/stores/account.js
import { defineStore } from "pinia";
import { ref } from "vue";
import {
  listAccounts,
  createAccount,
  updateAccount,
  deleteAccount,
} from "@/services/api.js";

export const useAccountStore = defineStore("account", () => {
  // ========================
  // STATE
  // ========================
  const accounts = ref([]);

  // ========================
  // FETCH
  // ========================
  const fetchAccounts = async () => {
    try {
      accounts.value = await listAccounts();
    } catch (err) {
      console.error("Erro ao buscar contas:", err);
    }
  };

  // ========================
  // ADD
  // ========================
  const addAccount = async (payload) => {
    try {
      const newAcc = await createAccount(payload);
      accounts.value.push(newAcc);
      return newAcc;
    } catch (err) {
      console.error("Erro ao adicionar conta:", err);
      throw err;
    }
  };

  // ========================
  // EDIT
  // ========================
  const editAccount = async (id, payload) => {
    try {
      const updatedAcc = await updateAccount(id, payload);
      const idx = accounts.value.findIndex((c) => c.id === id);
      if (idx !== -1) accounts.value[idx] = updatedAcc;
      return updatedAcc;
    } catch (err) {
      console.error("Erro ao atualizar conta:", err);
      throw err;
    }
  };

  // ========================
  // DELETE
  // ========================
  const removeAccount = async (id) => {
    try {
      await deleteAccount(id);
      accounts.value = accounts.value.filter((c) => c.id !== id);
    } catch (err) {
      console.error("Erro ao remover conta:", err);
      throw err;
    }
  };

  return {
    accounts,
    fetchAccounts,
    addAccount,
    editAccount,
    removeAccount,
  };
});
