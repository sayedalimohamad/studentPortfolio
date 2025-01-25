<template>
  <v-container class="py-12">
    <v-row class="mb-8">
      <v-col cols="12" class="text-center">
        <h1 class="text-3xl font-bold word-color">Events</h1>
        <p class="text-lg text-gray-700 mt-2">Manage and view events here.</p>
      </v-col>
    </v-row>

    <!-- Create Event Button (Only for Admins/Supervisors) -->
    <v-row v-if="userRole === 'admin' || userRole === 'supervisor'" class="mb-8">
      <v-col cols="12" class="text-right">
        <v-btn color="primary" dark @click="showCreateEventModal = true">
          <v-icon left>mdi-plus</v-icon>
          Create Event
        </v-btn>
      </v-col>
    </v-row>

    <!-- Events Table -->
    <v-card v-if="events.length > 0" class="mx-auto" max-width="1200">
      <v-card-text class="pa-6">
        <v-table>
          <thead>
            <tr>
              <th class="text-left pa-4">Title</th>
              <th class="text-left pa-4">Description</th>
              <th class="text-left pa-4">Date</th>
              <th class="text-left pa-4">Location</th>
              <th class="text-left pa-4" v-if="userRole === 'admin' || userRole === 'supervisor'">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="event in events" :key="event.event_id">
              <td class="font-bold word-color pa-4">{{ event.title }}</td>
              <td class="text-gray-700 pa-4">{{ event.description }}</td>
              <td class="text-gray-700 pa-4">
                <v-icon small>mdi-calendar</v-icon>
                {{ new Date(event.date).toDateString() }}
              </td>
              <td class="text-gray-700 pa-4">
                <v-icon small>mdi-map-marker</v-icon>
                {{ event.location }}
              </td>
              <td class="pa-4">
                <v-btn v-if="userRole === 'admin' || userRole === 'supervisor' || event.user_id === userId" icon @click="editEvent(event)" class="mb-2">
                  <v-icon color="primary">mdi-pencil</v-icon>
                </v-btn>
                <v-btn v-if="userRole === 'admin' || userRole === 'supervisor' || event.user_id === userId" icon @click="deleteEvent(event.event_id)">
                  <v-icon color="red">mdi-delete</v-icon>
                </v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>

    <!-- Loading and Error Messages -->
    <v-alert v-if="loading" type="info" class="mt-8">Loading events...</v-alert>
    <v-alert v-if="error" type="error" class="mt-8">{{ error }}</v-alert>

    <!-- Create Event Modal -->
    <v-dialog v-model="showCreateEventModal" max-width="600">
      <v-card>
        <v-card-title class="headline pa-6">
          <v-icon color="primary" left>mdi-plus</v-icon>
          Create Event
        </v-card-title>
        <v-card-text class="pa-6">
          <v-form ref="createEventForm" v-model="createEventFormValid">
            <v-text-field v-model="newEvent.title" label="Title" required outlined dense class="mb-4"></v-text-field>
            <v-text-field v-model="newEvent.description" label="Description" required outlined dense class="mb-4"></v-text-field>
            <v-text-field v-model="newEvent.date" label="Date" type="date" required outlined dense class="mb-4"></v-text-field>
            <v-text-field v-model="newEvent.location" label="Location" required outlined dense class="mb-4"></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions class="pa-6">
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="showCreateEventModal = false">
            <v-icon left>mdi-cancel</v-icon>
            Cancel
          </v-btn>
          <v-btn color="green darken-1" text @click="createEvent">
            <v-icon left>mdi-check</v-icon>
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Edit Event Modal -->
    <v-dialog v-model="showEditEventModal" max-width="600">
      <v-card>
        <v-card-title class="headline pa-6">
          <v-icon color="primary" left>mdi-pencil</v-icon>
          Edit Event
        </v-card-title>
        <v-card-text class="pa-6">
          <v-form ref="editEventForm" v-model="editEventFormValid">
            <v-text-field v-model="editedEvent.title" label="Title" required outlined dense class="mb-4"></v-text-field>
            <v-text-field v-model="editedEvent.description" label="Description" required outlined dense class="mb-4"></v-text-field>
            <v-text-field v-model="editedEvent.date" label="Date" type="date" required outlined dense class="mb-4"></v-text-field>
            <v-text-field v-model="editedEvent.location" label="Location" required outlined dense class="mb-4"></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions class="pa-6">
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="showEditEventModal = false">
            <v-icon left>mdi-cancel</v-icon>
            Cancel
          </v-btn>
          <v-btn color="green darken-1" text @click="updateEvent">
            <v-icon left>mdi-check</v-icon>
            Save Changes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default {
  name: 'EventsView',
  data() {
    return {
      events: [],
      loading: true,
      error: null,
      userRole: localStorage.getItem('userRole'),
      userId: localStorage.getItem('userId'),
      showCreateEventModal: false,
      showEditEventModal: false,
      createEventFormValid: false,
      editEventFormValid: false,
      newEvent: {
        title: '',
        description: '',
        date: '',
        location: '',
      },
      editedEvent: {
        event_id: null,
        title: '',
        description: '',
        date: '',
        location: '',
      },
    };
  },
  async created() {
    await this.fetchEvents();
  },
  methods: {
    async fetchEvents() {
      const storedAuth = localStorage.getItem('token');
      try {
        const response = await axios.get('/api/events/', {
          headers: { Authorization: `Bearer ${storedAuth}` },
        });
        this.events = response.data;
      } catch (error) {
        console.error('Error fetching events:', error);
        this.error = 'Failed to load events.';
        useToast().error(this.error);
      } finally {
        this.loading = false;
      }
    },
    async createEvent() {
      if (!this.createEventFormValid) {
        this.error = 'Please fill in all required fields.';
        useToast().error(this.error);
        return;
      }

      const storedAuth = localStorage.getItem('token');
      try {
        const response = await axios.post('/api/events/', this.newEvent, {
          headers: { Authorization: `Bearer ${storedAuth}` },
        });
        this.events.push(response.data);
        this.showCreateEventModal = false;
        useToast().success('Event created successfully.');
      } catch (error) {
        console.error('Error creating event:', error);
        this.error = 'Failed to create event.';
        useToast().error(this.error);
      }
    },
    editEvent(event) {
      this.editedEvent = { ...event };
      this.showEditEventModal = true;
    },
    async updateEvent() {
      if (!this.editEventFormValid) {
        this.error = 'Please fill in all required fields.';
        useToast().error(this.error);
        return;
      }

      const storedAuth = localStorage.getItem('token');
      try {
        await axios.put(`/api/events/${this.editedEvent.event_id}`, this.editedEvent, {
          headers: { Authorization: `Bearer ${storedAuth}` },
        });
        await this.fetchEvents();
        this.showEditEventModal = false;
        useToast().success('Event updated successfully.');
      } catch (error) {
        console.error('Error updating event:', error);
        this.error = 'Failed to update event.';
        useToast().error(this.error);
      }
    },
    async deleteEvent(eventId) {
      const storedAuth = localStorage.getItem('token');
      try {
        await axios.delete(`/api/events/${eventId}`, {
          headers: { Authorization: `Bearer ${storedAuth}` },
        });
        this.events = this.events.filter((event) => event.event_id !== eventId);
        useToast().success('Event deleted successfully.');
      } catch (error) {
        console.error('Error deleting event:', error);
        this.error = 'Failed to delete event.';
        useToast().error(this.error);
      }
    },
  },
};
</script>

<style scoped>
.word-color {
  color: #0097a7;
}
</style>