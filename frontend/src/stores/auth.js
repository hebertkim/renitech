// src/stores/auth.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import {
  login as apiLogin,
  logout as apiLogout,
  getUser as apiGetUser,
} from "@/services/api.js";

export const useAuthStore = defineStore("auth", () => {
  // ========================
  // STATE
  // ========================

  // ❗ Não carregamos usuário do localStorage, só do backend via token
  const user = ref(null);

  // ========================
  // COMPUTEDS
  // ========================

  const isAuthenticated = computed(() => !!user.value);

  const role = computed(() => user.value?.role || "cliente");

  const isClient = computed(() => role.value === "cliente");

  const isSeller = computed(() => role.value === "vendedor");

  const isAdmin = computed(() =>
    ["admin", "superadmin", "vendedor"].includes(role.value)
  );

  const isSuperAdmin = computed(() => role.value === "superadmin");

  // ========================
  // INTERNAL HELPERS
  // ========================

  const clearSession = () => {
    user.value = null;
    localStorage.removeItem("user");
    localStorage.removeItem("token");
  };

  // ========================
  // ACTIONS
  // ========================

  // Busca usuário logado pelo token
  const fetchUser = async () => {
    try {
      const userData = await apiGetUser(); // /users/me
      user.value = userData;
      return userData;
    } catch (err) {
      if (err.response && err.response.status === 401) {
        console.warn("Token inválido ou expirado. Limpando sessão...");
        clearSession();
      }
      throw err;
    }
  };

  // Login
  const login = async (email, password) => {
    try {
      await apiLogin(email, password); // salva token
      await fetchUser(); // busca /users/me
      return true;
    } catch (err) {
      console.error("Erro no login:", err);
      clearSession();
      return false;
    }
  };

  // Logout manual
  const logout = () => {
    try {
      apiLogout();
    } catch (e) {
      // mesmo se backend falhar, limpamos local
    }
    clearSession();

    // Sempre volta pro ecommerce
    window.location.href = "/welcome";
  };

  // Atualiza perfil local (apenas em memória)
  const updateProfile = (updatedUser) => {
    user.value = { ...user.value, ...updatedUser };
  };

  // ========================
  // AUTO LOGOUT AO FECHAR ABA
  // ========================

  window.addEventListener("beforeunload", () => {
    clearSession();
  });

  // ========================
  // EXPORTS
  // ========================

  return {
    // state
    user,

    // computed
    role,
    isAuthenticated,
    isClient,
    isSeller,
    isAdmin,
    isSuperAdmin,

    // actions
    login,
    logout,
    fetchUser,
    updateProfile,
  };
});
