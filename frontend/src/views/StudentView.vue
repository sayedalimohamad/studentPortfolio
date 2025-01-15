<template>
  <v-container class="py-12">
    <h1 class="text-3xl font-bold mb-6 word-color">Students List ({{ filteredStudents.length }})</h1>
    <v-text-field
      v-model="searchQuery"
      label="Search by name"
      prepend-inner-icon="mdi-magnify"
      class="mb-6"
      outlined
      dense
    ></v-text-field>
    <v-row v-if="filteredStudents.length > 0" dense align="stretch">
      <v-col v-for="student in filteredStudents" :key="student.student_id" cols="12" md="6" lg="4">
        <v-card class="mb-4 pa-4 d-flex flex-column justify-space-between elevation-2">
          <v-card-title class="d-flex align-center">
            <v-avatar class="mr-3" size="40">
              <v-icon color="primary" size="36">mdi-account</v-icon>
            </v-avatar>
            <span class="text-lg font-bold word-color">{{ student.full_name }}</span>
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
            <span>Privacy Level: <span class="word-color">{{ student.privacy_level }}</span></span>
          </v-card-subtitle>
          <v-card-text class="text-gray-800 mt-4" style="background-color: #e0f7fa; border-radius: 8px;">
            <v-icon small class="mr-1">mdi-information-outline</v-icon>
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
import axios from 'axios'; // Import the custom Axios instance

export default {
  name: 'StudentView',
  data() {
    return {
      students: [],
      searchQuery: '',
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
  computed: {
    filteredStudents() {
      return this.students.filter(student => {
        const fullName = student.full_name.toLowerCase().includes(this.searchQuery.toLowerCase());
        const institution = student.institution.toLowerCase().includes(this.searchQuery.toLowerCase());
        const privacyLevel = student.privacy_level.toString().includes(this.searchQuery);
        return fullName || institution || privacyLevel;
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
