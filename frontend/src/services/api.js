import axios from "axios";

// ============================
// CONFIGURAÇÃO DO AXIOS
// ============================
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  // O Axios detecta Content-Type automaticamente
});

// ============================
// INTERCEPTOR AUTOMÁTICO
// ============================
// Envia token automaticamente, se existir
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ============================
// AUTENTICAÇÃO
// ============================
export async function login(email, password) {
  const form = new FormData();
  form.append("username", email); // OAuth2 usa "username"
  form.append("password", password);

  const { data } = await api.post("/users/login", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  localStorage.setItem("token", data.access_token);
  return data;
}

export function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
}

export async function getUser() {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Usuário não autenticado");

  const { data } = await api.get("/users/me", {
    headers: { Authorization: `Bearer ${token}` },
  });

  return data;
}

export async function register(payload) {
  const { data } = await api.post("/users", payload);
  return data;
}

// ============================
// PERFIL
// ============================
export async function getProfile() {
  const { data } = await api.get("/users/me");
  return data;
}

export async function updateProfile(payload) {
  const { data } = await api.put("/users/me", payload);
  return data;
}

// ============================
// DESPESAS - CRUD
// ============================
export async function listExpenses(params = {}) {
  const { data } = await api.get("/expenses", { params });
  return data;
}

export async function getExpense(id) {
  const { data } = await api.get(`/expenses/${id}`);
  return data;
}

export async function createExpense(payload) {
  const { data } = await api.post("/expenses", payload);
  return data;
}

export async function updateExpense(id, payload) {
  const { data } = await api.put(`/expenses/${id}`, payload);
  return data;
}

export async function deleteExpense(id) {
  await api.delete(`/expenses/${id}`);
}

// ============================
// CATEGORIAS - CRUD
// ============================
export async function listCategories() {
  const { data } = await api.get("/categories");
  return data;
}

export async function createCategory(payload) {
  const { data } = await api.post("/categories", payload);
  return data;
}

export async function updateCategory(id, payload) {
  const { data } = await api.put(`/categories/${id}`, payload);
  return data;
}

export async function deleteCategory(id) {
  await api.delete(`/categories/${id}`);
}

// ============================
// CONTAS - CRUD
// ============================
export async function listAccounts() {
  const { data } = await api.get("/accounts");
  return data;
}

export async function createAccount(payload) {
  const { data } = await api.post("/accounts", payload);
  return data;
}

export async function updateAccount(id, payload) {
  const { data } = await api.put(`/accounts/${id}`, payload);
  return data;
}

export async function deleteAccount(id) {
  await api.delete(`/accounts/${id}`);
}

// ============================
// RECEITAS - CRUD
// ============================
export async function listIncomes(params = {}) {
  const { data } = await api.get("/incomes", { params });
  return data;
}

export async function getIncome(id) {
  const { data } = await api.get(`/incomes/${id}`);
  return data;
}

export async function createIncome(payload) {
  const { data } = await api.post("/incomes", payload);
  return data;
}

export async function updateIncome(id, payload) {
  const { data } = await api.put(`/incomes/${id}`, payload);
  return data;
}

export async function deleteIncome(id) {
  await api.delete(`/incomes/${id}`);
}

// ============================
// EXPORT DEFAULT
// ============================
export default api;
