// src/stores/auth.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { login as apiLogin, logout as apiLogout, getUser as apiGetUser } from "@/services/api.js";

export const useAuthStore = defineStore("auth", () => {
  // ========================
  // STATE
  // ========================

  // ❗ NÃO carregamos mais usuário do localStorage
  const user = ref(null);

  const isAuthenticated = computed(() => !!user.value);

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

  // Busca usuário logado
  const fetchUser = async () => {
    try {
      const userData = await apiGetUser(); // retorna o usuário logado pelo token
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
      // mesmo se der erro, limpamos local
    }
    clearSession();
    window.location.href = "/login";
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

  return {
    user,
    isAuthenticated,
    login,
    logout,
    fetchUser,
    updateProfile,
  };
});
