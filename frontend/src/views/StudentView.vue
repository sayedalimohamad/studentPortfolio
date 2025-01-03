<template>
  <v-container class="py-12">
    <h1 class="text-3xl font-bold mb-6">Students</h1>
    <v-card v-if="students.length > 0">
      <v-list>
        <v-list-item
          v-for="student in students"
          :key="student.student_id"
          class="hover:bg-gray-50"
        >
          <v-list-item-content>
            <v-list-item-title class="text-lg font-semibold">
              {{ student.full_name }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-gray-600">
              {{ student.major }} at {{ student.institution }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card>
    <v-alert v-else type="info" class="mt-6"> No students found. </v-alert>
  </v-container>
</template>

<script>
export default {
  name: 'StudentView',
  data() {
    return {
      students: [],
    };
  },
  async created() {
    try {
      const response = await this.$axios.get('/api/students'); // Use global Axios
      this.students = response.data;
    } catch (error) {
      console.error('Error fetching students:', error);
    }
  },
};
</script>

<style scoped>
/* Add custom Tailwind classes or styles here */
</style>