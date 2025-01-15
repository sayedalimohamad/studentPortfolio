<template>
  <v-container class="py-12">
    <v-row class="justify-center">
      <v-col cols="12" md="6">
        <v-card class="px-6 py-8 elevation-12">
          <h1 class="text-3xl font-bold mb-6 text-center">Login</h1>
          <v-form @submit.prevent="login" ref="form">
            <v-text-field v-model="email" label="Email" type="email" :rules="[
              (v) => !!v || 'Email is required',
              (v) => /.+@.+\..+/.test(v) || 'Email must be valid'
            ]" required outlined dense></v-text-field>

            <v-text-field v-model="password" label="Password" :type="showPassword ? 'text' : 'password'"
              :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="[(v) => !!v || 'Password is required']" required outlined dense
              @click:append-inner="showPassword = !showPassword"></v-text-field>

            <v-btn type="submit" color="primary" block large class="my-4">Login</v-btn>
            <div class="d-block mb-2 text-muted py-4 text-center">
              Don't have an account?
              <a href="/register" class="text-decoration-none text-primary font-weight-bold">
                Register Now
              </a>
            </div>

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
        // Step 1: Login
        const response = await axios.post('/api/users/login', {
          email: this.email,
          password: this.password,
        });

        console.log('Login response:', response.data);

        // Store token and user role in localStorage
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('userRole', response.data.role);
        localStorage.setItem('isAuthenticated', true); // Set authentication state

        // Step 2: Show success message
        this.toast.success('Login successful!');

        // Step 3: Fetch user profile
        const userResponse = await axios.get('/api/users/me', {
          headers: { Authorization: `Bearer ${response.data.access_token}` },
        });

        console.log('User profile response:', userResponse.data);
        const user = userResponse.data;

        // Store the user ID after fetching the profile
        localStorage.setItem('userId', user.user_id);

        // Step 4: Redirect the user
        this.$router
          .push({
            name: 'UserProfile',
            params: { role: user.role, id: user.user_id },
          }).then(() => {
            location.reload();
          })
          .catch((err) => {
            console.error('Router push error:', err);
            this.$router.push('/'); // Fallback to home page if redirection fails
          });
      } catch (error) {
        console.error('Error during login:', error);
        this.errorMessage = 'Invalid email or password. Please try again.';
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
