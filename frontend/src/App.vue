<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar app :color="navbarColor" :dark="isDarkTheme">
      <v-toolbar-title class="headline font-weight-bold text-uppercase">
        Student Portfolio
      </v-toolbar-title>
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

        <!-- About Button -->
        <v-btn to="/about" class="text-white mx-2">
          <v-icon left>mdi-book</v-icon>
          About
        </v-btn>

        <!-- Admin Dropdown -->
        <v-menu v-if="userRole === 'admin' || userRole === 'supervisor'" open-on-hover>
          <template v-slot:activator="{ props }">
            <v-btn v-bind="props" class="text-white mx-2">
              <v-icon left>mdi-account-arrow-down</v-icon>
              Manage
              <v-icon right>mdi-menu-down</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item to="/students">
              <v-list-item-icon><v-icon>mdi-account-school</v-icon></v-list-item-icon>
              <v-list-item-content> Students</v-list-item-content>
            </v-list-item>
            <v-list-item to="/supervisors">
              <v-list-item-icon><v-icon>mdi-account-tie</v-icon></v-list-item-icon>
              <v-list-item-content> Supervisors</v-list-item-content>
            </v-list-item>
            <v-list-item v-if="userRole === 'admin'" to="/admins">
              <v-list-item-icon><v-icon>mdi-account-multiple</v-icon></v-list-item-icon>
              <v-list-item-content> Admins</v-list-item-content>
            </v-list-item>
          </v-list>
        </v-menu>

        <!-- Chat Button (Visible to Students) -->
        <v-btn v-if="userRole === 'student'" to="/chat" class="text-white mx-2">
          <v-icon left>mdi-chat</v-icon>
          Chat
        </v-btn>

        <!-- User Dropdown (Inbox, Events, Account) -->
        <v-menu v-if="isAuthenticated" open-on-hover>
          <template v-slot:activator="{ props }">
            <v-btn v-bind="props" class="text-white mx-2">
              <v-icon left>mdi-account-circle</v-icon>
              Profile
              <v-icon right>mdi-menu-down</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item v-if="userEmail" :to="`/inbox/${userEmail}`">
              <v-list-item-icon><v-icon>mdi-email</v-icon></v-list-item-icon>
              <v-list-item-content> Inbox</v-list-item-content>
            </v-list-item>
            <v-list-item to="/events">
              <v-list-item-icon><v-icon>mdi-party-popper</v-icon></v-list-item-icon>
              <v-list-item-content> Events</v-list-item-content>
            </v-list-item>
            <v-list-item :to="`/user/${userRole}/${userId}`">
              <v-list-item-icon><v-icon>mdi-account</v-icon></v-list-item-icon>
              <v-list-item-content> Account</v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
            <!-- Logout Button with Red Color and Pointer Cursor -->
            <v-list-item v-if="isAuthenticated" @click="logout" class="logout-item">
              <v-list-item-icon><v-icon>mdi-logout</v-icon></v-list-item-icon>
              <v-list-item-content> Logout</v-list-item-content>
            </v-list-item>
          </v-list>
        </v-menu>

        <!-- Login Button -->
        <v-btn v-if="!isAuthenticated" to="/login" class="text-white mx-2">
          <v-icon left>mdi-login</v-icon>
          Login
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
          <v-list-item-content> Home</v-list-item-content>
        </v-list-item>

        <!-- About Link -->
        <v-list-item to="/about">
          <v-list-item-icon><v-icon left>mdi-book</v-icon></v-list-item-icon>
          <v-list-item-content> About</v-list-item-content>
        </v-list-item>

        

        <!-- Admin Links -->
        <v-list-item v-if="userRole === 'admin' || userRole === 'supervisor'" to="/students">
          <v-list-item-icon><v-icon>mdi-account-school</v-icon></v-list-item-icon>
          <v-list-item-content> Students</v-list-item-content>
        </v-list-item>

        <v-list-item v-if="userRole === 'admin' || userRole === 'supervisor'" to="/supervisors">
          <v-list-item-icon><v-icon>mdi-account-tie</v-icon></v-list-item-icon>
          <v-list-item-content> Supervisors</v-list-item-content>
        </v-list-item>

        <v-list-item v-if="userRole === 'admin'" to="/admins">
          <v-list-item-icon><v-icon>mdi-account-multiple</v-icon></v-list-item-icon>
          <v-list-item-content> Admins</v-list-item-content>
        </v-list-item>

        <!-- Chat Link (Visible to Students) -->
        <v-list-item v-if="userRole === 'student'" to="/chat">
          <v-list-item-icon><v-icon>mdi-chat</v-icon></v-list-item-icon>
          <v-list-item-content> Chat</v-list-item-content>
        </v-list-item>

        <!-- Login/Register Links -->
        <v-list-item v-if="!isAuthenticated" to="/login">
          <v-list-item-icon><v-icon>mdi-login</v-icon></v-list-item-icon>
          <v-list-item-content> Login</v-list-item-content>
        </v-list-item>
        <v-list-item v-if="!isAuthenticated" to="/register">
          <v-list-item-icon><v-icon>mdi-account-plus</v-icon></v-list-item-icon>
          <v-list-item-content> Register</v-list-item-content>
        </v-list-item>

        <!-- Inbox Link -->
        <v-list-item v-if="isAuthenticated && userEmail" :to="`/inbox/${userEmail}`">
          <v-list-item-icon><v-icon>mdi-email</v-icon></v-list-item-icon>
          <v-list-item-content> Inbox</v-list-item-content>
        </v-list-item>

        <!-- Events Link -->
        <v-list-item v-if="isAuthenticated" to="/events">
          <v-list-item-icon><v-icon>mdi-party-popper</v-icon></v-list-item-icon>
          <v-list-item-content> Events</v-list-item-content>
        </v-list-item>

        <!-- Account Link -->
        <v-list-item v-if="isAuthenticated" :to="`/user/${userRole}/${userId}`">
          <v-list-item-icon><v-icon>mdi-account</v-icon></v-list-item-icon>
          <v-list-item-content> Account</v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <!-- Logout Link -->
        <v-list-item v-if="isAuthenticated" @click="logout" class="logout-item">
          <v-list-item-icon><v-icon>mdi-logout</v-icon></v-list-item-icon>
          <v-list-item-content> Logout</v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main :style="{ backgroundColor: themeColors.background, color: themeColors.onBackground }">
      <router-view></router-view>
    </v-main>

    <!-- Footer -->
    <v-footer :color="footerColor" :dark="isDarkTheme" padless>
      <v-col class="text-center headline font-weight-bold text-uppercase" cols="12">
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
      isAuthenticated: false,
      userRole: null,
      userId: null,
      userEmail: null,
    };
  },
  computed: {
    themeIcon() {
      return this.isDarkTheme ? 'mdi-weather-sunny' : 'mdi-weather-night';
    },
    isDarkTheme() {
      return this.$vuetify.theme.global.dark;
    },
    navbarColor() {
      return this.isDarkTheme ? 'primary' : 'primary';
    },
    footerColor() {
      return this.isDarkTheme ? 'primary' : 'primary';
    },
    themeColors() {
      return this.$vuetify.theme.global.current.colors;
    },
  },
  methods: {
    toggleTheme() {
      const currentTheme = this.$vuetify.theme.global.name;
      this.$vuetify.theme.global.name = currentTheme === 'light' ? 'dark' : 'light';
    },
    logout() {
      this.isAuthenticated = false;
      this.userRole = null;
      this.userId = null;
      localStorage.removeItem('token');
      localStorage.removeItem('userRole');
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('userId');
      this.$router.push('/login');
    },
  },
  mounted() {
    const storedToken = localStorage.getItem('token');
    const storedRole = localStorage.getItem('userRole');
    const storedUserId = localStorage.getItem('userId');
    const storedEmail = localStorage.getItem('email');
    if (storedToken && storedRole && storedUserId) {
      this.isAuthenticated = true;
      this.userRole = storedRole;
      this.userId = storedUserId;
      this.userEmail = storedEmail;
    }
    console.log('Stored User ID:', storedUserId);
  },
};
</script>

<style>
.word-color {
  color: #0097a7;
}

/* Custom Styles for Logout Item */
.logout-item {
  cursor: pointer; /* Change cursor to pointer on hover */
}

.logout-item:hover {
  background-color: #ffebee; /* Light red background on hover */
}

.logout-item .v-list-item__content {
  color: #ff5252; /* Red text color */
}

.logout-item .v-icon {
  color: #ff5252; /* Red icon color */
}

</style>