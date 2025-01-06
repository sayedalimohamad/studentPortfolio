<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar app :color="$vuetify.theme.current.dark ? 'primary' : 'primary'" dark>
      <v-toolbar-title>Student Portfolio</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn to="/" class="text-white mx-2">
        <v-icon left>mdi-home</v-icon>
        Home
      </v-btn>
      <v-btn to="/students" class="text-white mx-2">
        <v-icon left>mdi-account-group</v-icon>
        Students
      </v-btn>
      <v-btn to="/admins" class="text-white mx-2">
        <v-icon left>mdi-account-tie</v-icon>
        Admins
      </v-btn>
      <v-btn to="/login" class="text-white mx-2">
        <v-icon left>mdi-account-tie</v-icon>
        Login
      </v-btn>
      <v-btn to="/register" class="text-white mx-2">
        <v-icon left>mdi-account-plus</v-icon>
        Register
      </v-btn>
      <v-btn to="/chat" class="text-white mx-2">
        <v-icon left>mdi-chat</v-icon>
        Chat
      </v-btn>
      <v-btn @click="toggleTheme" icon>
        <v-icon>{{ themeIcon }}</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <router-view></router-view>
    </v-main>

    <!-- Footer -->
    <v-footer :color="$vuetify.theme.current.dark ? 'primary' : 'primary'" dark padless>
      <v-col class="text-center" cols="12">
        &copy; {{ new Date().getFullYear() }} — Student Portfolio
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  computed: {
    themeIcon() {
      return this.$vuetify.theme.current.dark ? 'mdi-weather-sunny' : 'mdi-weather-night';
    },
  },
  methods: {
    toggleTheme() {
      this.$vuetify.theme.current.dark = !this.$vuetify.theme.current.dark;
    },
  },
};
</script>

<style>
/* Add custom Tailwind classes or styles here */
</style>