<template>
  <div>
    <!-- Mobile Sidebar -->
    <TransitionRoot as="template" :show="sidebarOpen">
      <Dialog class="relative z-50 lg:hidden" @close="sidebarOpen = false">
        <TransitionChild
          as="template"
          enter="transition-opacity ease-linear duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="transition-opacity ease-linear duration-300"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black/70" />
        </TransitionChild>
        <div class="fixed inset-0 flex">
          <TransitionChild
            as="template"
            enter="transition ease-in-out duration-300 transform"
            enter-from="-translate-x-full"
            enter-to="translate-x-0"
            leave="transition ease-in-out duration-300 transform"
            leave-from="translate-x-0"
            leave-to="-translate-x-full"
          >
            <DialogPanel class="relative mr-16 flex w-full max-w-xs flex-1">
              <TransitionChild
                as="template"
                enter="ease-in-out duration-300"
                enter-from="opacity-0"
                enter-to="opacity-100"
                leave="ease-in-out duration-300"
                leave-from="opacity-100"
                leave-to="opacity-0"
              >
                <div class="absolute left-full top-0 flex w-16 justify-center pt-5">
                  <button type="button" class="-m-2.5 p-2.5" @click="sidebarOpen = false">
                    <span class="sr-only">Close sidebar</span>
                    <XMarkIcon class="h-6 w-6 text-white" />
                  </button>
                </div>
              </TransitionChild>

              <!-- Sidebar -->
              <div class="flex grow flex-col gap-y-5 overflow-y-auto bg-black px-6 pb-4">
                <div class="flex h-16 shrink-0 items-center gap-2">
                  <img class="h-8 w-8 rounded" :src="defaultLogo" alt="Logo" />
                  <span class="text-orange-500 font-bold">RENITECH</span>
                </div>
                <MenuSidebar />
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </Dialog>
    </TransitionRoot>

    <!-- Desktop Sidebar -->
    <div class="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-72 lg:flex-col">
      <div class="flex grow flex-col gap-y-5 overflow-y-auto bg-black px-6 pb-4">
        <div class="flex h-16 shrink-0 items-center gap-2">
          <img class="h-8 w-8 rounded" :src="defaultLogo" alt="Logo" />
          <span class="text-orange-500 font-bold">RENITECH</span>
        </div>
        <MenuSidebar />
      </div>
    </div>

    <!-- Main -->
    <div class="lg:pl-72">
      <!-- Top bar -->
      <div
        class="sticky top-0 z-40 flex h-16 items-center gap-x-4 bg-black px-4 shadow sm:gap-x-6 lg:px-8"
      >
        <button
          type="button"
          class="-m-2.5 p-2.5 text-orange-500 lg:hidden"
          @click="sidebarOpen = true"
        >
          <Bars3Icon class="h-6 w-6" />
        </button>

        <div class="flex flex-1 gap-x-4 items-center lg:gap-x-6">
          <!-- Search -->
          <div class="flex flex-1">
            <div class="relative w-full">
              <MagnifyingGlassIcon class="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
              <input
                type="search"
                placeholder="Buscar produtos..."
                class="w-full rounded-md border border-gray-700 bg-white pl-10 pr-4 py-2 text-sm outline-none focus:border-orange-500"
              />
            </div>
          </div>

          <div class="flex items-center gap-x-6">
            <!-- Notifications -->
            <button type="button" class="text-orange-500 hover:text-orange-400">
              <BellIcon class="h-6 w-6" />
            </button>

            <!-- ========================= -->
            <!-- AMAZON STYLE ACCOUNT -->
            <!-- ========================= -->
            <Menu as="div" class="relative">
              <MenuButton class="flex flex-col items-start leading-tight hover:opacity-90">
                <span class="text-xs text-gray-300">
                  {{ isAuthenticated ? `Olá, ${userName}` : "Olá, faça seu login" }}
                </span>
                <span class="text-sm font-semibold text-orange-500">
                  {{ isAuthenticated ? "Sua conta" : "Contas e Listas" }}
                </span>
              </MenuButton>

              <MenuItems
                class="absolute right-0 mt-2 w-44 rounded-md bg-white py-2 shadow-lg ring-1 ring-black/10"
              >
                <!-- NÃO LOGADO -->
                <template v-if="!isAuthenticated">
                  <MenuItem>
                    <a
                      href="/login"
                      class="block px-4 py-2 text-sm text-gray-900 hover:bg-orange-50"
                    >
                      Entrar
                    </a>
                  </MenuItem>
                  <MenuItem>
                    <a
                      href="/register"
                      class="block px-4 py-2 text-sm text-gray-900 hover:bg-orange-50"
                    >
                      Criar conta
                    </a>
                  </MenuItem>
                </template>

                <!-- LOGADO -->
                <template v-else>
                  <MenuItem>
                    <a
                      href="/profile"
                      class="block px-4 py-2 text-sm text-gray-900 hover:bg-orange-50"
                    >
                      Minha conta
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
                </template>
              </MenuItems>
            </Menu>
          </div>
        </div>
      </div>

      <!-- Page -->
      <main class="py-10 bg-gray-50 min-h-screen">
        <div class="px-4 sm:px-6 lg:px-8">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { useAuthStore } from "@/stores/auth"

import MenuSidebar from "@/components/MenuSidebar.vue"
import defaultLogo from "@/assets/img/Logo_renitech.jpg"

import {
  Dialog, DialogPanel, Menu, MenuButton, MenuItem, MenuItems,
  TransitionChild, TransitionRoot,
} from "@headlessui/vue"

import {
  Bars3Icon, BellIcon, XMarkIcon,
} from "@heroicons/vue/24/outline"

import { MagnifyingGlassIcon } from "@heroicons/vue/20/solid"

const sidebarOpen = ref(false)

const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const userName = computed(() => authStore.user?.name || "")

function logout() {
  authStore.logout()
}
</script>
