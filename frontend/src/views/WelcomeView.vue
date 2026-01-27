<template>
  <div class="min-h-screen bg-gray-100">

    <!-- ==================== NAVBAR ==================== -->
    <NavbarView />

    <!-- ==================== HERO ==================== -->
    <section class="relative h-96 bg-gray-200 overflow-hidden">
      <img src="https://via.placeholder.com/1400x450/FF7F50/ffffff?text=Promoções+Imperdíveis"
           class="absolute inset-0 w-full h-full object-cover"/>
      <div class="absolute inset-0 bg-black bg-opacity-30 flex flex-col justify-center items-start px-6 md:px-20">
        <h1 class="text-4xl md:text-6xl font-extrabold text-white mb-4">Tecnologia em Destaque</h1>
        <p class="text-white text-lg md:text-2xl mb-6">Ofertas exclusivas para você!</p>
        <button class="bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 px-6 rounded transition">
          Ver Ofertas
        </button>
      </div>
    </section>

    <!-- ==================== CATEGORIAS ==================== -->
    <section class="max-w-7xl mx-auto px-6 md:px-8 mt-12">
      <h2 class="text-3xl font-extrabold text-gray-800 mb-6">Categorias Populares</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6">
        <div v-for="cat in categories" :key="cat.name"
             class="bg-white rounded-lg shadow hover:shadow-lg transition p-4 text-center cursor-pointer">
          <img :src="cat.icon" class="mx-auto mb-2 w-16 h-16"/>
          <p class="text-sm font-semibold text-gray-800">{{ cat.name }}</p>
        </div>
      </div>
    </section>

    <!-- ==================== OFERTAS FLASH ==================== -->
    <section class="max-w-7xl mx-auto px-6 md:px-8 mt-16">
      <h2 class="text-3xl font-extrabold text-gray-800 mb-6">Ofertas Imperdíveis</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="offer in offers" :key="offer.title"
             class="bg-orange-500 rounded-lg text-white p-6 hover:bg-orange-600 transition">
          <p class="font-bold text-lg">{{ offer.title }}</p>
          <p class="text-sm mt-2">{{ offer.desc }}</p>
        </div>
      </div>
    </section>

    <!-- ==================== PRODUTOS EM DESTAQUE ==================== -->
    <section class="max-w-7xl mx-auto px-6 md:px-8 mt-16">
      <h2 class="text-3xl font-extrabold text-gray-800 mb-6">Produtos em Destaque</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="product in products" :key="product.name"
             class="bg-white rounded-lg shadow hover:shadow-xl transition p-4 flex flex-col">
          <img :src="product.image" class="w-full h-48 object-cover rounded-md mb-3"/>
          <h3 class="font-bold text-gray-900 text-lg">{{ product.name }}</h3>
          <p class="text-sm text-gray-500 mt-1">{{ product.description }}</p>
          <p class="text-xl font-bold text-orange-500 mt-2">{{ product.price }}</p>
          <button class="mt-auto w-full bg-black text-white py-2 rounded hover:bg-gray-800 transition mt-3">
            Ver detalhes
          </button>
        </div>
      </div>
    </section>

    <!-- ==================== MARCAS PARCEIRAS ==================== -->
    <section class="max-w-7xl mx-auto px-6 md:px-8 mt-16 mb-20">
      <h2 class="text-3xl font-extrabold text-gray-800 mb-6">Marcas que amamos</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-6 items-center">
        <img v-for="brand in brands" :key="brand" :src="brand"
             class="h-16 object-contain mx-auto"/>
      </div>
    </section>

  </div>
</template>

<script setup>
import NavbarView from "@/components/NavbarView.vue"

const categories = [
  { name: "Smartphones", icon: "https://via.placeholder.com/64?text=📱" },
  { name: "Notebooks", icon: "https://via.placeholder.com/64?text=💻" },
  { name: "TVs", icon: "https://via.placeholder.com/64?text=📺" },
  { name: "Audio", icon: "https://via.placeholder.com/64?text=🎧" },
  { name: "Promoções", icon: "https://via.placeholder.com/64?text=🔥" }
]

const offers = [
  { title: "Smartphone 20% OFF", desc: "Só até acabar o estoque!" },
  { title: "Notebook com Frete Grátis", desc: "Aproveite agora" },
  { title: "Desconto em TVs 4K", desc: "Melhores preços do mês" }
]

const products = [
  { name: "Smartphone X", description: "Tela OLED 6.7\"", price: "R$ 2.499", image: "https://via.placeholder.com/300x200?text=Smartphone+X" },
  { name: "Notebook Pro", description: "16GB RAM | SSD 512GB", price: "R$ 4.299", image: "https://via.placeholder.com/300x200?text=Notebook+Pro" },
  { name: "TV 4K Ultra", description: "65\" UHD Smart", price: "R$ 3.199", image: "https://via.placeholder.com/300x200?text=TV+4K+Ultra" },
  { name: "Caixa Bluetooth", description: "Som Potente e Design", price: "R$ 399", image: "https://via.placeholder.com/300x200?text=Caixa+Bluetooth" }
]

const brands = [
  "https://via.placeholder.com/120x60?text=BrandA",
  "https://via.placeholder.com/120x60?text=BrandB",
  "https://via.placeholder.com/120x60?text=BrandC",
  "https://via.placeholder.com/120x60?text=BrandD",
  "https://via.placeholder.com/120x60?text=BrandE",
  "https://via.placeholder.com/120x60?text=BrandF"
]
</script>

<style scoped>
/* Se desejar, você pode adicionar efeitos adicionais de hover e animações */
</style>
