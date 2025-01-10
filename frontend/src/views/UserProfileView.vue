<template>
  <v-container class="py-12">
    <v-row class="mb-6">
      <v-col cols="12" class="text-center">
        <h1 class="text-3xl font-bold word-color">{{ userRole }} Profile</h1>
        <p class="text-lg text-gray-700">Welcome to your personalized profile page.</p>
      </v-col>
    </v-row>

    <v-card v-if="user" class="mx-auto" max-width="800">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-icon>
                <v-icon color="primary">mdi-account</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title class="font-bold">Full Name</v-list-item-title>
                <v-list-item-subtitle class="text-gray-700">{{ user.full_name }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-icon>
                <v-icon color="primary">mdi-email</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title class="font-bold">Email</v-list-item-title>
                <v-list-item-subtitle class="text-gray-700">{{ user.email }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-alert v-if="loading" type="info" class="mt-6">Loading...</v-alert>
    <v-alert v-if="error" type="error" class="mt-6">{{ error }}</v-alert>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserProfileView',
  data() {
    return {
      user: null,
      loading: true,
      error: null,
      userRole: null,
    };
  },
  async created() {
  const storedRole = localStorage.getItem('userRole');
  const storedAuth = localStorage.getItem('access_token');

  // Redirect to login if not authenticated
  if (!storedRole || !storedAuth) {
    this.$router.push('/login');
    return;
  }

  const { role, id } = this.$route.params;
  const validRoles = ['student', 'admin', 'supervisor'];
  if (!validRoles.includes(role)) {
    this.error = 'Invalid user role.';
    this.loading = false;
    return;
  }

  this.userRole = role;

  try {
    // Fetch user details from the backend
    const response = await axios.get(`/api/users/${id}`, {
      headers: {
        Authorization: `Bearer ${storedAuth}`,
      },
    });
    this.user = response.data;
  } catch (error) {
    console.error(`Error fetching ${role} data:`, error);
    this.error = `Failed to load ${role} data.`;
  } finally {
    this.loading = false;
  }
}
};
</script>

<style scoped>
.word-color {
  color: #0097a7;
}
</style>