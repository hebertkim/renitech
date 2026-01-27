<template>
  <div class="min-h-screen bg-gray-100">

    <!-- ================= NAVBAR ================= -->
    <header class="bg-black text-white w-full">
      <div class="flex items-center justify-between px-8 py-3 gap-4">

        <!-- Logo -->
        <div
          class="text-2xl font-bold cursor-pointer select-none"
          @click="goHome"
        >
          <span class="text-orange-500">Reni</span>tech
        </div>

        <!-- SearchBar Component -->
        <div class="flex-1 hidden md:flex justify-center">
          <SearchBar />
        </div>

        <!-- Right Actions -->
        <div class="flex items-center gap-6">

          <!-- Cliente logado / Dropdown -->
          <Menu as="div" class="relative" v-if="isAuthenticated">
            <MenuButton
              class="flex items-center gap-1 text-sm leading-tight cursor-pointer hover:text-orange-400 transition"
            >
              <div class="flex flex-col">
                <span class="text-xs text-gray-300">Olá, {{ userName }}</span>
                <span class="font-bold text-orange-500">Seja bem-vindo</span>
              </div>
              <!-- Ícone discreto de dropdown -->
              <svg class="w-4 h-4 text-gray-300 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </MenuButton>

            <MenuItems
              class="absolute right-0 mt-2 w-48 rounded-md bg-white py-2 shadow-lg ring-1 ring-black/10 z-50"
            >
              <MenuItem>
                <a
                  href="#"
                  @click.prevent="goProfile"
                  class="block px-4 py-2 text-sm text-gray-900 hover:bg-orange-50"
                >
                  Meu perfil
                </a>
              </MenuItem>
              <MenuItem>
                <a
                  href="#"
                  class="block px-4 py-2 text-sm text-gray-900 hover:bg-orange-50"
                >
                  Meus pedidos
                </a>
              </MenuItem>
              <MenuItem>
                <a
                  href="#"
                  @click.prevent="logout"
                  class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                >
                  Sair
                </a>
              </MenuItem>
            </MenuItems>
          </Menu>

          <!-- Login / Conta (não logado) -->
          <div
            class="text-sm leading-tight cursor-pointer hover:text-orange-400 transition"
            v-if="!isAuthenticated"
            @click="goToLogin"
          >
            <div class="text-xs text-gray-300">Olá, faça seu</div>
            <div class="font-bold">Login / Conta</div>
          </div>

          <!-- Carrinho -->
          <div class="relative cursor-pointer hover:text-orange-400 transition">
            🛒
            <span
              class="absolute -top-2 -right-3 bg-orange-500 text-black text-xs font-bold rounded-full px-1.5"
            >
              0
            </span>
          </div>
        </div>
      </div>

      <!-- Submenu -->
      <div class="bg-gray-900 text-sm w-full">
        <div class="flex px-8 py-2 gap-6 text-gray-300">
          <span class="hover:text-orange-400 cursor-pointer">Todos</span>
          <span class="hover:text-orange-400 cursor-pointer">Ofertas</span>
          <span class="hover:text-orange-400 cursor-pointer">Eletrônicos</span>
          <span class="hover:text-orange-400 cursor-pointer">Serviços</span>
          <span class="hover:text-orange-400 cursor-pointer">Empresas</span>
        </div>
      </div>
    </header>

    <!-- ================= CONTEÚDO ================= -->
    <main class="max-w-7xl mx-auto px-4 py-10">

      <!-- Hero -->
      <div class="bg-white rounded-xl shadow p-10 text-center">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          Bem-vindo à <span class="text-orange-500">Renitech</span>
        </h1>

        <p class="text-gray-600 text-lg mb-8">
          Sua plataforma completa para compras, gestão e tecnologia.
        </p>

        <div class="flex justify-center gap-4 flex-wrap">
          <button
            @click="goToStore"
            class="px-6 py-3 bg-orange-500 text-black rounded-lg hover:bg-orange-600 transition font-bold"
          >
            Ver produtos
          </button>
        </div>
      </div>

      <!-- Vitrine fake -->
      <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div
          v-for="i in 3"
          :key="i"
          class="bg-white rounded-xl shadow p-6 text-center hover:shadow-lg transition"
        >
          <div class="h-40 bg-gray-100 rounded mb-4 flex items-center justify-center text-gray-400">
            Imagem
          </div>

          <h3 class="font-semibold text-gray-900">Produto em destaque</h3>

          <p class="text-sm text-gray-500 mt-2">
            Em breve aqui aparecerão os produtos da sua loja.
          </p>

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
import { computed } from "vue"
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"
import SearchBar from "@/components/SearchBar.vue"
import { Menu, MenuButton, MenuItems, MenuItem } from "@headlessui/vue"

const router = useRouter()
const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const userName = computed(() => authStore.user?.name || "")

const goToStore = () => router.push("/search?q=&category=all")
const goToLogin = () => router.push("/login")
const goHome = () => router.push("/welcome")
const goProfile = () => router.push("/profile")
const logout = () => authStore.logout()
</script>

<style scoped>
/* Tailwind controla todo o estilo */
</style>
