<template>
  <v-container class="py-12">
    <h1 class="text-3xl font-bold mb-6 word-color">Students List</h1>
    <v-card v-if="students.length > 0">
      <v-list>
        <v-list-item
          v-for="student in students"
          :key="student.student_id"
          class="hover:bg-gray-50"
        >
          <v-list-item-content>
            <v-list-item-title class="text-lg font-bold word-color">
              {{ student.full_name }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-gray-600">
              {{ student.major }} at <span class="word-color"> {{ student.institution }} </span>
            </v-list-item-subtitle>
            <v-list-item-subtitle class="text-gray-600">
              Date of Birth: {{ student.dob }}
            </v-list-item-subtitle>
            <v-list-item-subtitle class="text-gray-600">
              Privacy Level: {{ student.privacy_level }}
            </v-list-item-subtitle>
            <v-list-item-subtitle class="text-gray-600">
              Bio: {{ student.bio }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card>
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
    }
  },
};
</script>

<style scoped>
.word-color {
  color: #2b6cb0;
}
</style>