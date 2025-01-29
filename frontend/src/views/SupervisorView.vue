<template>
  <v-container class="py-12">
    <h1 class="text-3xl font-bold mb-6 word-color">Supervisors List ({{ filteredSupervisors.length }})</h1>
    <v-text-field
      v-model="search"
      label="Search by username, full name, or institution"
      prepend-inner-icon="mdi-magnify"
      class="mb-6"
      outlined
      dense
    ></v-text-field>
    
    <v-row v-if="filteredSupervisors.length > 0" dense>
      <v-col v-for="supervisor in filteredSupervisors" :key="supervisor.supervisor_id" cols="12" md="6" lg="4">
        <v-card class="mb-4 pa-4">
          <v-card-title class="d-flex align-center">
            <v-avatar class="mr-3" size="60">
              <v-icon color="primary" size="40">mdi-account</v-icon>
            </v-avatar>
            <span class="text-lg font-bold word-color">{{ supervisor.user.full_name }}
              <h6 >{{ calculateAge(supervisor.user.dob) }} year-old</h6>
            </span>
          </v-card-title>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-account-circle</v-icon>
            <span>Username: <span class="word-color">{{ supervisor.user.username }}</span></span>
          </v-card-subtitle>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-email</v-icon>
            <span>Email: <span class="word-color">{{ supervisor.user.email }}</span></span>
          </v-card-subtitle>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-school</v-icon>
            <span>Institution: <span class="word-color">{{ supervisor.institution }}</span></span>
          </v-card-subtitle>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-office-building</v-icon>
            <span>Department: <span class="word-color">{{ supervisor.department }}</span></span>
          </v-card-subtitle>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-calendar</v-icon>
            <span>Date of Birth: <span class="word-color">{{ new Date(supervisor.user.dob).toDateString() }}</span></span>
          </v-card-subtitle>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-4">
            <v-icon small class="mr-1">mdi-check-circle</v-icon>
            Status:
            <v-chip
              class="ma-1 ml-2"
              :color=" supervisor.user.status==='active' ? 'success' : (supervisor.user.status === 'idle' ? 'warning' : 'error')"
              text-color="white"
              small
              >
              <v-icon left>{{ supervisor.user.status === 'active' ? 'mdi-check' : (supervisor.user.status === 'idle' ? 'mdi-clock' : 'mdi-close') }}</v-icon> 
                <strong class="mx-2">{{ supervisor.user.status.toUpperCase() }}</strong>
              </v-chip>
          </v-card-subtitle>
          <!-- Bio Section at the End -->
          <v-card-text class="text-gray-800 pa-4 ma-4" :style="{
            backgroundColor: isDarkTheme ? $vuetify.theme.global.current.colors.background : $vuetify.theme.global.current.colors.onCard,
            borderRadius: '8px',
            color: $vuetify.theme.global.current.colors.primary
          }">
            <v-icon small class="mr-1">mdi-text</v-icon>
            <span class="font-medium">Bio:</span>
            <p class="ml-5 mt-2" style="text-align: justify;">{{ supervisor.bio }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-alert v-else type="info" class="mt-6">
      No supervisors found.
    </v-alert>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SupervisorView',
  data() {
    return {
      supervisors: [],
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
    filteredSupervisors() {
      return this.supervisors.filter(supervisor => {
        const usernameMatch = supervisor.user.username.toLowerCase().includes(this.search.toLowerCase());
        const fullNameMatch = supervisor.user.full_name.toLowerCase().includes(this.search.toLowerCase());
        const institutionMatch = supervisor.institution.toLowerCase().includes(this.search.toLowerCase());
        return usernameMatch || fullNameMatch || institutionMatch;
      });
    },
    isDarkTheme() {
      return this.$vuetify.theme.global.current.dark;
    },
  },
  async created() {
    try {
      const response = await axios.get('/api/supervisors');
      this.supervisors = response.data;
    } catch (error) {
      console.error('Error fetching supervisors:', error);
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