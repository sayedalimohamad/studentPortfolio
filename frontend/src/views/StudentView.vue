<template>
  <v-container class="py-12">
    <h1 class="text-3xl font-bold mb-6 word-color">Students List ({{ students.length }})</h1>
    <v-row v-if="students.length > 0" dense align="stretch">
      <v-col v-for="student in students" :key="student.student_id" cols="12" md="6" lg="4">
        <v-card class="mb-4 pa-4 d-flex flex-column justify-space-between">
          <div>
            <v-card-title class="d-flex align-center">
              <v-avatar class="mr-3">
                <v-icon color="primary">mdi-account-circle</v-icon>
              </v-avatar>
              <span class="text-lg font-bold word-color">{{ student.full_name }}</span>
            </v-card-title>
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
              <span>Date of Birth: <span class="word-color">{{ student.dob }}</span></span>
            </v-card-subtitle>
            <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
              <v-icon small class="mr-1">mdi-lock</v-icon>
              <span>Privacy Level: <span class="word-color">{{ student.privacy_level }}</span></span>
            </v-card-subtitle>
          </div>
          <v-card-text class="text-gray-800 mt-4">
            <v-icon small class="mr-1">mdi-information-outline</v-icon>
            <span class="font-medium">Bio:</span>
            <p class="ml-5 mt-2">{{ student.bio }}</p>
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
  height: 100%; /* Ensures all cards in the row have equal height */
  padding: 16px;
  margin-bottom: 16px;
}
.v-card-title {
  padding-bottom: 8px;
}
.v-card-subtitle {
  padding-bottom: 8px;
}
.v-card-text p {
  margin: 0;
  line-height: 1.5;
}
</style>
