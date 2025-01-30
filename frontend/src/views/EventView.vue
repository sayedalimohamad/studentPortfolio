<template>
  <v-container class="py-12">
    <v-row class="mb-8">
      <v-col cols="12" class="text-left">
        <h1 class="text-3xl font-bold word-color">Events ({{ filteredEvents.length }})</h1>
        <p class="text-lg text-gray-700 mt-2">
          <span v-if="userRole === 'admin' || userRole === 'supervisor'">Manage and view events here.</span>
          <span v-else>View upcoming events here.</span>
        </p>
      </v-col>
    </v-row>

    <!-- Search Bar and Status Filter (Only for Admins/Supervisors) -->
    <v-row class="mb-6">
      <v-col cols="12" :md="userRole === 'admin' || userRole === 'supervisor' ? 6 : 12">
        <v-text-field v-model="searchQuery" label="Search by title, description, location, or status"
          prepend-inner-icon="mdi-magnify" outlined dense></v-text-field>
      </v-col>
      <v-col cols="12" md="6" v-if="userRole === 'admin' || userRole === 'supervisor'">
        <v-select v-model="statusFilter" :items="statusOptions" label="Filter by Status" prepend-inner-icon="mdi-filter"
          outlined dense clearable></v-select>
      </v-col>
    </v-row>

    <!-- Create Event Button  -->
    <v-row  class="mb-8">
      <v-col cols="12" class="text-right">
        <v-btn color="primary" dark @click="showCreateEventModal = true">
          <v-icon left>mdi-plus</v-icon>
          Create Event
        </v-btn>
      </v-col>
    </v-row>

    <!-- Events Table -->
    <v-card v-if="filteredEvents.length > 0" class="mx-auto" max-width="1200">
      <v-card-text class="pa-6">
        <v-table>
          <thead>
            <tr>
              <th class="text-left pa-4">Title</th>
              <th class="text-left pa-4">Description</th>
              <th class="text-left pa-4">Date</th>
              <th class="text-left pa-4">Location</th>
              <th class="text-left pa-4" v-if="userRole === 'admin' || userRole === 'supervisor'">Status</th>
              <th class="text-left pa-4" v-if="userRole === 'admin' || userRole === 'supervisor'">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="event in filteredEvents" :key="event.event_id">
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
              <td class="text-gray-700 pa-4" v-if="userRole === 'admin' || userRole === 'supervisor'">
                <v-chip :color="getStatusColor(event.status)" small>
                  {{ event.status }}
                </v-chip>
              </td>
              <td class="pa-4">
                <v-btn v-if="userRole === 'admin' || userRole === 'supervisor'" icon
                  @click="openStatusUpdateModal(event)" class="mb-2" title="Status Update">
                  <v-icon color="warning">mdi-list-status</v-icon>
                </v-btn>
                <v-btn v-if="userRole === 'admin' || userRole === 'supervisor' || event.user_id === userId" icon
                  @click="editEvent(event)" class="mb-2" title="Edit Event">
                  <v-icon color="primary">mdi-pencil</v-icon>
                </v-btn>
                <v-btn v-if="userRole === 'admin' || userRole === 'supervisor' || event.user_id === userId" icon
                  @click="showDeleteConfirmation(event.event_id)" title="Delete Event">
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
    <v-alert v-else-if="filteredEvents.length === 0" type="info" class="mt-8">No events found.</v-alert>

    <!-- Add the Spinner Here -->
    <div v-if="loading" class="loading-overlay">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </div>

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
            <v-text-field v-model="newEvent.description" label="Description" required outlined dense
              class="mb-4"></v-text-field>
            <v-text-field v-model="newEvent.date" label="Date" type="date" required outlined dense
              class="mb-4"></v-text-field>
            <v-text-field v-model="newEvent.location" label="Location" required outlined dense
              class="mb-4"></v-text-field>
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
            <v-text-field v-model="editedEvent.description" label="Description" required outlined dense
              class="mb-4"></v-text-field>
            <v-text-field v-model="editedEvent.date" label="Date" type="date" required outlined dense
              class="mb-4"></v-text-field>
            <v-text-field v-model="editedEvent.location" label="Location" required outlined dense
              class="mb-4"></v-text-field>
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

    <!-- Delete Confirmation Modal -->
    <v-dialog v-model="showDeleteConfirmationModal" max-width="400">
      <v-card>
        <v-card-title class="headline pa-6">Confirm Deletion</v-card-title>
        <v-card-text class="pa-6">
          Are you sure you want to delete this event?
        </v-card-text>
        <v-card-actions class="pa-6">
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="showDeleteConfirmationModal = false">
            <v-icon left>mdi-cancel</v-icon>
            Cancel
          </v-btn>
          <v-btn color="red darken-1" text @click="confirmDeleteEvent">
            <v-icon left>mdi-delete</v-icon>
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Status Update Modal -->
    <v-dialog v-model="showStatusUpdateModal" max-width="400">
      <v-card>
        <v-card-title class="headline pa-6">
          <v-icon color="warning" left>mdi-list-status</v-icon>
          Update Event Status
        </v-card-title>
        <v-card-text class="pa-6">
          <v-select v-model="selectedStatus" :items="statusOptions" label="Select Status" outlined dense></v-select>
        </v-card-text>
        <v-card-actions class="pa-6">
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="showStatusUpdateModal = false">
            <v-icon left>mdi-cancel</v-icon>
            Cancel
          </v-btn>
          <v-btn color="green darken-1" text @click="saveStatusUpdate">
            <v-icon left>mdi-check</v-icon>
            Save
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
      searchQuery: '',
      statusFilter: null,
      statusOptions: ['pending', 'accepted', 'rejected'],
      loading: true,
      error: null,
      userRole: localStorage.getItem('userRole'),
      userId: localStorage.getItem('userId'),
      showCreateEventModal: false,
      showEditEventModal: false,
      showDeleteConfirmationModal: false,
      showStatusUpdateModal: false,
      eventToDelete: null,
      eventToUpdateStatus: null,
      selectedStatus: null,
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
    getStatusColor(status) {
      switch (status) {
        case 'pending':
          return 'orange';
        case 'accepted':
          return 'green';
        case 'rejected':
          return 'red';
        default:
          return 'gray';
      }
    },
    openStatusUpdateModal(event) {
      this.eventToUpdateStatus = event;
      this.selectedStatus = event.status;
      this.showStatusUpdateModal = true;
    },
    async saveStatusUpdate() {
      if (!this.eventToUpdateStatus || !this.selectedStatus) {
        this.error = 'Please select a status.';
        useToast().error(this.error);
        return;
      }

      const eventId = this.eventToUpdateStatus.event_id;
      const status = this.selectedStatus;

      const storedAuth = localStorage.getItem('token');
      try {
        const response = await axios.put(`/api/events/${eventId}/status`, { status }, {
          headers: { Authorization: `Bearer ${storedAuth}` },
        });
        console.log('Backend response:', response.data);
        await this.fetchEvents();
        useToast().success('Event status updated successfully.');
        this.showStatusUpdateModal = false;
      } catch (error) {
        console.error('Error updating event status:', error);
        this.error = 'Failed to update event status.';
        useToast().error(this.error);
      }
    },
    showDeleteConfirmation(eventId) {
      this.eventToDelete = eventId;
      this.showDeleteConfirmationModal = true;
    },
    async confirmDeleteEvent() {
      if (this.eventToDelete) {
        await this.deleteEvent(this.eventToDelete);
        this.showDeleteConfirmationModal = false;
        this.eventToDelete = null;
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
  },
  computed: {
    filteredEvents() {
      let events = this.events || [];

      // Filter by status (only for admins/supervisors)
      if (this.userRole === 'admin' || this.userRole === 'supervisor') {
        if (this.statusFilter) {
          events = events.filter(event => event.status === this.statusFilter);
        }
      } else {
        // Students can only see accepted events
        events = events.filter(event => event.status === 'accepted');
      }

      // Ensure searchQuery is not null or undefined
      const query = this.searchQuery ? this.searchQuery.toLowerCase() : "";

      return events.filter(event => {
        if (!event) return false; // Ensure event is not undefined/null
        return (
          (event.title && event.title.toLowerCase().includes(query)) ||
          (event.description && event.description.toLowerCase().includes(query)) ||
          (event.location && event.location.toLowerCase().includes(query)) ||
          (event.status && event.status.toLowerCase().includes(query))
        );
      });
    },
  },
};
</script>

<style scoped>
.word-color {
  color: #0097a7;
}

/* Add the loading overlay styles */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.8);
  z-index: 9999;
}
</style>