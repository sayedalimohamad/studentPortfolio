<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar app :color="navbarColor" :dark="isDarkTheme">
      <v-toolbar-title>Student Portfolio</v-toolbar-title>
      <v-spacer></v-spacer>

      <!-- Hamburger Menu for Small Screens -->
      <v-app-bar-nav-icon @click="drawer = !drawer" class="d-sm-none"></v-app-bar-nav-icon>

      <!-- Navigation Buttons for Larger Screens -->
      <div class="d-none d-sm-flex">
        <!-- Home Button -->
        <v-btn to="/" class="text-white mx-2">
          <v-icon left>mdi-home</v-icon>
          Home
        </v-btn>

        <!-- Students Link (Visible to Admins) -->
        <v-btn v-if="userRole === 'admin'" to="/students" class="text-white mx-2">
          <v-icon left>mdi-account-group</v-icon>
          Students
        </v-btn>

        <!-- Chat Link (Visible to Students) -->
        <v-btn v-if="userRole === 'student'" to="/chat" class="text-white mx-2">
          <v-icon left>mdi-chat</v-icon>
          Chat
        </v-btn>

        <!-- Dropdown for Login/Register or Logout -->
        <v-menu v-if="!isAuthenticated" offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn class="text-white mx-2" v-bind="attrs" v-on="on">
              <v-icon left>mdi-account</v-icon>
              Account
            </v-btn>
          </template>
          <v-list>
            <v-list-item to="/login">
              <v-list-item-icon><v-icon>mdi-login</v-icon></v-list-item-icon>
              <v-list-item-title>Login</v-list-item-title>
            </v-list-item>
            <v-list-item to="/register">
              <v-list-item-icon><v-icon>mdi-account-plus</v-icon></v-list-item-icon>
              <v-list-item-title>Register</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

        <!-- Logout Button (Visible to Authenticated Users) -->
        <v-btn v-if="isAuthenticated" @click="logout" class="text-dark font-weight-bold mx-2" variant="flat">
          <v-icon left>mdi-logout</v-icon>
          Logout
        </v-btn>
      </div>

      <!-- Theme Toggle Button -->
      <v-btn @click="toggleTheme" icon>
        <v-icon>{{ themeIcon }}</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Navigation Drawer for Small Screens -->
    <v-navigation-drawer v-model="drawer" app temporary class="d-sm-none">
      <v-list>
        <!-- Home Link -->
        <v-list-item to="/">
          <v-list-item-icon><v-icon>mdi-home</v-icon></v-list-item-icon>
          <v-list-item-content>Home</v-list-item-content>
        </v-list-item>

        <!-- Students Link (Visible to Admins) -->
        <v-list-item v-if="userRole === 'admin'" to="/students">
          <v-list-item-icon><v-icon>mdi-account-group</v-icon></v-list-item-icon>
          <v-list-item-content>Students</v-list-item-content>
        </v-list-item>

        <!-- Chat Link (Visible to Students) -->
        <v-list-item v-if="userRole === 'student'" to="/chat">
          <v-list-item-icon><v-icon>mdi-chat</v-icon></v-list-item-icon>
          <v-list-item-content>Chat</v-list-item-content>
        </v-list-item>

        <!-- Login Link (Visible to Unauthenticated Users) -->
        <v-list-item v-if="!isAuthenticated" to="/login">
          <v-list-item-icon><v-icon>mdi-login</v-icon></v-list-item-icon>
          <v-list-item-content>Login</v-list-item-content>
        </v-list-item>

        <!-- Register Link (Visible to Unauthenticated Users) -->
        <v-list-item v-if="!isAuthenticated" to="/register">
          <v-list-item-icon><v-icon>mdi-account-plus</v-icon></v-list-item-icon>
          <v-list-item-content>Register</v-list-item-content>
        </v-list-item>

        <!-- Logout Link (Visible to Authenticated Users) -->
        <v-list-item v-if="isAuthenticated" @click="logout">
          <v-list-item-icon><v-icon>mdi-logout</v-icon></v-list-item-icon>
          <v-list-item-content>Logout</v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <router-view></router-view>
    </v-main>

    <!-- Footer -->
    <v-footer :color="footerColor" :dark="isDarkTheme" padless>
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
      drawer: false, // Controls the visibility of the navigation drawer
      isAuthenticated: false, // Tracks authentication status
      userRole: null, // Tracks the user's role (admin, student, supervisor)
    };
  },
  computed: {
    // Dynamically determine the theme icon
    themeIcon() {
      return this.isDarkTheme ? 'mdi-weather-sunny' : 'mdi-weather-night';
    },
    // Check if the theme is dark
    isDarkTheme() {
      return this.$vuetify.theme.global.dark;
    },
    // Navbar color based on theme
    navbarColor() {
      return this.isDarkTheme ? 'onBackground' : 'primary';
    },
    // Footer color based on theme
    footerColor() {
      return this.isDarkTheme ? 'onBackground' : 'primary';
    },
  },
  methods: {
    // Toggle between light and dark themes
    toggleTheme() {
      this.$vuetify.theme.global.dark = !this.$vuetify.theme.global.dark;
    },
    // Logout method
    logout() {
      // Clear user session
      this.isAuthenticated = false;
      this.userRole = null;
      localStorage.removeItem('userRole');
      localStorage.removeItem('isAuthenticated');
      // Redirect to login page
      this.$router.push('/login');
    },
    // Simulate login 
    async login(credentials) {
      try {
        // Send login request to the backend
        const response = await axios.post('/api/users/login', credentials);
        const { access_token, role } = response.data;

        // Update authentication state
        this.isAuthenticated = true;
        this.userRole = role;
        localStorage.setItem('userRole', role);
        localStorage.setItem('isAuthenticated', true);
        localStorage.setItem('access_token', access_token);

        // Redirect based on the user's role
        if (role === 'admin') {
          this.$router.push('/admin-dashboard');
        } else if (role === 'student') {
          this.$router.push('/student-profile');
        } else if (role === 'supervisor') {
          this.$router.push('/supervisor-profile');
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.error = 'Invalid email or password';
        } else {
          this.error = 'An error occurred during login';
        }
      }
    },
  },
  mounted() {
  // Check authentication status on app load 
  const storedToken = localStorage.getItem('token');
  const storedRole = localStorage.getItem('userRole');
  if (storedToken && storedRole) {
    this.isAuthenticated = true;
    this.userRole = storedRole;
  }
},
methods: {
  logout() {
    // Clear user session
    this.isAuthenticated = false;
    this.userRole = null;
    localStorage.removeItem('userRole');
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('token'); // Clear the token
    // Redirect to login page
    this.$router.push('/login');
  },
},
};
</script>

<style>
/* Add custom Tailwind classes or styles here */
.word-color {
  color: #0097a7;
  /* Custom accent color */
}
</style>