import { defineStore } from "pinia";
import { ref } from "vue";
import {
  listCategories,
  createCategory,
  updateCategory,
  deleteCategory,
} from "@/services/api.js";

export const useCategoryStore = defineStore("category", () => {
  const categories = ref([]);

  // ========================
  // FETCH
  // ========================
  const fetchCategories = async () => {
    try {
      categories.value = await listCategories();
    } catch (err) {
      console.error("Erro ao buscar categorias:", err);
    }
  };

  // ========================
  // ADD
  // ========================
  const addCategory = async (payload) => {
    try {
      const newCat = await createCategory(payload);
      categories.value.push(newCat);
      return newCat;
    } catch (err) {
      console.error("Erro ao adicionar categoria:", err);
      throw err;
    }
  };

  // ========================
  // EDIT
  // ========================
  const editCategory = async (id, payload) => {
    try {
      const updatedCat = await updateCategory(id, payload);
      const idx = categories.value.findIndex((c) => c.id === id);
      if (idx !== -1) categories.value[idx] = updatedCat;
      return updatedCat;
    } catch (err) {
      console.error("Erro ao atualizar categoria:", err);
      throw err;
    }
  };

  // ========================
  // DELETE
  // ========================
  const removeCategory = async (id) => {
    try {
      await deleteCategory(id);
      categories.value = categories.value.filter((c) => c.id !== id);
    } catch (err) {
      console.error("Erro ao remover categoria:", err);
      throw err;
    }
  };

  return {
    categories,
    fetchCategories,
    addCategory,
    editCategory,
    removeCategory,
  };
});
