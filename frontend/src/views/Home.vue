<template>
  <div class="home">
    <router-link :to="{ name: 'start' }">Start</router-link>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Home',
});
</script>
