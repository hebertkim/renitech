<template>
  <transition name="fade">
    <div
      v-if="modelValue"
      class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
    >
      <div
        class="bg-white rounded-xl shadow-lg w-full max-w-md p-6 relative transform transition-transform duration-300 scale-95"
        @click.stop
      >
        <!-- Header -->
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-700">
            <slot name="title">{{ title }}</slot>
          </h2>
          <button
            @click="close"
            class="text-gray-500 hover:text-gray-900 text-lg font-bold"
          >
            ✕
          </button>
        </div>

        <!-- Body -->
        <div class="mb-4">
          <slot name="body"></slot>
        </div>

        <!-- Footer -->
        <div class="flex justify-end gap-2">
          <slot name="footer">
            <button
              @click="close"
              class="bg-gray-300 px-4 py-2 rounded hover:bg-gray-400 transition"
            >
              Cancelar
            </button>
            <button
              @click="$emit('save')"
              class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
            >
              Salvar
            </button>
          </slot>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
const props = defineProps({
  modelValue: { type: Boolean, default: false },
  title: { type: String, default: "Modal" },
});

const emit = defineEmits(["update:modelValue", "save"]);

const close = () => emit("update:modelValue", false);
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
