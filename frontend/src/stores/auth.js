// src/stores/auth.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { login as apiLogin, logout as apiLogout, getUser as apiGetUser } from "@/services/api.js";

export const useAuthStore = defineStore("auth", () => {
  // ========================
  // STATE
  // ========================
  const loadUserFromStorage = () => {
    const storedUser = localStorage.getItem("user");
    if (storedUser && storedUser !== "undefined" && storedUser !== "null") {
      try {
        return JSON.parse(storedUser);
      } catch (e) {
        console.error("Erro ao parsear usuário do localStorage:", e);
        localStorage.removeItem("user");
        return null;
      }
    }
    return null;
  };

  const user = ref(loadUserFromStorage());
  const isAuthenticated = computed(() => !!user.value);

  // ========================
  // ACTIONS
  // ========================

  // Busca usuário logado
  const fetchUser = async () => {
    try {
      const userData = await apiGetUser(); // retorna o usuário
      user.value = userData;
      localStorage.setItem("user", JSON.stringify(userData));
      return userData;
    } catch (err) {
      if (err.response && err.response.status === 401) {
        console.warn("Token inválido ou expirado. Limpando sessão...");
        user.value = null;
        localStorage.removeItem("user");
        localStorage.removeItem("token");
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
      return false;
    }
  };

  // Logout
  const logout = () => {
    apiLogout();
    user.value = null;
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  // Atualiza perfil local
  const updateProfile = (updatedUser) => {
    user.value = { ...user.value, ...updatedUser };
    localStorage.setItem("user", JSON.stringify(user.value));
  };

  return {
    user,
    isAuthenticated,
    login,
    logout,
    fetchUser,
    updateProfile,
  };
});
