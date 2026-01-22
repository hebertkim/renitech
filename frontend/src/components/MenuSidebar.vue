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
            <a :href="submenu.href">{{ submenu.name }}</a>
          </li>
        </ul>
      </DisclosurePanel>
    </Disclosure>
  </dl>
</template>

<script setup>
import { ref } from "vue";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
} from "@headlessui/vue";
import {
  HomeIcon,
  ServerIcon,
  MagnifyingGlassCircleIcon,
  ChartBarSquareIcon,
  DocumentChartBarIcon,
  WrenchScrewdriverIcon,
  Cog6ToothIcon,
  ClipboardDocumentListIcon,
  CurrencyDollarIcon,
  BuildingStorefrontIcon,
  ShieldCheckIcon,
  UserGroupIcon,
} from "@heroicons/vue/24/outline";

// MENU OFICIAL DO FINZIA
// MENU ATUALIZADO – SOMENTE VIEWS IMPLEMENTADAS
const navigation = [
  {
    name: "Dashboard",
    icon: HomeIcon,
    submenu: [
      { name: "Dashboard Geral", href: "/dashboard" },
    ],
  },

  {
    name: "Financeiro",
    icon: CurrencyDollarIcon,
    submenu: [
      { name: "Contas", href: "/accounts" },        // AccountsView.vue
      { name: "Despesas", href: "/expenses" },     // ExpensesView.vue
      { name: "Receitas", href: "/incomes" },      // IncomesView.vue
      { name: "Categorias", href: "/categories" }, // CategoriesView.vue
    ],
  },

  {
    name: "Perfil",
    icon: ShieldCheckIcon,
    submenu: [
      { name: "Configurações do Perfil", href: "/profile" }, // ProfileSettings.vue
    ],
  },

  {
    name: "Usuários",
    icon: UserGroupIcon,
    submenu: [
      { name: "Usuários", href: "/users" }, // UsersView.vue
    ],
  },
];


const activeIndex = ref(null);

const toggleMenu = (index) => {
  activeIndex.value = activeIndex.value === index ? null : index;
};
</script>
