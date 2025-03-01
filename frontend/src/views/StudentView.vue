<template>
  <v-container class="py-12">
    <h1 class="text-3xl font-bold mb-6 word-color">Students List ({{ filteredStudents.length }})</h1>
    <v-row dense>
      <v-col cols="12" md="6">
        <v-text-field v-model="searchQuery" label="Search by name" prepend-inner-icon="mdi-magnify" class="mb-6" outlined dense></v-text-field>
      </v-col>
      <v-col cols="12" md="6">
        <v-select v-model="selectedPrivacyLevel" :items="privacyLevels" label="Filter by Privacy Level" class="mb-6" prepend-inner-icon="mdi-filter"
        outlined dense clearable></v-select>
      </v-col>
    </v-row>
    <v-row v-if="filteredStudents.length > 0" dense align="stretch">
      <v-col v-for="student in filteredStudents" :key="student.student_id" cols="12" md="6" lg="4">
        <v-card class="mb-4 pa-4 d-flex flex-column justify-space-between elevation-2">
          <v-card-title class="d-flex align-center">
            <v-avatar class="mr-3" size="60">
              <v-icon color="primary" size="40">mdi-account</v-icon>
            </v-avatar>
            <span class="text-lg font-bold word-color">{{ student.full_name }}
              <h6>{{ calculateAge(student.dob) }} year-old</h6>
            </span>
          </v-card-title>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-email</v-icon>
            <span>Email: <span class="word-color">{{ student.email }}</span></span>
          </v-card-subtitle>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-account-circle</v-icon>
            <span>Username: <span class="word-color">{{ student.username }}</span></span>
          </v-card-subtitle>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-school</v-icon>
            <span>Major: <span class="word-color">{{ student.major }}</span></span>
          </v-card-subtitle>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-home-city</v-icon>
            <span>Institution: <span class="word-color">{{ student.institution }}</span></span>
          </v-card-subtitle>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-calendar</v-icon>
            <span>Date of Birth: <span class="word-color">{{ new Date(student.dob).toDateString() }}</span></span>
          </v-card-subtitle>
          <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
            <v-icon small class="mr-1">mdi-lock</v-icon>
            <span>Privacy Level:
              <v-chip class="ma-1 ml-2"
                :color="student.privacy_level === 'public' ? 'primary' : (student.privacy_level === 'supervisors' ? 'success' : 'error')"
                text-color="white" small>
                <strong class="mx-2">{{ student.privacy_level.toUpperCase() }}</strong>
              </v-chip>
              <v-chip
                :color="student.privacy_level === 'public' ? 'primary' : (student.privacy_level === 'supervisors' ? 'success' : 'error')">
                <v-icon left
                  :color="student.privacy_level === 'public' ? 'primary' : (student.privacy_level === 'supervisors' ? 'success' : 'error')">{{
                    student.privacy_level === 'public' ? 'mdi-earth' : (student.privacy_level ===
                      'supervisors' ? 'mdi-account-supervisor' : 'mdi-lock') }}</v-icon>
              </v-chip>
            </span>
          </v-card-subtitle>
          <v-card-text class="text-gray-800 mt-4" :style="{
            backgroundColor: isDarkTheme ? $vuetify.theme.global.current.colors.background : $vuetify.theme.global.current.colors.onCard,
            borderRadius: '8px',
            color: $vuetify.theme.global.current.colors.primary
          }">
            <v-icon small class="mr-1">mdi-text</v-icon>
            <span class="font-medium">Bio:</span>
            <p class="ml-5 mt-2 " style="text-align: justify;">{{ student.bio }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-alert v-else type="info" class="mt-6"> No students found. </v-alert>
  </v-container>
</template>

<script>
import axios from 'axios'; 

export default {
  name: 'StudentView',
  data() {
    return {
      students: [],
      searchQuery: '',
      selectedPrivacyLevel: null,
      privacyLevels: ['public', 'supervisors', 'private'],
    };
  },
  async created() {
    try {
      const response = await axios.get('/api/students'); // Use the custom Axios instance
      this.students = response.data;
    } catch (error) {
      console.error('Error fetching students:', error);
      this.$toast.error('Failed to fetch students. Please try again.');
    }
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
    filteredStudents() {
      return this.students.filter(student => {
        const fullName = student.full_name.toLowerCase().includes(this.searchQuery.toLowerCase());
        const institution = student.institution.toLowerCase().includes(this.searchQuery.toLowerCase());
        const privacyLevel = student.privacy_level.toString().includes(this.searchQuery);
        const matchesPrivacyLevel = this.selectedPrivacyLevel ? student.privacy_level === this.selectedPrivacyLevel : true;
        return (fullName || institution || privacyLevel) && matchesPrivacyLevel;
      });
    },
  },
};
</script>

<style scoped>
.word-color {
  color: #0097A7;
  /* Custom color for highlighted text */
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
