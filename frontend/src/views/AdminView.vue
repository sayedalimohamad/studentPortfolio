<template>
  <v-container class="py-12">
    <h1 class="text-3xl font-bold mb-6">Admins</h1>
    <v-card v-if="admins.length > 0">
      <v-list>
        <v-list-item v-for="admin in admins" :key="admin.admin_id" class="hover:bg-gray-50">
          <v-list-item-content>
            <v-list-item-title class="text-lg font-semibold">
              {{ admin.role }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-gray-600">
              Permissions: {{ admin.permissions }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card>
    <v-alert v-else type="info" class="mt-6">
      No admins found.
    </v-alert>
  </v-container>
</template>

<script>
export default {
  name: 'AdminView',
  data() {
    return {
      admins: [],
    };
  },
  async created() {
    try {
      const response = await this.$axios.get('/api/admins'); // Use global Axios
      this.admins = response.data;
    } catch (error) {
      console.error('Error fetching admins:', error);
    }
  },
};
</script>

<style scoped>
/* Add custom Tailwind classes or styles here */
</style>