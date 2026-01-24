import { defineStore } from 'pinia'
import axios from 'axios'

export const useCategoryStore = defineStore('category', {
  state: () => ({
    categories: [],
  }),
  actions: {
    // Buscar todas categorias
    async fetchCategories() {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://localhost:8000/categories/', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.categories = res.data
        return this.categories
      } catch (err) {
        console.error('Erro ao buscar categorias:', err)
        return []
      }
    },

    // Criar nova categoria
    async createCategory(categoryData) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.post('http://localhost:8000/categories/', categoryData, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.categories.push(res.data)
        return res.data
      } catch (err) {
        console.error('Erro ao criar categoria:', err)
        throw err
      }
    },

    // Atualizar categoria existente
    async updateCategory(id, categoryData) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.put(`http://localhost:8000/categories/${id}`, categoryData, {
          headers: { Authorization: `Bearer ${token}` }
        })
        const index = this.categories.findIndex(cat => cat.id === id)
        if (index !== -1) this.categories[index] = res.data
        return res.data
      } catch (err) {
        console.error('Erro ao atualizar categoria:', err)
        throw err
      }
    },

    // Excluir categoria
    async deleteCategory(id) {
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`http://localhost:8000/categories/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.categories = this.categories.filter(cat => cat.id !== id)
      } catch (err) {
        console.error('Erro ao excluir categoria:', err)
        throw err
      }
    }
  }
})
