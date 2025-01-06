<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar
      app
      :color="$vuetify.theme.global.dark ? 'primary' : 'primary'"
      :dark="$vuetify.theme.global.dark"
    >
      <v-toolbar-title>Student Portfolio</v-toolbar-title>
      <v-spacer></v-spacer>
      
      <!-- Hamburger Menu for Small Screens -->
      <v-app-bar-nav-icon @click="drawer = !drawer" class="d-sm-none"></v-app-bar-nav-icon>
      
      <!-- Navigation Buttons for Larger Screens -->
      <div class="d-none d-sm-flex">
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
      </div>
      
      <v-btn @click="toggleTheme" icon>
        <v-icon>{{ themeIcon }}</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Navigation Drawer for Small Screens -->
    <v-navigation-drawer
      v-model="drawer"
      app
      temporary
      class="d-sm-none"
    >
      <v-list>
        <v-list-item to="/">
          <v-list-item-icon><v-icon>mdi-home</v-icon></v-list-item-icon>
          <v-list-item-content>Home</v-list-item-content>
        </v-list-item>
        <v-list-item to="/students">
          <v-list-item-icon><v-icon>mdi-account-group</v-icon></v-list-item-icon>
          <v-list-item-content>Students</v-list-item-content>
        </v-list-item>
        <v-list-item to="/admins">
          <v-list-item-icon><v-icon>mdi-account-tie</v-icon></v-list-item-icon>
          <v-list-item-content>Admins</v-list-item-content>
        </v-list-item>
        <v-list-item to="/login">
          <v-list-item-icon><v-icon>mdi-account-tie</v-icon></v-list-item-icon>
          <v-list-item-content>Login</v-list-item-content>
        </v-list-item>
        <v-list-item to="/register">
          <v-list-item-icon><v-icon>mdi-account-plus</v-icon></v-list-item-icon>
          <v-list-item-content>Register</v-list-item-content>
        </v-list-item>
        <v-list-item to="/chat">
          <v-list-item-icon><v-icon>mdi-chat</v-icon></v-list-item-icon>
          <v-list-item-content>Chat</v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <router-view></router-view>
    </v-main>

    <!-- Footer -->
    <v-footer
      :color="$vuetify.theme.global.dark ? 'primary' : 'primary'"
      :dark="$vuetify.theme.global.dark"
      padless
    >
      <v-col class="text-center" cols="12">
        &copy; {{ new Date().getFullYear() }} — Student Portfolio
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      drawer: false,
    };
  },
  computed: {
    // Dynamically determine the icon based on the current theme
    themeIcon() {
      return this.$vuetify.theme.global.dark ? 'mdi-weather-sunny' : 'mdi-weather-night';
    },
  },
  methods: {
    // Toggle between light and dark themes
    toggleTheme() {
      this.$vuetify.theme.global.dark = !this.$vuetify.theme.global.dark;
    },
  },
};
</script>

<style>
/* Add custom Tailwind classes or styles here */
</style>
