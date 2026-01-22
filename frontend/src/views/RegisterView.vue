<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-50">
    <div class="w-full max-w-md p-4 bg-white rounded-lg shadow-md">
      <div class="mb-6 mt-2">
        <img
          src="../assets/img/logo.png"
          alt="Logo"
          class="w-16 h-16 mx-auto rounded-full shadow-md"
        />
      </div>
      <h2 class="mb-6 text-2xl font-bold text-center text-gray-800">Create Account</h2>
      <form @submit.prevent="onSubmit">
        <div class="mb-4">
          <label class="block mb-1 text-sm font-medium text-gray-700">Full Name</label>
          <input
            type="text"
            v-model="name"
            required
            class="w-full px-4 py-2 border rounded-md focus:ring focus:ring-blue-300"
          />
        </div>
        <div class="mb-4">
          <label class="block mb-1 text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            v-model="email"
            required
            class="w-full px-4 py-2 border rounded-md focus:ring focus:ring-blue-300"
          />
        </div>
        <div class="mb-4">
          <label class="block mb-1 text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            v-model="password"
            required
            class="w-full px-4 py-2 border rounded-md focus:ring focus:ring-blue-300"
          />
        </div>
        <div class="mb-4">
          <label class="block mb-1 text-sm font-medium text-gray-700">Confirm Password</label>
          <input
            type="password"
            v-model="confirmPassword"
            required
            class="w-full px-4 py-2 border rounded-md focus:ring focus:ring-blue-300"
          />
        </div>
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-2 mb-4 text-white bg-gray-500 rounded-md hover:bg-gray-600 transition-colors"
          :class="loading ? 'opacity-75 cursor-not-allowed' : ''"
        >
          {{ loading ? 'Creating Account...' : 'Create Account' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { register } from '@/services/api'
import { useRouter } from 'vue-router'

export default {
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
      internalLoading: false,
    }
  },
  computed: {
    loading() {
      return this.internalLoading
    },
  },
  methods: {
    async onSubmit() {
      if (this.loading) return
      this.internalLoading = true

      if (this.password !== this.confirmPassword) {
        alert('Passwords do not match!')
        this.internalLoading = false
        return
      }

      try {
        console.log('Tentando registro...')

        const payload = {
          name: this.name,
          email: this.email,
          password: this.password,
          confirm_password: this.confirmPassword, // ⚠️ NOME EXATO
        }

        console.log('Payload enviado:', payload)

        await register(payload) // ✅ ENVIA OBJETO

        console.log('Registro bem-sucedido!')
        alert('Registration successful!')
        this.router.push('/login')
      } catch (err) {
        console.error('Erro no registro:', err?.response?.data || err)
        alert('Registration failed, check your input and server.')
      } finally {
        this.internalLoading = false
      }
    },
  },
}
</script>
