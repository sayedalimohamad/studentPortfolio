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
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-icon>
                <v-icon color="primary">mdi-calendar</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title class="font-bold">Date of Birth</v-list-item-title>
                <v-list-item-subtitle class="text-gray-700">{{ new Date(user.dob).toDateString()  }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-icon>
                <v-icon color="primary">mdi-account-circle</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title class="font-bold">Username</v-list-item-title>
                <v-list-item-subtitle class="text-gray-700">{{ user.username }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
        </v-row>
        <!-- Student Specific Information -->
        <v-row v-if="userRole === 'student' && studentInfo">
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-icon>
                <v-icon color="primary">mdi-school</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title class="font-bold">Institution</v-list-item-title>
                <v-list-item-subtitle class="text-gray-700">{{ studentInfo.institution }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-icon>
                <v-icon color="primary">mdi-book</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title class="font-bold">Major</v-list-item-title>
                <v-list-item-subtitle class="text-gray-700">{{ studentInfo.major }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
        </v-row>
        <!-- Supervisor Specific Information -->
        <v-row v-if="userRole === 'supervisor' && supervisorInfo">
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-icon>
                <v-icon color="primary">mdi-office-building</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title class="font-bold">Institution</v-list-item-title>
                <v-list-item-subtitle class="text-gray-700">{{ supervisorInfo.institution }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-icon>
                <v-icon color="primary">mdi-domain</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title class="font-bold">Department</v-list-item-title>
                <v-list-item-subtitle class="text-gray-700">{{ supervisorInfo.department }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
        </v-row>
        <!-- Admin Specific Information -->
        <v-row v-if="userRole === 'admin' && adminInfo">
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-icon>
                <v-icon color="primary">mdi-shield-account</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title class="font-bold">Permissions</v-list-item-title>
                <v-list-item-subtitle class="text-gray-700">{{ adminInfo.permissions }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-icon>
                <v-icon color="primary">mdi-account-multiple</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title class="font-bold">Role</v-list-item-title>
                <v-list-item-subtitle class="text-gray-700">{{ adminInfo.role }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
        </v-row>
        <!-- Delete Account Button -->
        <v-row>
          <v-col cols="12" class="text-right">
            <v-btn color="red" dark @click="showDeleteModal = true">
              <v-icon left>mdi-delete</v-icon>
              Delete Account
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <v-alert v-if="loading" type="info" class="mt-6">Loading...</v-alert>
    <v-alert v-if="error" type="error" class="mt-6">{{ error }}</v-alert>
    <!-- Delete Confirmation Modal -->
    <v-dialog v-model="showDeleteModal" max-width="500">
      <v-card>
        <v-card-title class="headline">
          <v-icon color="red" left>mdi-alert-circle</v-icon>
          Confirm Account Deletion
        </v-card-title>
        <v-card-text>
          <p>Please enter your password to confirm account deletion:</p>
          <v-text-field v-model="password" :type="showPassword ? 'text' : 'password'" label="Password" required outlined
            dense :rules="[(v) => !!v || 'Password is required']"
            append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="showPassword = !showPassword"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="showDeleteModal = false">
            <v-icon left>mdi-cancel</v-icon>
            Cancel
          </v-btn>
          <v-btn color="red darken-1" text @click="confirmDeleteAccount">
            <v-icon left>mdi-delete</v-icon>
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';
export default {
  name: 'UserProfileView',
  data() {
    return {
      user: null,
      studentInfo: null,
      supervisorInfo: null,
      adminInfo: null,
      loading: true,
      error: null,
      userRole: null,
      showDeleteModal: false,
      password: '',
      showPassword: false,
    };
  },
  async created() {
    const { role, id } = this.$route.params; // Ensure these match the route params
    const storedAuth = localStorage.getItem('token');
    // Redirect to login if not authenticated
    if (!storedAuth) {
      this.$router.push('/login');
      return;
    }
    this.userRole = role;
    try {
      // Fetch user details from the backend
      const userResponse = await axios.get(`/api/users/${id}`, {
        headers: {
          Authorization: `Bearer ${storedAuth}`,
        },
      });
      this.user = userResponse.data;
      // Fetch role-specific information
      if (role === 'student') {
        const studentResponse = await axios.get(`/api/students/${id}`, {
          headers: {
            Authorization: `Bearer ${storedAuth}`,
          },
        });
        this.studentInfo = studentResponse.data;
      } else if (role === 'supervisor') {
        const supervisorResponse = await axios.get(`/api/supervisors/${id}`, {
          headers: {
            Authorization: `Bearer ${storedAuth}`,
          },
        });
        this.supervisorInfo = supervisorResponse.data;
      } else if (role === 'admin') {
        const adminResponse = await axios.get(`/api/admins/${id}`, {
          headers: {
            Authorization: `Bearer ${storedAuth}`,
          },
        });
        this.adminInfo = adminResponse.data;
      }
    } catch (error) {
      console.error(`Error fetching ${role} data:`, error);
      this.error = `Failed to load ${role} data.`;
      useToast().error(this.error);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async confirmDeleteAccount() {
      const { id } = this.$route.params;
      const storedAuth = localStorage.getItem('token');
      if (!this.password) {
        this.error = 'Please enter your password.';
        useToast().error(this.error);
        return;
      }
      try {
        // Step 1: Verify the password
        const verifyResponse = await axios.post('/api/users/verify-password', {
          password: this.password,
        }, {
          headers: {
            Authorization: `Bearer ${storedAuth}`,
          },
        });
        if (!verifyResponse.data.isValid) {
          this.error = 'Incorrect password. Please try again.';
          useToast().error(this.error);
          return;
        }
        // Step 2: Delete the account
        await axios.delete(`/api/users/${id}`, {
          headers: {
            Authorization: `Bearer ${storedAuth}`,
          },
          data: {
            password: this.password,
          },
        });
        // Step 3: Force logout
        localStorage.removeItem('token'); // Clear the token
        this.$router.push('/login'); // Redirect to login page
        location.reload(); // Reload the page
        useToast().success('Account deleted successfully.');
      } catch (error) {
        console.error('Error deleting account:', error);
        this.error = 'Failed to delete account. Please try again.';
        useToast().error(this.error);
      } finally {
        this.showDeleteModal = false;
      }
    },
  },
};
</script>
<style scoped>
.word-color {
  color: #0097a7;
}
</style>