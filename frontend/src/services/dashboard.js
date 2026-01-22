// src/services/dashboard.js
import axios from "axios";

export default {
  // =========================
  // Resumo do Dashboard
  // =========================
  async getSummary(month = null, year = null) {
    const res = await axios.get("/dashboard/summary", {
      params: { month, year },
    });
    return res.data;
  },

  // =========================
  // Evolução Mensal
  // =========================
  async getMonthlyEvolution(months = 12) {
    const res = await axios.get("/dashboard/monthly-evolution", {
      params: { months },
    });
    return res.data.data; // retorna o array de MonthlyEvolutionItem
  },

  // =========================
  // Resumo por Conta
  // =========================
  async getByAccount() {
    const res = await axios.get("/dashboard/by-account");
    return res.data; // array de AccountSummary
  },

  // =========================
  // Top categorias
  // =========================
  async getTopExpenseCategories(limit = 5) {
    const res = await axios.get("/dashboard/top-expense-categories", {
      params: { limit },
    });
    return res.data;
  },

  async getTopIncomeCategories(limit = 5) {
    const res = await axios.get("/dashboard/top-income-categories", {
      params: { limit },
    });
    return res.data;
  },

  // =========================
  // Anomalias
  // =========================
  async getAnomalies() {
    const res = await axios.get("/dashboard/anomalies");
    return res.data;
  },

  // =========================
  // Tendências
  // =========================
  async getTrends() {
    const res = await axios.get("/dashboard/trends");
    return res.data.trends; // array de TrendItem
  },

  // =========================
  // Insights
  // =========================
  async getInsights() {
    const res = await axios.get("/dashboard/insights");
    return res.data.insights; // array de InsightItem
  },

  // =========================
  // Forecast
  // =========================
  async getForecast(months = 6) {
    const res = await axios.get("/dashboard/forecast", {
      params: { months },
    });
    return res.data.forecast; // array de ForecastItem
  },
};
