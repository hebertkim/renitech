<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-50">
    <div class="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
      <div class="mb-6 mt-2">
        <img src="../assets/img/logo.png" alt="Logo" class="w-16 h-16 mx-auto rounded-full shadow-md" />
      </div>
      <h2 class="mb-6 text-2xl font-bold text-center text-gray-800">Login</h2>
      <form @submit.prevent="onSubmit">
        <div class="mb-4">
          <label class="block mb-1 text-sm font-medium text-gray-700">Email</label>
          <input type="email" v-model="email" required
            class="w-full px-4 py-2 border rounded-md focus:ring focus:ring-blue-300" />
        </div>
        <div class="mb-6">
          <label class="block mb-1 text-sm font-medium text-gray-700">Password</label>
          <input type="password" v-model="password" required
            class="w-full px-4 py-2 border rounded-md focus:ring focus:ring-blue-300" />
        </div>
        <button type="submit" :disabled="loading"
          class="w-full py-2 text-white rounded-md transition-colors"
          :class="loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-gray-500 hover:bg-gray-600'">
          {{ loading ? 'Logging in...' : 'Log In' }}
        </button>
      </form>
      <p class="text-sm mt-4 text-center">
        Don't have an account?
        <router-link to="/register" class="text-blue-500 hover:underline">Create Account</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const email = ref('');
const password = ref('');
const loading = ref(false);
const router = useRouter();
const auth = useAuthStore();

const onSubmit = async () => {
  if (loading.value) return;

  loading.value = true;
  try {
    console.log('Tentando login...');
    const success = await auth.login(email.value, password.value);
    if (success) {
      console.log('Login bem-sucedido, redirecionando...');
      await router.push('/welcome');
    } else {
      console.error('Credenciais inválidas.');
      alert('Invalid credentials');
    }
  } catch (err) {
    console.error('Erro geral no login:', err);
    alert('Login failed, check server.');
  } finally {
    loading.value = false;
  }
};
</script>
