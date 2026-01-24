<template>
  <dl class="mt-10 space-y-1 divide-y divide-gray-900/10">
    <Disclosure
      as="div"
      v-for="(item, index) in navigation"
      :key="item.name"
      class="pt-3"
    >
      <dt>
        <DisclosureButton
          class="flex w-full items-start justify-between text-left text-white group"
          @click="toggleMenu(index)"
        >
          <div class="flex items-center gap-x-3">
            <component
              :is="item.icon"
              class="size-6 shrink-0 text-white group-hover:text-indigo-400"
            />
            <span class="text-base font-semibold">
              {{ item.name }}
            </span>
          </div>
        </DisclosureButton>
      </dt>

      <DisclosurePanel v-show="activeIndex === index" as="dd" class="mt-2 pl-9">
        <ul class="space-y-2">
          <li
            v-for="submenu in item.submenu"
            :key="submenu.name"
            class="text-sm text-white hover:text-indigo-400"
          >
            <RouterLink :to="submenu.href">{{ submenu.name }}</RouterLink>
          </li>
        </ul>
      </DisclosurePanel>
    </Disclosure>
  </dl>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@headlessui/vue";
import {
  HomeIcon,
  ShoppingBagIcon,
  ClipboardDocumentListIcon,
  UsersIcon,
  Cog6ToothIcon,
  CreditCardIcon,
} from "@heroicons/vue/24/outline";

// MENU RENITECH (LIMPO)
const navigation = [
  {
    name: "Dashboard",
    icon: HomeIcon,
    submenu: [
      { name: "Visão Geral", href: "/dashboard" },
    ],
  },

  {
    name: "Catálogo",
    icon: ShoppingBagIcon,
    submenu: [
      { name: "Produtos", href: "/products" },
      { name: "Categorias", href: "/categories" },
    ],
  },

  {
    name: "Pedidos",
    icon: ClipboardDocumentListIcon,
    submenu: [
      { name: "Lista de Pedidos", href: "/orders" },
    ],
  },

  {
    name: "Clientes",
    icon: UsersIcon,
    submenu: [
      { name: "Clientes", href: "/customers" },
    ],
  },

  {
    name: "Loja",
    icon: Cog6ToothIcon,
    submenu: [
      { name: "Configurações", href: "/store-settings" },
      { name: "Banners", href: "/banners" },
      { name: "Domínio", href: "/domain" },
    ],
  },

  {
    name: "Assinatura",
    icon: CreditCardIcon,
    submenu: [
      { name: "Meu Plano", href: "/subscription" },
      { name: "Faturas", href: "/invoices" },
    ],
  },
];

const activeIndex = ref(null);

const toggleMenu = (index) => {
  activeIndex.value = activeIndex.value === index ? null : index;
};
</script>
