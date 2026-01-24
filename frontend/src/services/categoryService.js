import axios from 'axios';

const API_URL = '/categories'; // Assumindo que o backend está no mesmo host

export default {
  // Listar categorias
  async getCategories(skip = 0, limit = 100) {
    const response = await axios.get(`${API_URL}/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // Obter uma categoria
  async getCategory(id) {
    const response = await axios.get(`${API_URL}/${id}`);
    return response.data;
  },

  // Criar categoria
  async createCategory(category) {
    const response = await axios.post(API_URL + '/', category);
    return response.data;
  },

  // Atualizar categoria
  async updateCategory(id, category) {
    const response = await axios.put(`${API_URL}/${id}`, category);
    return response.data;
  },

  // Deletar categoria
  async deleteCategory(id) {
    const response = await axios.delete(`${API_URL}/${id}`);
    return response.data;
  }
};
