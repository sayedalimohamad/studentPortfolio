<template>
  <v-container class="py-12">
    <v-row class="justify-center">
      <v-col cols="12" md="6">
        <v-card class="px-6 py-8">
          <h1 class="text-3xl font-bold mb-6 text-center">Register</h1>
          <v-form @submit.prevent="register" ref="form">
            <v-text-field v-model="username" label="Username" :rules="[(v) => !!v || 'Username is required']" required
              outlined></v-text-field>
            <v-text-field v-model="email" label="Email" type="email" :rules="[
              (v) => !!v || 'Email is required',
              (v) => /.+@.+\..+/.test(v) || 'Email must be valid',
            ]" required outlined></v-text-field>
            <v-text-field v-model="password" label="Password" type="password" :rules="[
              (v) => !!v || 'Password is required',
              (v) => v.length >= 8 || 'Password must be at least 8 characters',
            ]" required outlined></v-text-field>

            <!-- Dynamic Row for Role and Code Input -->
            <v-row>
              <!-- Role Selection -->
              <v-col :cols="rolesUnlocked ? 12 : 6">
                <v-select v-model="role" :items="filteredRoles" label="Role" :rules="[(v) => !!v || 'Role is required']"
                  required outlined dense></v-select>
              </v-col>

              <!-- Code/Password Input -->
              <v-col v-if="!rolesUnlocked" cols="6">
                <v-text-field class="text-info font-bold" v-model="roleCode" label="Code to Unlock Roles"
                  type="password" :rules="[(v) => !!v || 'Code is required to unlock roles']" outlined dense
                  @input="validateCode"></v-text-field>
              </v-col>
            </v-row>

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
      roleCode: '', // Code input field for unlocking roles
      validCode: 'admin123', // Predefined valid code for unlocking roles
      rolesUnlocked: false, // Tracks whether roles are unlocked
      role: 'student', // Default role
      roles: ['student', 'admin', 'supervisor'], // All available roles
      filteredRoles: ['student'], // Initially only show "student"
    };
  },
  methods: {
    validateCode() {
      // Check if the entered code matches the valid code
      if (this.roleCode === this.validCode) {
        this.filteredRoles = this.roles; // Unlock all roles
        this.rolesUnlocked = true; // Update state
        alert('Roles unlocked successfully!');
      } else {
        this.filteredRoles = ['student']; // Lock roles to "student" only
        this.rolesUnlocked = false; // Reset state
      }
    },
    async register() {
      if (this.$refs.form.validate()) {
        try {
          const response = await this.$axios.post('/api/users/register', {
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
/* Add custom styles here */
</style>
