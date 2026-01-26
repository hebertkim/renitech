<template>
  <div class="relative w-full max-w-2xl">

    <div class="flex">

      <!-- Categoria -->
      <select
        v-model="category"
        class="bg-gray-300 text-black px-3 rounded-l-md focus:outline-none"
      >
        <option value="all">Todos</option>
        <option value="electronics">Eletrônicos</option>
        <option value="services">Serviços</option>
        <option value="software">Softwares</option>
      </select>

      <!-- Input -->
      <input
        v-model="query"
        @input="onInput"
        @keydown.enter="submitSearch"
        @focus="showSuggestions = true"
        type="text"
        placeholder="Buscar na Renitech..."
        class="flex-1 px-4 py-2 bg-gray-200 text-black focus:outline-none"
      />

      <!-- Botão -->
      <button
        @click="submitSearch"
        class="bg-orange-500 px-4 flex items-center justify-center rounded-r-md hover:bg-orange-600 transition"
      >
        <MagnifyingGlassIcon class="w-6 h-6 text-black" />
      </button>

    </div>

    <!-- Dropdown -->
    <div
      v-if="showSuggestions && (suggestions.length || history.length)"
      class="absolute z-50 bg-white w-full mt-1 rounded shadow border"
    >

      <!-- Histórico -->
      <div v-if="!query && history.length">
        <div class="px-3 py-2 text-xs text-gray-500 flex justify-between">
          <span>Buscas recentes</span>
          <button @click="clearHistory" class="text-orange-500 hover:underline">
            Limpar
          </button>
        </div>

        <div
          v-for="(item, index) in history"
          :key="index"
          class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
          @click="useHistory(item)"
        >
          {{ item }}
        </div>
      </div>

      <!-- Sugestões -->
      <div v-if="query">
        <div
          v-for="item in suggestions"
          :key="item.id"
          class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
          @click="selectSuggestion(item.name)"
        >
          {{ item.name }}
        </div>

        <div
          v-if="suggestions.length === 0"
          class="px-4 py-2 text-gray-500"
        >
          Nenhuma sugestão
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue"
import { useRouter } from "vue-router"
import { MagnifyingGlassIcon } from "@heroicons/vue/24/solid"
import { suggest } from "@/services/searchService"

const router = useRouter()

const query = ref("")
const category = ref("all")
const suggestions = ref([])
const showSuggestions = ref(false)

const history = ref([])

// ===== Histórico =====
const loadHistory = () => {
  history.value = JSON.parse(localStorage.getItem("renitech_search_history") || "[]")
}

const saveHistory = (q) => {
  let h = JSON.parse(localStorage.getItem("renitech_search_history") || "[]")
  h = [q, ...h.filter((i) => i !== q)].slice(0, 5)
  localStorage.setItem("renitech_search_history", JSON.stringify(h))
  history.value = h
}

const clearHistory = () => {
  localStorage.removeItem("renitech_search_history")
  history.value = []
}

onMounted(loadHistory)

// ===== Autocomplete =====
const onInput = async () => {
  if (!query.value) {
    suggestions.value = []
    return
  }

  suggestions.value = await suggest(query.value)
}

// ===== Ações =====
const submitSearch = () => {
  if (!query.value) return

  saveHistory(query.value)

  showSuggestions.value = false

  router.push({
    path: "/search",
    query: {
      q: query.value,
      category: category.value,
    },
  })
}

const selectSuggestion = (name) => {
  query.value = name
  submitSearch()
}

const useHistory = (item) => {
  query.value = item
  submitSearch()
}

// Fecha dropdown ao clicar fora
document.addEventListener("click", () => {
  showSuggestions.value = false
})
</script>
