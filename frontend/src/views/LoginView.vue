<template>
  <v-container class="py-12">
    <v-row class="justify-center">
      <v-col cols="12" md="6">
        <v-card class="px-6 py-8">
          <h1 class="text-3xl font-bold mb-6 text-center">Login</h1>
          <v-form @submit.prevent="login">
            <v-text-field v-model="email" label="Email" required outlined></v-text-field>
            <v-text-field v-model="password" label="Password" type="password" required outlined></v-text-field>
            <v-btn type="submit" color="primary" block large>Login</v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await this.$axios.post('/api/users/login', { // Use global Axios
          email: this.email,
          password: this.password,
        });
        localStorage.setItem('token', response.data.access_token);
        this.$router.push('/');
      } catch (error) {
        alert('Invalid credentials');
      }
    },
  },
};
</script>

<style scoped>
/* Add custom Tailwind classes or styles here */
</style>