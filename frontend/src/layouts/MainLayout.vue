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
          <div class="fixed inset-0 bg-gray-900/80" />
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
              <div class="flex grow flex-col gap-y-5 overflow-y-auto bg-gray-900 px-6 pb-4">
                <div class="flex h-16 shrink-0 items-center">
                  <img class="h-8 w-8 rounded-full" :src="defaultLogo" alt="Logo" />
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
      <div class="flex grow flex-col gap-y-5 overflow-y-auto bg-gray-900 px-6 pb-4">
        <div class="flex h-16 shrink-0 items-center">
          <img class="h-8 w-8 rounded-full" :src="defaultLogo" alt="Logo" />
        </div>
        <MenuSidebar />
      </div>
    </div>

    <!-- Main -->
    <div class="lg:pl-72">
      <!-- Top bar -->
      <div
        class="sticky top-0 z-40 flex h-16 items-center gap-x-4 border-b bg-white px-4 shadow-sm sm:gap-x-6 lg:px-8"
      >
        <button
          type="button"
          class="-m-2.5 p-2.5 text-gray-700 lg:hidden"
          @click="sidebarOpen = true"
        >
          <Bars3Icon class="h-6 w-6" />
        </button>

        <div class="flex flex-1 gap-x-4 items-center lg:gap-x-6">
          <form class="grid flex-1 grid-cols-1">
            <input
              type="search"
              placeholder="Search"
              class="block w-full pl-8 text-gray-900 outline-none"
            />
            <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
          </form>

          <div class="flex items-center gap-x-4 lg:gap-x-6">
            <button type="button" class="-m-2.5 p-2.5 text-gray-400 hover:text-gray-500">
              <BellIcon class="h-6 w-6" />
            </button>

            <!-- User -->
            <Menu as="div" class="relative">
              <MenuButton class="-m-1.5 flex items-center p-1.5">
                <img class="h-8 w-8 rounded-full" :src="userAvatar" />
                <span class="ml-4 text-sm font-semibold text-gray-900">
                  {{ userName }}
                </span>
              </MenuButton>

              <MenuItems
                class="absolute right-0 mt-2 w-32 rounded-md bg-white py-2 shadow-lg ring-1 ring-gray-900/5"
              >
                <MenuItem>
                  <a href="/profile" class="block px-3 py-1 text-sm text-gray-900">Profile</a>
                </MenuItem>
                <MenuItem>
                  <a href="#" @click.prevent="logout" class="block px-3 py-1 text-sm text-red-600">
                    Logout
                  </a>
                </MenuItem>
              </MenuItems>
            </Menu>

            <button @click="logout" class="text-gray-400 hover:text-gray-500">
              <ArrowRightOnRectangleIcon class="h-6 w-6" />
            </button>
          </div>
        </div>
      </div>

      <!-- Page -->
      <main class="py-10">
        <div class="px-4 sm:px-6 lg:px-8">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import MenuSidebar from "@/components/MenuSidebar.vue"
import defaultLogo from "@/assets/img/logo.png"

import {
  Dialog, DialogPanel, Menu, MenuButton, MenuItem, MenuItems,
  TransitionChild, TransitionRoot,
} from "@headlessui/vue"

import {
  Bars3Icon, BellIcon, XMarkIcon, ArrowRightOnRectangleIcon,
} from "@heroicons/vue/24/outline"

import { MagnifyingGlassIcon } from "@heroicons/vue/20/solid"

const sidebarOpen = ref(false)

const API_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"

const defaultAvatar = "https://via.placeholder.com/150?text=User"
const userName = ref("Guest")
const userAvatar = ref(defaultAvatar)

// 🔹 Função para carregar usuário do localStorage
const loadUser = () => {
  const user = localStorage.getItem("user")
  if (user) {
    const parsed = JSON.parse(user)
    userName.value = parsed.name
    userAvatar.value = parsed.avatar
      ? API_URL + parsed.avatar
      : defaultAvatar
  }
}

onMounted(() => {
  loadUser()
  // 🔹 Escuta atualizações de localStorage (avatar atualizado)
  window.addEventListener("storage", (event) => {
    if (event.key === "user") {
      loadUser()
    }
  })
})

// Logout
function logout() {
  localStorage.removeItem("token")
  localStorage.removeItem("user")
  window.location.href = "/login"
}
</script>
