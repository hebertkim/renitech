<template>
  <div class="min-h-screen bg-white">

    <!-- ==================== HEADER ==================== -->
    <header class="bg-black text-white w-full">
      <div class="flex items-center justify-between px-8 py-3 gap-4">

        <div class="text-2xl font-bold cursor-pointer select-none" @click="goHome">
          <span class="text-orange-500">Reni</span>tech
        </div>

        <div class="flex-1 hidden md:flex justify-center">
          <SearchBar />
        </div>

        <div class="flex items-center gap-5">

          <!-- Dropdown usuário -->
          <Menu as="div" class="relative" v-if="isAuthenticated">
            <MenuButton class="flex items-center gap-1 text-sm hover:text-orange-400">
              <span class="font-semibold text-orange-500">{{ userName }}</span>
              <svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </MenuButton>
            <MenuItems class="absolute right-0 mt-2 w-44 bg-white text-black rounded shadow">
              <MenuItem><div @click="goProfile" class="p-2 hover:bg-orange-100 cursor-pointer">Meu perfil</div></MenuItem>
              <MenuItem><div class="p-2 hover:bg-orange-100 cursor-pointer">Meus pedidos</div></MenuItem>
              <MenuItem><div @click="logout" class="p-2 hover:bg-orange-100 text-red-600 cursor-pointer">Sair</div></MenuItem>
            </MenuItems>
          </Menu>

          <div v-if="!isAuthenticated" class="cursor-pointer" @click="goToLogin">
            <span class="block text-sm">Olá, faça seu</span>
            <span class="font-bold text-lg text-orange-500">Login</span>
          </div>

          <div class="relative cursor-pointer" @click="goToCart">
            🛒
            <span class="absolute -top-2 -right-3 bg-orange-500 text-black text-xs font-bold rounded-full px-1.5">0</span>
          </div>

        </div>
      </div>

      <div class="bg-gray-900 text-gray-300 text-sm px-8 py-2 flex gap-6">
        <span class="hover:text-orange-400 cursor-pointer">Eletrônicos</span>
        <span class="hover:text-orange-400 cursor-pointer">Tecnologia</span>
        <span class="hover:text-orange-400 cursor-pointer">Casa</span>
        <span class="hover:text-orange-400 cursor-pointer">Jogos</span>
        <span class="hover:text-orange-400 cursor-pointer">Moda</span>
        <span class="hover:text-orange-400 cursor-pointer">Ofertas</span>
      </div>
    </header>

    <!-- ==================== MAIN ==================== -->
    <main class="space-y-12">

      <!-- HERO ROTATIVO -->
      <div class="relative h-96 overflow-hidden">
        <img src="https://via.placeholder.com/1400x450/FF7F50/ffffff?text=Tecnologia+em+destaque" class="absolute inset-0 w-full h-full object-cover"/>
        <img src="https://via.placeholder.com/1400x450/000000/ffffff?text=Novidades+Em+Eletr%C3%B4nicos" class="absolute inset-0 w-full h-full object-cover opacity-0"/>
      </div>

      <div class="max-w-7xl mx-auto px-6 space-y-10">

        <!-- CATEGORIAS EM DESTAQUE -->
        <section>
          <h2 class="text-3xl font-extrabold text-gray-800 mb-4">Categorias populares</h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6">
            <div v-for="cat in categories" :key="cat.name"
                 class="bg-white rounded-lg shadow hover:shadow-lg transition p-4 text-center cursor-pointer">
              <img :src="cat.icon" class="mx-auto mb-2 w-16 h-16"/>
              <p class="text-sm font-semibold text-gray-800">{{ cat.name }}</p>
            </div>
          </div>
        </section>

        <!-- OFERTAS FLASH -->
        <section>
          <h2 class="text-3xl font-extrabold text-gray-800 mb-4">Ofertas imperdíveis</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div v-for="offer in offers" :key="offer.title"
                 class="bg-orange-500 rounded-lg text-white p-6 hover:bg-orange-600 transition">
              <p class="font-bold text-lg">{{ offer.title }}</p>
              <p class="text-sm">{{ offer.desc }}</p>
            </div>
          </div>
        </section>

        <!-- PRODUTOS EM DESTAQUE -->
        <section>
          <h2 class="text-3xl font-extrabold text-gray-800 mb-4">Produtos em destaque</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div v-for="product in products" :key="product.name"
                 class="bg-white rounded-lg shadow hover:shadow-xl transition p-4">
              <img :src="product.image" class="w-full h-40 object-cover rounded-md mb-3"/>
              <h3 class="font-bold text-gray-900">{{ product.name }}</h3>
              <p class="text-sm text-gray-500">{{ product.description }}</p>
              <p class="text-xl font-bold text-orange-500 mt-2">{{ product.price }}</p>
              <button class="mt-3 w-full bg-black text-white py-2 rounded hover:bg-gray-800 transition">Ver detalhes</button>
            </div>
          </div>
        </section>

        <!-- MARCAS PARCEIRAS -->
        <section>
          <h2 class="text-3xl font-extrabold text-gray-800 mb-4">Marcas que amamos</h2>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-6 items-center">
            <img v-for="brand in brands" :key="brand" :src="brand"
                 class="h-16 object-contain mx-auto"/>
          </div>
        </section>

      </div>
    </main>
  </div>
</template>

<script setup>
import SearchBar from "@/components/SearchBar.vue"
import { Menu, MenuButton, MenuItems, MenuItem } from "@headlessui/vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = authStore.isAuthenticated
const userName = authStore.user?.name || ""

// Categorias fictícias
const categories = [
  { name: "Smartphones", icon: "https://via.placeholder.com/64?text=📱" },
  { name: "Notebooks", icon: "https://via.placeholder.com/64?text=💻" },
  { name: "TVs", icon: "https://via.placeholder.com/64?text=📺" },
  { name: "Audio", icon: "https://via.placeholder.com/64?text=🎧" },
  { name: "Promoções", icon: "https://via.placeholder.com/64?text=🔥" }
]

// Ofertas fictícias
const offers = [
  { title: "Smartphone 20% OFF", desc: "Só até acabar o estoque!" },
  { title: "Notebook com Frete Grátis", desc: "Aproveite agora" },
  { title: "Desconto em TVs 4K", desc: "Melhores preços do mês" }
]

// Produtos fictícios
const products = [
  { name: "Smartphone X", description: "Tela OLED 6.7\"", price: "R$ 2.499", image: "https://via.placeholder.com/300x200?text=Smartphone+X" },
  { name: "Notebook Pro", description: "16GB RAM | SSD 512GB", price: "R$ 4.299", image: "https://via.placeholder.com/300x200?text=Notebook+Pro" },
  { name: "TV 4K Ultra", description: "65\" UHD Smart", price: "R$ 3.199", image: "https://via.placeholder.com/300x200?text=TV+4K+Ultra" },
  { name: "Caixa Bluetooth", description: "Som Potente e Design", price: "R$ 399", image: "https://via.placeholder.com/300x200?text=Caixa+Bluetooth" }
]

// Marcas fictícias
const brands = [
  "https://via.placeholder.com/120x60?text=BrandA",
  "https://via.placeholder.com/120x60?text=BrandB",
  "https://via.placeholder.com/120x60?text=BrandC",
  "https://via.placeholder.com/120x60?text=BrandD",
  "https://via.placeholder.com/120x60?text=BrandE",
  "https://via.placeholder.com/120x60?text=BrandF"
]

const goHome = () => router.push("/welcome")
const goToLogin = () => router.push("/login")
const goProfile = () => router.push("/profile")
const logout = () => authStore.logout()
const goToCart = () => router.push("/cart")
</script>

<style scoped>
/* nada além do Tailwind necessário */
</style>
