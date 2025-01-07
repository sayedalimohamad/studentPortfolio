import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import '@mdi/font/css/materialdesignicons.css'; // Ensure you are using css-loader

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light', // Initial default theme
    themes: {
      light: {
        dark: false, // Explicitly mark this as a light theme
        colors: {
          primary: '#00ACC1', // Darker cyan
          secondary: '#80DEEA', // Lighter cyan
          accent: '#FF6F00', // Vibrant orange
          error: '#D32F2F', // Red for errors
          info: '#0097A7', // Dark cyan for info
          success: '#43A047', // Green for success
          warning: '#FFA000', // Amber for warnings
          background: '#E0F7FA', // Base background color
          surface: '#FFFFFF', // White for surfaces
          onPrimary: '#FFFFFF', // White text on primary
          onSecondary: '#000000', // Black text on secondary
          onBackground: '#000000', // Black text on background
          onSurface: '#000000', // Black text on surface
        },
      },
      dark: {
        dark: true, // Explicitly mark this as a dark theme
        colors: {
          primary: '#00ACC1', // Darker cyan
          secondary: '#80DEEA', // Lighter cyan
          accent: '#FF6F00', // Vibrant orange
          error: '#D32F2F', // Red for errors
          info: '#0097A7', // Dark cyan for info
          success: '#43A047', // Green for success
          warning: '#FFA000', // Amber for warnings
          background: '#121212', // Dark background
          surface: '#1E1E1E', // Slightly lighter surface
          onPrimary: '#000000', // Black text on primary
          onSecondary: '#000000', // Black text on secondary
          onBackground: '#FFFFFF', // White text on background
          onSurface: '#FFFFFF', // White text on surface
        },
      },
    },
  },
});