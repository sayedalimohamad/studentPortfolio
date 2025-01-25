<template>
  <v-container class="py-12">
    <v-row class="mb-6">
      <v-col cols="12" class="text-center">
        <h1 class="text-3xl font-bold">Events</h1>
        <p class="text-lg text-gray-700">Manage and view events here.</p>
      </v-col>
    </v-row>

    <!-- Create Event Button (Only for Admins/Supervisors) -->
    <v-row v-if="userRole === 'admin' || userRole === 'supervisor'">
      <v-col cols="12" class="text-right">
        <v-btn color="primary" dark @click="showCreateEventModal = true">
          <v-icon left>mdi-plus</v-icon>
          Create Event
        </v-btn>
      </v-col>
    </v-row>

    <!-- Events List -->
    <v-card v-if="events.length > 0" class="mx-auto" max-width="800">
      <v-card-text>
        <v-list>
          <v-list-item v-for="event in events" :key="event.event_id" class="mb-4">
            <v-list-item-content>
              <v-list-item-title class="font-bold">{{ event.title }}</v-list-item-title>
              <v-list-item-subtitle class="text-gray-700">{{ event.description }}</v-list-item-subtitle>
              <v-list-item-subtitle class="text-gray-700">
                <v-icon small>mdi-calendar</v-icon>
                {{ new Date(event.date).toDateString() }}
              </v-list-item-subtitle>
              <v-list-item-subtitle class="text-gray-700">
                <v-icon small>mdi-map-marker</v-icon>
                {{ event.location }}
              </v-list-item-subtitle>
            </v-list-item-content>

            <!-- Update and Delete Buttons (Only for Admins/Supervisors or Event Creator) -->
            <v-list-item-action v-if="userRole === 'admin' || userRole === 'supervisor' || event.user_id === userId">
              <v-btn icon @click="editEvent(event)">
                <v-icon color="primary">mdi-pencil</v-icon>
              </v-btn>
              <v-btn icon @click="deleteEvent(event.event_id)">
                <v-icon color="red">mdi-delete</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <!-- Loading and Error Messages -->
    <v-alert v-if="loading" type="info" class="mt-6">Loading events...</v-alert>
    <v-alert v-if="error" type="error" class="mt-6">{{ error }}</v-alert>

    <!-- Create Event Modal -->
    <v-dialog v-model="showCreateEventModal" max-width="600">
      <v-card>
        <v-card-title class="headline">
          <v-icon color="primary" left>mdi-plus</v-icon>
          Create Event
        </v-card-title>
        <v-card-text>
          <v-form ref="createEventForm" v-model="createEventFormValid">
            <v-text-field v-model="newEvent.title" label="Title" required outlined dense></v-text-field>
            <v-text-field v-model="newEvent.description" label="Description" required outlined dense></v-text-field>
            <v-text-field v-model="newEvent.date" label="Date" type="date" required outlined dense></v-text-field>
            <v-text-field v-model="newEvent.location" label="Location" required outlined dense></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
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
        <v-card-title class="headline">
          <v-icon color="primary" left>mdi-pencil</v-icon>
          Edit Event
        </v-card-title>
        <v-card-text>
          <v-form ref="editEventForm" v-model="editEventFormValid">
            <v-text-field v-model="editedEvent.title" label="Title" required outlined dense></v-text-field>
            <v-text-field v-model="editedEvent.description" label="Description" required outlined dense></v-text-field>
            <v-text-field v-model="editedEvent.date" label="Date" type="date" required outlined dense></v-text-field>
            <v-text-field v-model="editedEvent.location" label="Location" required outlined dense></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
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
