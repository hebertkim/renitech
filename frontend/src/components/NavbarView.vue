<template>
  <div class="min-h-screen bg-white">

    <!-- ==================== HEADER ==================== -->
    <header class="bg-black text-white w-full">
      <div class="flex items-center justify-between px-6 md:px-8 py-2 md:py-3 gap-4">

        <!-- LOGO -->
        <div class="text-2xl font-bold cursor-pointer select-none" @click="goHome">
          <span class="text-orange-500">Reni</span>tech
        </div>

        <!-- SEARCHBAR -->
        <div class="flex-1 hidden md:flex justify-center">
          <SearchBar />
        </div>

        <!-- AÇÕES DIREITA -->
        <div class="flex items-center gap-5 text-sm">

          <!-- LOGIN -->
          <div v-if="!isAuthenticated" class="cursor-pointer text-right" @click="goToLogin">
            <span class="block text-xs text-gray-300">Olá, faça seu</span>
            <span class="font-bold text-sm text-orange-500">Login</span>
          </div>

          <!-- USUÁRIO / CONTA -->
          <Menu as="div" class="relative" v-if="isAuthenticated">
            <MenuButton class="flex flex-col items-start text-right hover:text-orange-400">
              <span class="text-xs text-gray-300">Olá, {{ userName }}</span>
              <div class="flex items-center gap-1 font-bold text-sm text-orange-500">
                Conta e Listas
                <!-- ícone discreto de dropdown -->
                <ChevronDownIcon class="w-3 h-3 text-gray-300" />
              </div>
            </MenuButton>
            <MenuItems class="absolute right-0 mt-2 w-48 bg-white text-black rounded shadow z-50">
              <MenuItem>
                <div @click="goProfile" class="p-2 hover:bg-orange-100 cursor-pointer">Meu perfil</div>
              </MenuItem>
              <MenuItem>
                <div @click="goWishlist" class="p-2 hover:bg-orange-100 cursor-pointer">Minha lista de desejos</div>
              </MenuItem>
              <MenuItem>
                <div @click="logout" class="p-2 hover:bg-orange-100 text-red-600 cursor-pointer">Sair</div>
              </MenuItem>
            </MenuItems>
          </Menu>

          <!-- DEVOLUÇÕES E PEDIDOS -->
          <div @click="goOrders" class="cursor-pointer text-right hover:text-orange-400">
            <span class="block text-xs text-gray-300">Devoluções</span>
            <span class="font-bold text-sm text-orange-500">e Pedidos</span>
          </div>

          <!-- CARRINHO -->
          <div class="relative cursor-pointer flex items-center gap-2" @click="goToCart">
            <div class="relative">
              <ShoppingCartIcon class="w-8 h-8 text-white" />
              <span class="absolute -top-2 -right-2 bg-orange-500 text-black rounded-full px-2 text-xs font-bold">{{ cartCount }}</span>
            </div>
            <span class="hidden md:block font-bold text-white text-sm">Carrinho</span>
          </div>

        </div>
      </div>

      <!-- MENU SECUNDÁRIO -->
      <nav class="bg-gray-900 text-gray-300 text-sm px-6 md:px-8 py-2 flex gap-6">
        <div class="relative group cursor-pointer">
          <span class="hover:text-orange-400">Eletrônicos</span>
          <div class="absolute left-0 mt-2 w-48 bg-white text-black rounded shadow-lg p-2 opacity-0 group-hover:opacity-100 transition">
            <a href="#" class="block px-2 py-1 hover:bg-orange-100 rounded">Smartphones</a>
            <a href="#" class="block px-2 py-1 hover:bg-orange-100 rounded">Notebooks</a>
            <a href="#" class="block px-2 py-1 hover:bg-orange-100 rounded">TVs</a>
          </div>
        </div>

        <div class="relative group cursor-pointer">
          <span class="hover:text-orange-400">Tecnologia</span>
          <div class="absolute left-0 mt-2 w-48 bg-white text-black rounded shadow-lg p-2 opacity-0 group-hover:opacity-100 transition">
            <a href="#" class="block px-2 py-1 hover:bg-orange-100 rounded">Audio</a>
            <a href="#" class="block px-2 py-1 hover:bg-orange-100 rounded">Câmeras</a>
            <a href="#" class="block px-2 py-1 hover:bg-orange-100 rounded">Acessórios</a>
          </div>
        </div>

        <span class="hover:text-orange-400 cursor-pointer">Casa</span>
        <span class="hover:text-orange-400 cursor-pointer">Jogos</span>
        <span class="hover:text-orange-400 cursor-pointer">Moda</span>
        <span class="hover:text-orange-400 cursor-pointer">Ofertas</span>
      </nav>
    </header>

    <!-- ==================== MAIN ==================== -->
    <main class="space-y-12">
      <!-- Conteúdo permanece igual -->
    </main>
  </div>
</template>

<script setup>
import SearchBar from "@/components/SearchBar.vue"
import { Menu, MenuButton, MenuItems, MenuItem } from "@headlessui/vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

// ícones Heroicons
import { ShoppingCartIcon, ChevronDownIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = authStore.isAuthenticated
const userName = authStore.user?.name || ""
const cartCount = 0

const goHome = () => router.push("/welcome")
const goToLogin = () => router.push("/login")
const goProfile = () => router.push("/profile")
const goWishlist = () => router.push("/wishlist")
const goOrders = () => router.push("/orders")
const logout = () => authStore.logout()
const goToCart = () => router.push("/cart")
</script>

<style scoped>
/* Tailwind já cuida da maior parte, hover e group usados */
</style>
