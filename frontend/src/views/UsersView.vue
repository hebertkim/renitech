<script setup>
import { onMounted, ref } from "vue";
import { userService } from "@/services/userService";

const users = ref([]);

onMounted(async () => {
  const { data } = await userService.list();
  users.value = data;
});
</script>
