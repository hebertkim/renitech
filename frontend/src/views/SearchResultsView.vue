<template>
  <div class="min-h-screen bg-gray-100">

    <!-- Navbar simples reaproveitável depois -->
    <header class="bg-black text-white">
      <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">

        <!-- Logo -->
        <div
          class="text-2xl font-bold cursor-pointer"
          @click="goHome"
        >
          <span class="text-orange-500">Reni</span>tech
        </div>

        <!-- Search -->
        <SearchBar />

      </div>
    </header>

    <!-- Conteúdo -->
    <main class="max-w-7xl mx-auto px-4 py-10">

      <h1 class="text-2xl font-bold mb-6">
        Resultados para: <span class="text-orange-500">"{{ q }}"</span>
      </h1>

      <div v-if="loading" class="text-gray-500">
        Buscando resultados...
      </div>

      <div v-else-if="results.length === 0" class="text-gray-500">
        Nenhum resultado encontrado.
      </div>

      <!-- Resultados -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div
          v-for="item in results"
          :key="item.id"
          class="bg-white rounded-xl shadow p-6 hover:shadow-lg transition"
        >
          <div class="h-40 bg-gray-100 rounded mb-4 flex items-center justify-center text-gray-400">
            Imagem
          </div>

          <h3 class="font-semibold text-gray-900">{{ item.name }}</h3>
          <p class="text-sm text-gray-500 mt-2">{{ item.description }}</p>

          <button
            class="mt-4 px-4 py-2 bg-black text-white rounded hover:bg-gray-800 transition"
          >
            Ver detalhes
          </button>
        </div>
      </div>

    </main>

  </div>
</template>

<script setup>
import { ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import SearchBar from "@/components/SearchBar.vue"
import { search } from "@/services/searchService"

const route = useRoute()
const router = useRouter()

const q = ref(route.query.q || "")
const category = ref(route.query.category || "all")

const loading = ref(false)
const results = ref([])

const runSearch = async () => {
  loading.value = true
  results.value = await search(q.value, category.value)
  loading.value = false
}

// Reage à mudança de querystring
watch(
  () => route.query,
  (newQuery) => {
    q.value = newQuery.q || ""
    category.value = newQuery.category || "all"
    runSearch()
  },
  { immediate: true }
)

const goHome = () => {
  router.push("/welcome")
}
</script>
