<template>
  <v-container class="py-12">
    <v-row class="justify-center">
      <v-col cols="12" md="6">
        <v-card class="px-6 py-8">
          <h1 class="text-3xl font-bold mb-6 text-center">Login</h1>
          <v-form @submit.prevent="login" ref="form">
            <v-text-field
              v-model="email"
              label="Email"
              type="email"
              :rules="[
                (v) => !!v || 'Email is required',
                (v) => /.+@.+\..+/.test(v) || 'Email must be valid',
              ]"
              required
              outlined
            ></v-text-field>

            <v-text-field
              v-model="password"
              label="Password"
              :type="showPassword ? 'text' : 'password'"
              :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="[(v) => !!v || 'Password is required']"
              required
              outlined
              @click:append-inner="showPassword = !showPassword"
            ></v-text-field>

            <v-btn type="submit" color="primary" block large>Login</v-btn>

            <v-alert v-if="errorMessage" type="error" class="mt-4">{{ errorMessage }}</v-alert>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      errorMessage: '',
      showPassword: false,
    };
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  methods: {
    async login() {
  this.errorMessage = '';
  try {
    console.log('Sending login request with:', {
      email: this.email,
      password: this.password,
    });

    // Step 1: Login
    const response = await axios.post('/api/users/login', {
      email: this.email,
      password: this.password,
    });

    console.log('Login response:', response.data);
    localStorage.setItem('token', response.data.access_token);

    // Step 2: Show success message
    this.toast.success('Login successful!');

    // Step 3: Fetch user profile
    console.log('Fetching user profile...');
    const userResponse = await axios.get('/api/users/me', {
      headers: { Authorization: `Bearer ${response.data.access_token}` },
    });

    console.log('User profile response:', userResponse.data);
    const user = userResponse.data;

    // Step 4: Redirect the user
    console.log('Redirecting to user profile...');
    console.log('Route name:', 'UserProfile');
    console.log('Route params:', { role: String(user.role), id: String(user.user_id) });

    this.$router.push({
      name: 'UserProfile',
      params: { role: String(user.role), id: String(user.user_id) },
    }).catch(err => {
      console.error('Router push error:', err);
    });
  } catch (error) {
    console.error('Error during login:', error);

    if (error.response) {
      console.error('Server Error:', error.response.data);
      if (error.response.status === 401) {
        this.errorMessage = 'Invalid email or password. Please try again.';
      } else if (error.response.status === 500) {
        this.errorMessage = 'Server error. Please try again later.';
      } else {
        this.errorMessage = 'An error occurred. Please try again later.';
      }
    } else if (error.request) {
      console.error('Network Error:', error.request);
      this.errorMessage = 'Network error. Please check your connection.';
    } else {
      console.error('Error:', error.message);
      this.errorMessage = 'An unexpected error occurred.';
    }

    // Show error message
    this.toast.error(this.errorMessage);
  }
},
  },
};
</script>

<style scoped>
.error {
  color: red;
}
</style>