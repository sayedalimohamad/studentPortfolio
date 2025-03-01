<template>
  <v-container class="py-12" >
    <!-- Hero Section -->
    <v-row align="center" class="mb-12">
      <v-col cols="12" md="6" class="text-center text-md-left">
        <h1 class="text-4xl font-bold mb-4 word-color">Welcome to StudentPortfolio</h1>
        <p class="text-lg text-gray-700 mb-6">
          Revolutionizing how students manage their academic and professional growth.
        </p>
        <v-btn to="/login" color="primary" large class="mr-4" >Get Started</v-btn>
        <v-btn to="/register" outlined color="primary" large>Register</v-btn>
      </v-col>
      <v-col cols="12" md="6" class="text-center">
        <v-img
          src="/reading-book_qe4h.svg"
          alt="StudentPortfolio Hero Image"
          class="rounded-lg"
        ></v-img>
      </v-col>
    </v-row>

    <!-- Features Section -->
    <v-row class="mb-12">
      <v-col cols="12" class="text-center">
        <h2 class="text-3xl font-bold mb-6 word-color">Why Choose StudentPortfolio?</h2>
      </v-col>
      <v-col cols="12" md="4" class="d-flex">
        <v-card class="pa-6 text-center flex-grow-1">
          <v-icon size="64" color="primary">mdi-account-group</v-icon>
          <h3 class="text-xl font-bold mt-4 mb-2">Centralized Platform</h3>
          <p class="text-gray-700">
            A user-friendly system to create and maintain portfolios, all in one place.
          </p>
        </v-card>
      </v-col>
      <v-col cols="12" md="4" class="d-flex">
        <v-card class="pa-6 text-center flex-grow-1">
          <v-icon size="64" color="primary">mdi-chart-line</v-icon>
          <h3 class="text-xl font-bold mt-4 mb-2">AI-Powered Tools</h3>
          <p class="text-gray-700">
            Leverage AI to showcase skills, track progress, and receive personalized guidance.
          </p>
        </v-card>
      </v-col>
      <v-col cols="12" md="4" class="d-flex">
        <v-card class="pa-6 text-center flex-grow-1">
          <v-icon size="64" color="primary">mdi-handshake</v-icon>
          <h3 class="text-xl font-bold mt-4 mb-2">Collaboration & Guidance</h3>
          <p class="text-gray-700">
            Connect with supervisors and peers for meaningful interactions and feedback.
          </p>
        </v-card>
      </v-col>
    </v-row>

    <!-- About Section -->
    <v-row class="mb-12">
      <v-col cols="12" class="text-center">
        <h2 class="text-3xl font-bold mb-6 word-color">About StudentPortfolio</h2>
      </v-col>
      <v-col cols="12" md="6" class="text-center">
        <v-img
          src="/resume-folder_hf4p.svg"
          alt="About StudentPortfolio"
          class="rounded-lg"
        ></v-img>
      </v-col>
      <v-col cols="12" md="6">
        <p class="text-lg text-gray-700 mb-6">
          StudentPortfolio is an advanced platform designed to streamline the process of showcasing skills, managing academic activities, and enabling meaningful interactions between students, supervisors, and administrators.
        </p>
        <p class="text-lg text-gray-700 mb-6">
          Our mission is to provide a well-rounded and future-ready student experience, empowering learners to achieve their academic and professional goals.
        </p>
        <v-btn to="/about" color="primary" large>Learn More</v-btn>
      </v-col>
      
    </v-row>

    <!-- Testimonials Section -->
    <v-row class="mb-12" align="stretch">
      <v-col cols="12" class="text-center">
      <h2 class="text-3xl font-bold mb-6 word-color">What Our Users Say</h2>
      </v-col>
      <v-col cols="12" md="4" class="d-flex">
      <v-card class="pa-6 text-center flex-grow-1">
        <v-avatar size="120" class="mb-4">
        <v-img src="/student.svg" alt="User 1" style="background-color: #fbc531;"></v-img>
        </v-avatar>
        <p class="text-gray-700 mb-4 ">
        "StudentPortfolio has transformed how I manage my academic journey. I love it!"
        </p>
        <h3 class="text-lg font-bold word-color">Wendy Hawkins</h3>
        <p class="text-gray-600 mb-4">Student </p>
        <v-chip color="warning" outlined >Idle</v-chip>
      </v-card>
      </v-col>
      <v-col cols="12" md="4" class="d-flex">
      <v-card class="pa-6 text-center flex-grow-1">
        <v-avatar size="120" class="mb-4">
        <v-img src="/woman.svg" alt="User 2" style="background-color: #e84118;"></v-img>
        </v-avatar>
        <p class="text-gray-700 mb-4">
        "As a supervisor, I find the platform incredibly helpful for guiding my students."
        </p>
        <h3 class="text-lg font-bold word-color">Stephanie Johnson</h3>
        <p class="text-gray-600 mb-6">Supervisor</p>
        <v-chip color="error" outlined>Offline</v-chip>
      </v-card>
      </v-col>
      <v-col cols="12" md="4" class="d-flex">
      <v-card class="pa-6 text-center flex-grow-1">
        <v-avatar size="120" class="mb-4">
        <v-img src="/man.svg" alt="User 3" style="background-color: #4cd137;"></v-img>
        </v-avatar>
        <p class="text-gray-700 mb-4">
        "The AI tools and collaboration features are game-changers for our institution."
        </p>
        <h3 class="text-lg font-bold word-color">Jason Martin</h3>
        <p class="text-gray-600 mb-4">Administrator</p>
        <v-chip color="success" outlined>Active</v-chip>
      </v-card>
      </v-col>
    </v-row>

    <!-- Call to Action Section -->
    <v-row class="mb-12">
      <v-col cols="12" class="text-center">
        <h2 class="text-3xl font-bold mb-6 word-color">Ready to Get Started?</h2>
        <p class="text-lg text-gray-700 mb-4">
          Join StudentPortfolio today and take control of your academic and professional growth.
        </p>
        <v-btn to="/register" color="primary" large>Sign Up Now</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'HomeView',
};
</script>

<style scoped>
.word-color {
  color: #0097a7;
}
h3{
  font-size: 1.4rem;
}

</style>