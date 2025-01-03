<template>
  <v-container class="py-12">
    <v-row class="justify-center">
      <v-col cols="12" md="6">
        <v-card class="px-6 py-8">
          <h1 class="text-3xl font-bold mb-6 text-center">Register</h1>
          <v-form @submit.prevent="register" ref="form">
            <v-text-field
              v-model="username"
              label="Username"
              :rules="[(v) => !!v || 'Username is required']"
              required
              outlined
            ></v-text-field>
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
              type="password"
              :rules="[
                (v) => !!v || 'Password is required',
                (v) => v.length >= 8 || 'Password must be at least 8 characters',
              ]"
              required
              outlined
            ></v-text-field>
            <v-select
              v-model="role"
              :items="roles"
              label="Role"
              :rules="[(v) => !!v || 'Role is required']"
              required
              outlined
            ></v-select>
            <v-btn type="submit" color="primary" block large>Register</v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'RegisterView',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      role: 'student', // Default role
      roles: ['student', 'admin', 'supervisor'], // Available roles
    };
  },
  methods: {
    async register() {
      if (this.$refs.form.validate()) {
        try {
          const response = await this.$axios.post('/api/users/register', { // Use global Axios
            username: this.username,
            email: this.email,
            password: this.password,
            role: this.role,
          });
          alert('Registration successful!');
          this.$router.push('/login'); // Redirect to login page
        } catch (error) {
          alert('Registration failed. Please try again.');
          console.error(error);
        }
      }
    },
  },
};
</script>

<style scoped>
/* Add custom Tailwind classes or styles here */
</style>