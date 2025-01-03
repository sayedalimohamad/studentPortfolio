import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light', // or 'dark'
    themes: {
      light: {
        primary: '#1976D2', // Default Vuetify primary color
      },
      dark: {
        primary: '#2196F3', // A lighter shade for dark theme
      },
    },
  },
});