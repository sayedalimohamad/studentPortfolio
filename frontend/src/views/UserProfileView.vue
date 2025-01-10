<template>
    <v-container class="py-12">
      <!-- User Profile Header -->
      <v-row class="mb-6">
        <v-col cols="12" class="text-center">
          <h1 class="text-3xl font-bold word-color">{{ userRole }} Profile</h1>
          <p class="text-lg text-gray-700">Welcome to your personalized profile page.</p>
        </v-col>
      </v-row>
  
      <!-- User Profile Card -->
      <v-card v-if="user" class="mx-auto" max-width="800">
        <v-card-text>
          <!-- Common Fields for All Roles -->
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
  
          <!-- Student-Specific Fields -->
          <template v-if="userRole === 'student'">
            <v-row>
              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon color="primary">mdi-school</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title class="font-bold">Major</v-list-item-title>
                    <v-list-item-subtitle class="text-gray-700">{{ user.major }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon color="primary">mdi-bank</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title class="font-bold">Institution</v-list-item-title>
                    <v-list-item-subtitle class="text-gray-700">{{ user.institution }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon color="primary">mdi-cake</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title class="font-bold">Date of Birth</v-list-item-title>
                    <v-list-item-subtitle class="text-gray-700">{{ user.dob }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon color="primary">mdi-lock</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title class="font-bold">Privacy Level</v-list-item-title>
                    <v-list-item-subtitle class="text-gray-700">{{ user.privacy_level }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon color="primary">mdi-text</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title class="font-bold">Bio</v-list-item-title>
                    <v-list-item-subtitle class="text-gray-700">{{ user.bio }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
            </v-row>
          </template>
  
          <!-- Admin-Specific Fields -->
          <template v-if="userRole === 'admin'">
            <v-row>
              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon color="primary">mdi-office-building</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title class="font-bold">Department</v-list-item-title>
                    <v-list-item-subtitle class="text-gray-700">{{ user.department }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon color="primary">mdi-shield-account</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title class="font-bold">Access Level</v-list-item-title>
                    <v-list-item-subtitle class="text-gray-700">{{ user.access_level }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
            </v-row>
          </template>
  
          <!-- Supervisor-Specific Fields -->
          <template v-if="userRole === 'supervisor'">
            <v-row>
              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon color="primary">mdi-domain</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title class="font-bold">Faculty</v-list-item-title>
                    <v-list-item-subtitle class="text-gray-700">{{ user.faculty }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
              <v-col cols="12" md="6">
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon color="primary">mdi-map-marker</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title class="font-bold">Office</v-list-item-title>
                    <v-list-item-subtitle class="text-gray-700">{{ user.office }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon color="primary">mdi-account-group</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title class="font-bold">Assigned Students</v-list-item-title>
                    <v-list-item-subtitle class="text-gray-700">{{ user.assigned_students }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
            </v-row>
          </template>
        </v-card-text>
      </v-card>
  
      <!-- Loading or Error Messages -->
      <v-alert v-if="loading" type="info" class="mt-6">Loading...</v-alert>
      <v-alert v-if="error" type="error" class="mt-6">{{ error }}</v-alert>
    </v-container>
  </template>
  
  <script>
  export default {
    name: 'UserProfileView',
    data() {
      return {
        user: null, // Store user data
        loading: true, // Track loading state
        error: null, // Store error message
        userRole: null, // Store user role (student, admin, supervisor)
      };
    },
    async created() {
      // Extract user role and ID from route params
      const { role, id } = this.$route.params;
  
      // Validate role
      const validRoles = ['student', 'admin', 'supervisor'];
      if (!validRoles.includes(role)) {
        this.error = 'Invalid user role.';
        this.loading = false;
        return;
      }
  
      this.userRole = role;
  
      try {
        // Simulate fetching user data (replace with actual API call)
        this.user = this.getStaticUserData(role, id);
      } catch (error) {
        console.error(`Error fetching ${role} data:`, error);
        this.error = `Failed to load ${role} data.`;
      } finally {
        this.loading = false;
      }
    },
    methods: {
      // Simulate static user data (replace with API call)
      getStaticUserData(role, id) {
        const staticData = {
          student: {
            full_name: 'John Doe',
            email: 'john.doe@example.com',
            major: 'Computer Science',
            institution: 'University of Example',
            dob: '1998-05-15',
            privacy_level: 'Public',
            bio: 'Passionate about AI and software development.',
          },
          admin: {
            full_name: 'Jane Smith',
            email: 'jane.smith@example.com',
            department: 'IT Services',
            access_level: 'Super Admin',
          },
          supervisor: {
            full_name: 'Michael Brown',
            email: 'michael.brown@example.com',
            faculty: 'Engineering',
            office: 'Building A, Room 101',
            assigned_students: '15',
          },
        };
  
        return staticData[role];
      },
    },
  };
  </script>
  
  <style scoped>
  .word-color {
    color: #0097a7;
  }
  </style>