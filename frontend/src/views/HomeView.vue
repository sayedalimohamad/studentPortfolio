<template>
  <v-container class="py-12">
    <v-row class="text-center">
      <v-col cols="12">
        <h1 class="text-4xl font-bold mb-4">Welcome to the Student Portfolio</h1>
        <p class="text-lg text-gray-600">
          Manage and showcase student achievements, events, and more.
        </p>
      </v-col>
      <v-col cols="12" class="mt-8">
        <v-btn color="primary" to="/students" large>View Students</v-btn>
        <v-btn color="secondary" to="/admins" large class="ml-4">View Admins</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'HomeView',
};
</script>

<style scoped>
/* Add custom Tailwind classes or styles here */
</style>