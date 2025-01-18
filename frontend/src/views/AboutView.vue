<template>
  <v-container class="py-12">
    <!-- Hero Section -->
    <v-row align="center" class="mb-12">
      <v-col cols="12" md="6" class="text-center text-md-left">
        <h1 class="text-4xl font-bold mb-4 word-color">About StudentPortfolio</h1>
        <p class="text-lg text-gray-700 mb-6">
          Revolutionizing the way students, supervisors, and administrators manage academic and professional growth.
          A comprehensive solution for collaboration, organization, and progress tracking.
          StudentPortfolio offers intuitive tools and features designed to enhance productivity and streamline
          workflows,
          ensuring that every user can achieve their full potential. Join us in transforming the educational experience
          with cutting-edge technology and innovative solutions.
        </p>
        <v-btn to="/register" color="primary" large class="mr-4">Get Started Now</v-btn>
      </v-col>
      <v-col cols="12" md="6" class="text-center">
        <v-img src="/oad-to-knowledge_f9zn.svg" alt="StudentPortfolio Overview" class="rounded-lg shadow-lg"></v-img>
      </v-col>
    </v-row>

    <!-- Core Features Section -->
    <v-row class="mb-12">
      <v-col cols="12" class="text-center">
        <h2 class="text-3xl font-bold mb-6 word-color">Core Features of StudentPortfolio</h2>
        <p class="text-lg text-gray-700 mb-6">
          Key features that make StudentPortfolio the ultimate platform for students and educators.
        </p>
      </v-col>
      <v-col cols="12" md="4" class="d-flex">
        <v-card class="pa-6 text-center flex-grow-1 hover-elevation">
          <v-icon size="64" color="primary">mdi-account-multiple</v-icon>
          <h3 class="text-xl font-bold mt-4 mb-2">Personalized Dashboard</h3>
          <p class="text-gray-700">
            Stay organized with personalized dashboards that provide at-a-glance insights into academic progress,
            upcoming events, and tasks. Customize your dashboard to fit your unique needs and preferences.
          </p>
        </v-card>
      </v-col>
      <v-col cols="12" md="4" class="d-flex">
        <v-card class="pa-6 text-center flex-grow-1 hover-elevation">
          <v-icon size="64" color="primary">mdi-brain</v-icon>
          <h3 class="text-xl font-bold mt-4 mb-2">AI-Powered Insights</h3>
          <p class="text-gray-700">
            Leverage advanced AI tools to track progress, get personalized learning suggestions, and optimize your study
            efforts. Our AI algorithms analyze your performance and provide actionable insights to help you improve.
          </p>
        </v-card>
      </v-col>
      <v-col cols="12" md="4" class="d-flex">
        <v-card class="pa-6 text-center flex-grow-1 hover-elevation">
          <v-icon size="64" color="primary">mdi-lock</v-icon>
          <h3 class="text-xl font-bold mt-4 mb-2">Robust Security</h3>
          <p class="text-gray-700">
            Protect your academic data with state-of-the-art encryption and secure access protocols, ensuring complete
            privacy and control. Our platform is designed with security in mind to keep your information safe.
          </p>
        </v-card>
      </v-col>
    </v-row>

    <!-- Benefits Section -->
    <v-row class="mb-12">
      <v-col cols="12" class="text-center">
        <h2 class="text-3xl font-bold mb-6 word-color">Why Choose StudentPortfolio?</h2>
        <p class="text-lg text-gray-700 mb-6">
          Whether you're a student, educator, or administrator, StudentPortfolio empowers you to achieve your goals with
          ease.
        </p>
      </v-col>
      <v-col cols="12" md="4" class="d-flex">
        <v-card class="pa-6 text-center flex-grow-1 hover-elevation">
          <v-icon size="64" color="primary">mdi-school</v-icon>
          <h3 class="text-xl font-bold mt-4 mb-2">For Students</h3>
          <p class="text-gray-700">
            Centralized portfolios, AI-driven academic support, collaboration tools, and event management all in one
            place. Enhance your learning experience and stay on top of your academic journey.
          </p>
        </v-card>
      </v-col>
      <v-col cols="12" md="4" class="d-flex">
        <v-card class="pa-6 text-center flex-grow-1 hover-elevation">
          <v-icon size="64" color="primary">mdi-account-tie</v-icon>
          <h3 class="text-xl font-bold mt-4 mb-2">For Educators</h3>
          <p class="text-gray-700">
            Manage student portfolios, provide feedback, and offer real-time academic support and event recommendations.
            Streamline your teaching process and enhance student engagement.
          </p>
        </v-card>
      </v-col>
      <v-col cols="12" md="4" class="d-flex">
        <v-card class="pa-6 text-center flex-grow-1 hover-elevation">
          <v-icon size="64" color="primary">mdi-account-cog</v-icon>
          <h3 class="text-xl font-bold mt-4 mb-2">For Administrators</h3>
          <p class="text-gray-700">
            Easily monitor user activity, track progress, and maintain system security with advanced admin controls.
            Ensure smooth operation and data integrity across the platform.
          </p>
        </v-card>
      </v-col>
    </v-row>

    <!-- Technical Stack Section -->
    <v-row class="mb-12">
      <v-col cols="12" class="text-center">
        <h2 class="text-3xl font-bold mb-6 word-color">Our Technology Stack</h2>
        <p class="text-lg text-gray-700 mb-6">
          Built on modern technologies to ensure reliability, scalability, and performance.
        </p>
      </v-col>
      <v-col cols="12" md="6" class="d-flex">
        <v-card class="pa-6 text-center flex-grow-1 hover-elevation">
          <v-icon size="64" color="primary">mdi-vuejs</v-icon>
          <h3 class="text-xl font-bold mt-4 mb-2">Frontend</h3>
          <p class="text-gray-700">
            Vue.js with Vuetify provides a rich, dynamic, and responsive user interface that’s intuitive and easy to
            use. Enjoy a seamless and engaging user experience across all devices.
          </p>
        </v-card>
      </v-col>
      <v-col cols="12" md="6" class="d-flex">
        <v-card class="pa-6 text-center flex-grow-1 hover-elevation">
          <v-icon size="64" color="primary">mdi-flask</v-icon>
          <h3 class="text-xl font-bold mt-4 mb-2">Backend</h3>
          <p class="text-gray-700">
            Flask provides a lightweight, flexible backend while SQLite ensures fast, local database operations. Our
            backend architecture is designed for efficiency and scalability.
          </p>
        </v-card>
      </v-col>
    </v-row>

    <!-- Call to Action Section -->
    <v-row class="mb-12">
      <v-col cols="12" class="text-center">
        <h2 class="text-3xl font-bold mb-6 word-color">Ready to Take Control of Your Journey?</h2>
        <p class="text-lg text-gray-700 mb-6">
          Join StudentPortfolio today and streamline your academic and professional growth with ease!
        </p>
        <v-btn to="/register" color="primary" large>Sign Up Now</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "EnhancedAboutPage",
};
</script>

<style scoped>
.word-color {
  color: #0097a7;
}

p {
  text-align: justify;
  margin: 8px;
  padding: 4px;
}

</style>
