<template>
  <v-container class="py-12">
    <v-row class="justify-center">
      <v-col cols="12" md="6">
        <v-card class="px-6 py-8">
          <h1 class="text-3xl font-bold mb-6 text-center">Register</h1>
          <v-form @submit.prevent="register" ref="form">
            <!-- Username -->
            <v-text-field v-model="username" label="Username" :rules="[(v) => !!v || 'Username is required']" required
              outlined></v-text-field>

            <!-- Email -->
            <v-text-field v-model="email" label="Email" type="email"
              :rules="[(v) => !!v || 'Email is required', (v) => /.+@.+\..+/.test(v) || 'Email must be valid',]"
              required outlined></v-text-field>

            <!-- Password -->
            <v-text-field v-model="password" label="Password" :type="showPassword ? 'text' : 'password'"
              :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="[(v) => !!v || 'Password is required', (v) => v.length >= 8 || 'Password must be at least 8 characters',]"
              required outlined @click:append-inner="showPassword = !showPassword"></v-text-field>

            <!-- Confirm Password -->
            <v-text-field v-model="confirmPassword" label="Confirm Password" :type="showPassword ? 'text' : 'password'"
              :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="[(v) => !!v || 'Confirm Password is required', (v) => v === password || 'Passwords must match',]"
              required outlined @click:append-inner="showPassword = !showPassword"></v-text-field>

            <!-- Full Name (Required for all roles) -->
            <v-text-field v-model="fullName" label="Full Name" :rules="[(v) => !!v || 'Full Name is required']" required
              outlined></v-text-field>

            <!-- Date of Birth (Required for all roles) -->
            <v-text-field v-model="dob" label="Date of Birth" type="date"
              :rules="[(v) => !!v || 'Date of Birth is required']" required outlined></v-text-field>

            <!-- Dynamic Row for Role and Code Input -->
            <v-row>
              <!-- Role Selection -->
              <v-col :cols="rolesUnlocked ? 12 : 6">
                <v-select v-model="role" :items="filteredRoles" label="Role" :rules="[(v) => !!v || 'Role is required']"
                  required outlined dense @change="handleRoleChange"></v-select>
              </v-col>

              <!-- Code/Password Input -->
              <v-col v-if="!rolesUnlocked" cols="6">
                <v-text-field class="text-info font-bold" v-model="roleCode" label="Unlock Roles" type="password"
                  outlined dense @input="validateCode"></v-text-field>
              </v-col>
            </v-row>

            <!-- Additional Fields for Admin -->
            <template v-if="role === 'admin'">
              <v-card class="mb-4" outlined>
                <v-card-title>Permissions</v-card-title>
                <v-card-text>
                  <v-checkbox v-for="(value, key) in permissions" :key="key" v-model="permissions[key]" :label="key"
                    hide-details color="primary"></v-checkbox>
                </v-card-text>
              </v-card>
              <v-text-field v-model="createdBy" label="Created By (User ID)"
                :rules="[(v) => !!v || 'Created By is required']" required outlined></v-text-field>
            </template>

            <!-- Additional Fields for Supervisor -->
            <template v-if="role === 'supervisor'">
              <v-text-field v-model="institution" label="Institution" :rules="[(v) => !!v || 'Institution is required']"
                required outlined></v-text-field>
              <v-text-field v-model="department" label="Department" :rules="[(v) => !!v || 'Department is required']"
                required outlined></v-text-field>
              <v-textarea v-model="bio" label="Bio" outlined></v-textarea>
            </template>

            <!-- Additional Fields for Student -->
            <template v-if="role === 'student'">
              <v-text-field v-model="institution" label="Institution" :rules="[(v) => !!v || 'Institution is required']"
                required outlined></v-text-field>
              <v-text-field v-model="major" label="Major" :rules="[(v) => !!v || 'Major is required']" required
                outlined></v-text-field>
              <v-select v-model="privacyLevel" :items="privacyLevels" label="Privacy Level"
                :rules="[(v) => !!v || 'Privacy Level is required']" required outlined></v-select>
              <v-textarea v-model="bio" label="Bio" outlined></v-textarea>
            </template>

            <v-btn type="submit" color="primary" block large class="my-4">Register</v-btn>
            <div class="d-block mb-2 text-muted py-4 text-center">
              I have an account
              <a href="/login" class="text-decoration-none text-primary font-weight-bold">
                Login
              </a>
            </div>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useToast } from 'vue-toastification';
import axios from 'axios';

export default {
  name: 'RegisterView',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      roleCode: '',
      validCode: 'admin123',
      rolesUnlocked: false,
      role: 'student', // Default role
      filteredRoles: ['student'], // Initially only show "student"
      roles: ['student', 'admin', 'supervisor'],
      showPassword: false,

      // Admin-specific fields
      permissions: {
        manage_users: false,
        manage_content: false,
      },
      createdBy: '',

      // Supervisor-specific fields
      institution: '',
      department: '',
      bio: '',

      // Student-specific fields
      fullName: '',
      dob: '',
      major: '',
      privacyLevel: '',

      // Privacy Levels
      privacyLevels: ['Public', 'Private', 'Restricted'],
    };
  },
  methods: {
    validateCode() {
      const toast = useToast();
      if (this.roleCode === this.validCode) {
        this.filteredRoles = this.roles;
        this.rolesUnlocked = true;
        toast.success('Roles unlocked successfully!');
      } else {
        this.filteredRoles = ['student'];
        this.rolesUnlocked = false;
      }
    },
    handleRoleChange() {
      // Reset role-specific fields when the role changes
      this.permissions = {
        manage_users: false,
        manage_content: false,
      };
      this.createdBy = '';
      this.institution = '';
      this.department = '';
      this.major = '';
      this.privacyLevel = '';
      this.bio = '';
    },
    async register() {
      const toast = useToast();
      if (this.$refs.form.validate()) {
        if (this.password !== this.confirmPassword) {
          toast.error('Passwords do not match.');
          return;
        }

        try {
          // Prepare the payload
          const payload = {
            username: this.username,
            email: this.email,
            password: this.password,
            role: this.role,
            full_name: this.fullName,
            dob: this.dob,
            status: 'active',
          };

          // Add role-specific fields
          if (this.role === 'admin') {
            payload.permissions = this.permissions;
            payload.created_by = this.createdBy;
          } else if (this.role === 'supervisor') {
            payload.institution = this.institution;
            payload.department = this.department;
            payload.bio = this.bio;
          } else if (this.role === 'student') {
            payload.institution = this.institution;
            payload.major = this.major;
            payload.privacy_level = this.privacyLevel;
            payload.bio = this.bio;
          }

          console.log('Registration Payload:', payload);

          // Send the payload to the backend
          const response = await axios.post('/api/users/register', payload);
          console.log('Registration Response:', response.data);

          toast.success('Registration successful!');
          this.$router.push('/login');
        } catch (error) {
          console.error('Registration Error:', error.response ? error.response.data : error.message);
          toast.error(error.response?.data?.error || 'Registration failed. Please try again.');
        }
      } else {
        console.log('Form validation failed');
      }
    },
  },
};
</script>