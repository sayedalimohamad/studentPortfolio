<template>
  <v-container class="py-12">
    <h1 class="text-3xl font-bold mb-6 word-color">Admins List ({{ filteredAdmins.length }})</h1>
    <v-text-field
      v-model="search"
      label="Search by username, full name, or created by"
      prepend-inner-icon="mdi-magnify"
      class="mb-6"
      outlined
      dense
    ></v-text-field>
    
    <v-row v-if="filteredAdmins.length > 0" dense>
      <v-col v-for="admin in filteredAdmins" :key="admin.admin_id" cols="12" md="6" lg="4">
        <v-card class="mb-4 pa-4">
          <v-card-title class="d-flex align-center">
            <v-avatar class="mr-3" size="60">
              <v-icon color="primary" size="40">mdi-account</v-icon>
            </v-avatar>
            <span class="text-lg font-bold word-color">{{ admin.user.full_name }} 
              <h6>{{ calculateAge(admin.user.dob) }} year-old</h6>
            </span>
          </v-card-title>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-account-circle</v-icon>
            <span>Username: <span class="word-color">{{ admin.user.username }} ({{ admin.role }})</span></span>
          </v-card-subtitle>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-email</v-icon>
            <span>Email: <span class="word-color">{{ admin.user.email }}</span></span>
          </v-card-subtitle>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-calendar</v-icon>
            <span>Date of Birth: <span class="word-color">{{ new Date(admin.user.dob).toDateString() }}</span></span>
          </v-card-subtitle>
            <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
              <v-icon small class="mr-1">mdi-lock</v-icon>
              <span>Can Manage:</span>
              <v-chip
              class="ma-1 ml-2"
              :color="admin.permissions.manage_users ? 'green' : 'red'"
              text-color="white"
              small
              >
              <v-icon left small>mdi-account-multiple</v-icon>
              Users
              </v-chip>
              <v-chip
              class="ma-1"
              :color="admin.permissions.manage_content ? 'success' : 'error'"
              text-color="white"
              small
              >
              <v-icon left small>mdi-file-document</v-icon>
              Content
              </v-chip>
            </v-card-subtitle>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-account</v-icon>
            <span>Created By:</span>
            <v-chip class="ma-1 ml-2" color="primary" text-color="white" small>
              ID: {{ admin.created_by }}
            </v-chip>
            <v-chip class="ma-1" color="primary" text-color="white" small>
              <v-icon left small>mdi-account-circle</v-icon>
              {{ getUserName(admin.created_by) }}
            </v-chip>
          </v-card-subtitle>
          <v-card-subtitle class="text-gray-600 d-flex align-center">
            <v-icon small class="mr-1">mdi-check-circle</v-icon>
            Status:
            <v-chip
              class="ma-1 ml-2"
              :color=" admin.user.status==='active' ? 'success' : (admin.user.status === 'idle' ? 'warning' : 'error')"
              text-color="white"
              small
              >
              <v-icon left>{{ admin.user.status === 'active' ? 'mdi-check' : (admin.user.status === 'idle' ? 'mdi-clock' : 'mdi-close') }}</v-icon> 
                <strong class="mx-2">{{ admin.user.status.toUpperCase() }}</strong>
              </v-chip>
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
    <v-alert v-else type="info" class="mt-6">
      No admins found.
    </v-alert>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminView',
  data() {
    return {
      admins: [],
      search: '',
    };
  },
  methods: {
    calculateAge(dob) {
      const birthDate = new Date(dob);
      const today = new Date();
      let age = today.getFullYear() - birthDate.getFullYear();
      const month = today.getMonth();
      const birthMonth = birthDate.getMonth();

      if (month < birthMonth || (month === birthMonth && today.getDate() < birthDate.getDate())) {
        age--;
      }

      return age;
    },
  },
  computed: {
    filteredAdmins() {
      return this.admins.filter(admin => {
        const usernameMatch = admin.user.username.toLowerCase().includes(this.search.toLowerCase());
        const fullNameMatch = admin.user.full_name.toLowerCase().includes(this.search.toLowerCase());
        const createdByMatch = admin.created_by.toString().includes(this.search);
        return usernameMatch || fullNameMatch || createdByMatch;
      });
    },
  },
  async created() {
    try {
      const response = await axios.get('/api/admins');
      this.admins = response.data;
      this.getUserName = function(userId) {
        const user = this.admins.find((admin) => admin.user_id === userId);
        return user ? user.user.username : 'Unknown';
      };
    } catch (error) {
      console.error('Error fetching admins:', error);
    }
  },
};
</script>

<style scoped>
.word-color {
  color: #0097A7; /* Custom color for highlighted text */
}
.v-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  /* Ensures all cards in the row have equal height */
  padding: 16px;
  margin-bottom: 16px;
  border-radius: 8px;
  /* Add a subtle shadow for better visual separation */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.v-card-title {
  padding-bottom: 24px;
}

.v-card-subtitle {
  padding-bottom: 8px;
}

.v-card-text p {
  margin: 0;
  line-height: 1.5;
}

.v-avatar {
  background-color: #e0f7fa;
}

.v-icon {
  color: #0097A7;
}
</style>
