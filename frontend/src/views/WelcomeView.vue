<template>
  <MainLayout>
    <!-- Conteúdo da página Welcome -->
    <div class="text-center">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">Welcome to Finzia Dashboard</h1>
      <p class="text-gray-600 text-lg mb-6">
        This is your central hub for managing your company, monitoring KPIs, and more.
      </p>

      <div class="flex justify-center gap-4">
        <button
          @click="goToDashboard"
          class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          Go to Dashboard
        </button>
        <button
          @click="goToProfile"
          class="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-100 transition"
        >
          Profile Settings
        </button>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/layouts/MainLayout.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goToDashboard = () => {
  router.push('/dashboard')
}

const goToProfile = () => {
  router.push('/profile')
}
</script>

<style scoped>
/* Caso queira customizações específicas para a Welcome page */
</style>
