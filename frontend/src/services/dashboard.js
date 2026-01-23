import axios from "axios";

export default {
  // =========================
  // Obter Resumo do Dashboard
  // =========================
  async getDashboardSummary() {
    try {
      const res = await axios.get("/api/dashboard");
      return res.data;
    } catch (error) {
      console.error("Erro ao obter resumo do dashboard:", error);
      throw error;
    }
  },

  // =========================
  // Obter Produtos com Estoque Baixo
  // =========================
  async getLowStockProducts() {
    try {
      const res = await axios.get("/api/dashboard/low-stock");
      return res.data;
    } catch (error) {
      console.error("Erro ao obter produtos com estoque baixo:", error);
      throw error;
    }
  },
};
