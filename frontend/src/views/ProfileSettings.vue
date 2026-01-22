<template>
  <MainLayout>
  <div class="max-w-3xl mx-auto py-10">
    <h1 class="text-2xl font-bold mb-6 text-gray-800">Profile Settings</h1>

    <div class="bg-white shadow-md rounded-lg p-6">
      <form @submit.prevent="saveProfile">
        <!-- Profile Image -->
        <div class="mb-6 flex items-center gap-4">
          <img
            :src="previewAvatar || user.avatarFull || defaultAvatar"
            alt="Profile"
            class="h-20 w-20 rounded-full object-cover border border-gray-300"
          />
          <div>
            <label class="cursor-pointer px-3 py-2 bg-gray-200 rounded-md hover:bg-gray-300 text-sm">
              Change Photo
              <input type="file" accept="image/*" @change="onFileChange" class="hidden" />
            </label>
            <button
              type="button"
              v-if="user.avatar || previewAvatar"
              @click="removeAvatar"
              class="ml-2 px-2 py-1 bg-red-500 text-white rounded-md text-sm hover:bg-red-600"
            >
              Remove
            </button>
          </div>
        </div>

        <!-- Name -->
        <div class="mb-4">
          <label class="block mb-1 font-medium text-gray-700">Name</label>
          <input
            type="text"
            v-model="user.name"
            class="w-full px-4 py-2 border border-gray-300 rounded-md"
            required
          />
        </div>

        <!-- Email -->
        <div class="mb-4">
          <label class="block mb-1 font-medium text-gray-700">Email</label>
          <input
            type="email"
            v-model="user.email"
            class="w-full px-4 py-2 border border-gray-300 rounded-md"
            required
          />
        </div>

        <!-- Password -->
        <div class="mb-4">
          <label class="block mb-1 font-medium text-gray-700">Password</label>
          <input
            type="password"
            v-model="password"
            class="w-full px-4 py-2 border border-gray-300 rounded-md"
            placeholder="Leave blank to keep current"
          />
        </div>

        <!-- Buttons -->
        <div class="flex justify-end gap-2">
          <button
            type="button"
            @click="cancelProfile"
            class="px-4 py-2 bg-gray-300 rounded-md"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-blue-600 rounded-md text-white"
          >
            Save Changes
          </button>
        </div>
      </form>
    </div>
  </div>
  </MainLayout>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import api from "@/services/api"
import MainLayout from "@/layouts/MainLayout.vue"

const router = useRouter()
const API_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"

const defaultAvatar = "https://via.placeholder.com/150?text=User"

const user = reactive({
  name: "",
  email: "",
  avatar: null,          // caminho do backend /assets/...
  avatarFull: null,      // caminho completo para mostrar na view
})

const password = ref("")
const previewAvatar = ref(null)
const selectedFile = ref(null)

// ============================
// Carregar perfil
// ============================
const loadProfile = async () => {
  const { data } = await api.get("/users/me")
  user.name = data.name
  user.email = data.email
  user.avatar = data.avatar
  user.avatarFull = data.avatar ? API_URL + data.avatar : null
}

onMounted(loadProfile)

// ============================
// Upload preview
// ============================
const onFileChange = (event) => {
  const file = event.target.files[0]
  if (!file) return

  selectedFile.value = file
  previewAvatar.value = URL.createObjectURL(file)
}

// ============================
// Remover avatar
// ============================
const removeAvatar = async () => {
  previewAvatar.value = null
  selectedFile.value = null
  user.avatar = null
  user.avatarFull = null

  await api.delete("/users/me/avatar")

  // Atualiza localStorage e dispara evento storage
  const stored = JSON.parse(localStorage.getItem("user"))
  stored.avatar = null
  localStorage.setItem("user", JSON.stringify(stored))
  window.dispatchEvent(new Event("storage"))
}

// ============================
// Salvar perfil
// ============================
const saveProfile = async () => {
  try {
    const payload = {
      name: user.name,
      email: user.email,
    }
    if (password.value) payload.password = password.value

    const { data: updated } = await api.put("/users/me", payload)

    // Upload avatar
    let avatarPath = updated.avatar
    if (selectedFile.value) {
      const form = new FormData()
      form.append("file", selectedFile.value)

      const { data } = await api.post("/users/me/avatar", form)
      avatarPath = data.avatar
      user.avatar = avatarPath
      user.avatarFull = API_URL + avatarPath
    }

    // Atualiza localStorage e dispara evento storage
    localStorage.setItem("user", JSON.stringify({
      ...updated,
      avatar: avatarPath
    }))
    window.dispatchEvent(new Event("storage"))

    alert("Profile updated successfully!")
    router.push("/dashboard")
  } catch (err) {
    console.error(err)
    alert("Erro ao salvar perfil")
  }
}

// ============================
// Cancelar
// ============================
const cancelProfile = () => {
  router.push("/dashboard")
}
</script>
