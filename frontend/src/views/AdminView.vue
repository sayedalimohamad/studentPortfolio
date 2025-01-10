<template>
  <v-container class="py-12">
    <h1 class="text-3xl font-bold mb-6 word-color">Admins List</h1>
    <v-card v-if="admins.length > 0">
      <v-list>
        <v-list-item v-for="admin in admins" :key="admin.admin_id" class="hover:bg-gray-50">
          <v-list-item-content>
            <v-list-item-title class="text-lg font-bold word-color">
              {{ admin.user.username }} ({{ admin.role }})
            </v-list-item-title>
            <v-list-item-subtitle class="text-gray-600">
              Email: <span class="word-color">{{ admin.user.email }}</span>
            </v-list-item-subtitle>
            <v-list-item-subtitle class="text-gray-600">
              Permissions: <span class="word-color">{{ JSON.stringify(admin.permissions) }}</span>
            </v-list-item-subtitle>
            <v-list-item-subtitle class="text-gray-600">
              Created By: <span class="word-color">{{ admin.created_by }}</span>
            </v-list-item-subtitle>
            <v-list-item-subtitle class="text-gray-600">
              Status: <span class="word-color">{{ admin.user.status }}</span>
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
import axios from 'axios';

export default {
  name: 'AdminView',
  data() {
    return {
      admins: [],
    };
  },
  async created() {
    try {
      const response = await axios.get('/api/admins');
      this.admins = response.data;
    } catch (error) {
      console.error('Error fetching admins:', error);
    }
  },
};
</script>

<style scoped>
.word-color {
  color: #0097A7; /* Custom color for highlighted text */
}
</style>