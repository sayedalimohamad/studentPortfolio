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
                <v-list-item-subtitle class="text-gray-700">{{ new Date(user.dob).toDateString() }}</v-list-item-subtitle>
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
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-icon>
                <v-icon color="primary">mdi-information-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title class="font-bold">Bio</v-list-item-title>
                <v-list-item-subtitle class="text-gray-700 text-justify">{{ studentInfo.bio }}</v-list-item-subtitle>
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
          <v-col cols="12" md="6">
            <v-list-item>
              <v-list-item-icon>
                <v-icon color="primary">mdi-information-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title class="font-bold">Bio</v-list-item-title>
                <v-list-item-subtitle class="text-gray-700 text-justify">{{ supervisorInfo.bio }}</v-list-item-subtitle>
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
                <v-list-item-subtitle class="text-gray-700">
                  <v-chip class="ma-1 ml-2" :color="adminInfo.permissions.manage_users ? 'green' : 'red'" text-color="white" small>
                    <v-icon left small>mdi-account-multiple</v-icon>
                    Manage Users
                  </v-chip>
                  <v-chip class="ma-1" :color="adminInfo.permissions.manage_content ? 'green' : 'red'" text-color="white" small>
                    <v-icon left small>mdi-file-document</v-icon>
                    Manage Content
                  </v-chip>
                </v-list-item-subtitle>
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

        <!-- Edit Profile Button -->
        <v-row>
          <v-col cols="12" class="text-right">
            <v-btn color="primary" dark @click="showEditModal = true">
              <v-icon left>mdi-pencil</v-icon>
              Edit Profile
            </v-btn>
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

    <!-- Edit Profile Modal -->
    <v-dialog v-model="showEditModal" max-width="600">
      <v-card>
        <v-card-title class="headline">
          <v-icon color="primary" left>mdi-pencil</v-icon>
          Edit Profile
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="formValid">
            <!-- Common Fields -->
            <v-text-field v-model="editedUser.full_name" label="Full Name" required outlined dense></v-text-field>
            <v-text-field v-model="editedUser.email" label="Email" required outlined dense></v-text-field>
            <v-text-field v-model="editedUser.username" label="Username" required outlined dense></v-text-field>
            <v-text-field
              v-model="editedUser.dob"
              label="Date of Birth"
              type="date"
              required
              outlined
              dense
              :rules="[(v) => !!v || 'Date of Birth is required']"
            ></v-text-field>

            <!-- Student-Specific Fields -->
            <v-row v-if="userRole === 'student'">
              <v-col cols="12" md="6">
                <v-text-field v-model="editedUser.institution" label="Institution" outlined dense></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="editedUser.major" label="Major" outlined dense></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea v-model="editedUser.bio" label="Bio" outlined dense></v-textarea>
              </v-col>
            </v-row>

            <!-- Supervisor-Specific Fields -->
            <v-row v-if="userRole === 'supervisor'">
              <v-col cols="12" md="6">
                <v-text-field v-model="editedUser.institution" label="Institution" outlined dense></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="editedUser.department" label="Department" outlined dense></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea v-model="editedUser.bio" label="Bio" outlined dense></v-textarea>
              </v-col>
            </v-row>

            <!-- Admin-Specific Fields -->
            <v-row v-if="userRole === 'admin'">
              <v-col cols="12">
                <v-select
                  v-model="editedUser.role"
                  :items="['admin', 'student', 'supervisor']"
                  label="Role"
                  outlined
                  dense
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-switch
                  v-model="editedUser.permissions.manage_users"
                  label="Manage Users"
                  color="primary"
                ></v-switch>
              </v-col>
              <v-col cols="12">
                <v-switch
                  v-model="editedUser.permissions.manage_content"
                  label="Manage Content"
                  color="primary"
                ></v-switch>
              </v-col>
            </v-row>

            <!-- New Password Fields -->
            <v-text-field
              v-if="newPassword"
              v-model="editedUser.password"
              label="New Password"
              type="password"
              outlined
              dense
              :rules="[(v) => !!v || 'Password is required']"
            />
            <v-text-field
              v-if="newPassword"
              v-model="confirmPassword"
              label="Confirm New Password"
              type="password"
              outlined
              dense
              :rules="[(v) => v === editedUser.password || 'Passwords must match']"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="showEditModal = false">
            <v-icon left>mdi-cancel</v-icon>
            Cancel
          </v-btn>
          <v-btn color="green darken-1" text @click="confirmUpdateProfile">
            <v-icon left>mdi-check</v-icon>
            Save Changes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Modal -->
    <v-dialog v-model="showDeleteModal" max-width="500">
      <v-card>
        <v-card-title class="headline">
          <v-icon color="red" left>mdi-alert-circle</v-icon>
          Confirm Account Deletion
        </v-card-title>
        <v-card-text>
          <p>Please enter your password to confirm account deletion:</p>
          <v-text-field v-model="password" :type="showPassword ? 'text' : 'password'" label="Password" required outlined dense :rules="[(v) => !!v || 'Password is required']" append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'" @click:append-inner="showPassword = !showPassword"></v-text-field>
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
      editedUser: {
        full_name: '',
        email: '',
        username: '',
        dob: '',
        password: '',
        institution: '', // Student/Supervisor
        major: '', // Student
        department: '', // Supervisor
        bio: '', // Student/Supervisor
        role: '', // Admin
        permissions: { // Admin
          manage_users: false,
          manage_content: false,
        },
      },
      studentInfo: null,
      supervisorInfo: null,
      adminInfo: null,
      loading: true,
      error: null,
      userRole: null,
      showDeleteModal: false,
      showEditModal: false,
      newPassword: false,
      confirmPassword: '',
      password: '',
      showPassword: false,
      formValid: false,
    };
  },
  async created() {
    const { role } = this.$route.params;
    const storedAuth = localStorage.getItem('token');

    // Redirect to login if not authenticated
    if (!storedAuth) {
      this.$router.push('/login');
      return;
    }

    this.userRole = role;
    await this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      const { id } = this.$route.params;
      const storedAuth = localStorage.getItem('token');

      try {
        // Fetch user details from the backend
        const userResponse = await axios.get(`/api/users/${id}`, {
          headers: { Authorization: `Bearer ${storedAuth}` },
        });
        this.user = userResponse.data;
        this.editedUser = { ...this.user ,dob: this.user.dob ? new Date(this.user.dob).toISOString().split('T')[0] : '' };

        // Fetch role-specific information
        if (this.userRole === 'student') {
          this.studentInfo = userResponse.data;
          this.editedUser.institution = this.studentInfo.institution;
          this.editedUser.major = this.studentInfo.major;
          this.editedUser.bio = this.studentInfo.bio;
        } else if (this.userRole === 'supervisor') {
          this.supervisorInfo = userResponse.data;
          this.editedUser.institution = this.supervisorInfo.institution;
          this.editedUser.department = this.supervisorInfo.department;
          this.editedUser.bio = this.supervisorInfo.bio;
        } else if (this.userRole === 'admin') {
          this.adminInfo = userResponse.data;
          this.editedUser.role = this.adminInfo.role;
          this.editedUser.permissions = this.adminInfo.permissions;
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
        this.error = 'Failed to load user data.';
        useToast().error(this.error);
      } finally {
        this.loading = false;
      }
    },

    async confirmUpdateProfile() {
      const { id } = this.$route.params;
      const storedAuth = localStorage.getItem('token');

      if (!this.formValid) {
        this.error = 'Please fill in all required fields.';
        useToast().error(this.error);
        return;
      }

      try {
        const updatedUser = { ...this.editedUser };

        // Include role-specific fields in the payload
        if (this.userRole === 'student') {
          updatedUser.institution = this.editedUser.institution;
          updatedUser.major = this.editedUser.major;
          updatedUser.bio = this.editedUser.bio;
        } else if (this.userRole === 'supervisor') {
          updatedUser.institution = this.editedUser.institution;
          updatedUser.department = this.editedUser.department;
          updatedUser.bio = this.editedUser.bio;
        } else if (this.userRole === 'admin') {
          updatedUser.role = this.editedUser.role;
          updatedUser.permissions = {
            manage_users: this.editedUser.permissions.manage_users,
            manage_content: this.editedUser.permissions.manage_content,
          };
        }

        // Handle password update
        if (this.newPassword && this.editedUser.password !== this.confirmPassword) {
          this.error = 'Passwords must match.';
          useToast().error(this.error);
          return;
        }

        if (this.newPassword) {
          updatedUser.password = this.editedUser.password;
        }

        // Send the update request to the API
        await axios.put(`/api/users/${id}`, updatedUser, {
          headers: {
            Authorization: `Bearer ${storedAuth}`,
          },
        });

        // Re-fetch the updated user data
        await this.fetchUserData();

        useToast().success('Profile updated successfully.');
        this.showEditModal = false;
        localStorage.setItem('email', updatedUser.email);
      } catch (error) {
        console.error('Error updating profile:', error);
        this.error = 'Failed to update profile.';
        useToast().error(this.error);
      }
    },

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