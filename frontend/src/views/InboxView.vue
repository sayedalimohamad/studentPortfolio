<template>
  <v-app>
    <!-- Navigation Drawer -->
    <v-navigation-drawer v-model="drawer" :width="400" class="pa-6" temporary>
      <v-list-item title="Inbox" :subtitle="storedEmail || 'No email provided'"></v-list-item>
      <v-divider></v-divider>
      <!-- Compose Email -->
      <v-list-item v-if="!isAuthenticated" to="/send-email" class="mt-4" color="primary">
        <v-icon left>mdi-pencil</v-icon>
        Compose Email
      </v-list-item>

      <!-- Navigate to Inbox -->
      <v-list-item class="mt-4 clickable-list-item" @click="showInbox">
        <v-icon left>mdi-email</v-icon>
        Inbox
      </v-list-item>

      <!-- Navigate to Sent Emails -->
      <v-list-item class="mt-4 clickable-list-item" @click="fetchSentEmails">
        <v-icon left>mdi-email-fast</v-icon>
        Sent Emails
      </v-list-item>
    </v-navigation-drawer>

    <!-- App Bar -->
    <v-app-bar color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Email App</v-toolbar-title>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <v-container class="pa-4">
        <!-- Inbox Emails -->
        <v-row v-if="!showSentEmails" class="pa-3">
          <!-- Empty state with an icon -->
          <v-col v-if="emails.length === 0 && !loading" class="text-center">
            <v-alert type="info" border="left" prominent class="empty-state-alert">
              <v-icon large color="primary">mdi-inbox</v-icon>
              <div>No emails available.</div>
            </v-alert>
          </v-col>

          <!-- Title for Inbox -->
          <v-subheader class="mt-4 text-h4 font-weight-bold ml-auto">Inbox</v-subheader>
          <v-divider class="mb-4"></v-divider>

          <!-- Display inbox email cards -->
          <v-col v-for="email in emails" :key="email.email_id" cols="12" sm="6" md="4">
            <v-card elevation="4" class="hover-card pa-3"  @click="viewEmail(email)">
              <v-card-title class="card-title">
                <v-icon left>mdi-email</v-icon>
                <span class="headline">{{ email.subject }}</span>
              </v-card-title>
              <v-card-subtitle class="card-subtitle">
                <strong>From:</strong> {{ email.sender_email }} <br />
                <strong>Received:</strong> {{ new Date(email.timestamp).toLocaleString() }}
              </v-card-subtitle>
              <v-card-text>
                {{ email.message?.slice(0, 50) || "No preview available." }}...
              </v-card-text>
              <v-card-actions>
                <v-btn @click="viewEmail(email)" color="primary" rounded><v-icon left>mdi-cube-scan</v-icon> View
                  Email</v-btn>
                <v-btn @click="showConfirmDeleteModal(email.email_id)" color="red" rounded><v-icon
                    left>mdi-delete</v-icon> Delete</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <!-- Sent Emails -->
        <v-row v-if="showSentEmails" class="pa-3 ">
          <!-- Empty state with an icon -->
          <v-col v-if="sentEmails.length === 0 && !loading" class="text-center">
            <v-alert type="info" border="left" prominent class="empty-state-alert">
              <v-icon large color="primary">mdi-email-send</v-icon>
              <div>No sent emails available.</div>
            </v-alert>
          </v-col>

          <!-- Title for Sent Emails -->
          <v-subheader  class="mt-4 text-h4 font-weight-bold ml-auto " >Sent Emails</v-subheader>
          <v-divider class="mb-4"></v-divider>

          <!-- Display sent email cards with custom color (onCard) -->
          <v-col v-for="email in sentEmails" :key="email.email_id" cols="12" sm="6" md="4">
            <v-card elevation="4" class="hover-card pa-3" color="onCard"  @click="viewEmail(email)">
              <v-card-title class="card-title">
                <v-icon left>mdi-email</v-icon>
                <span class="headline">{{ email.subject }}</span>
              </v-card-title>
              <v-card-subtitle class="card-subtitle">
                <strong>To:</strong> {{ email.recipient_email }} <br />
                <strong>Sent:</strong> {{ new Date(email.timestamp).toLocaleString() }}
              </v-card-subtitle>
              <v-card-text>
                {{ email.message?.slice(0, 50) || "No preview available." }}...
              </v-card-text>
              <v-card-actions>
                <v-btn @click="viewEmail(email)" color="primary" rounded><v-icon left>mdi-cube-scan</v-icon> View
                  Email</v-btn>
                <v-btn @click="showConfirmDeleteModal(email.email_id)" color="red" rounded><v-icon
                    left>mdi-delete</v-icon> Delete</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <!-- Loading Spinner -->
        <div v-if="loading" class="loading-overlay">
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        </div>

        <!-- Confirm Deletion Modal -->
        <v-dialog v-model="confirmDeleteDialogVisible" max-width="400px">
          <v-card>
            <v-card-title class="headline">Confirm Deletion</v-card-title>
            <v-card-text>Are you sure you want to delete this email?</v-card-text>
            <v-card-actions>
              <v-btn color="red" text @click="confirmDeletion">Yes, Delete</v-btn>
              <v-btn color="primary" text @click="cancelDeletion">Cancel</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Email Details Modal -->
        <v-dialog v-model="emailDialogVisible" max-width="800px">
          <v-card class="modal-card pa-4">
            <v-card-title>
              <v-btn icon @click="closeEmailDialog" class="float-right close-btn" color="red">
                <v-icon>mdi-close</v-icon>
              </v-btn>
              <v-icon left>mdi-email</v-icon>
              <span>{{ selectedEmail?.subject }}</span>
            </v-card-title>
            <v-card-subtitle class="modal-card-subtitle">
              <strong>From:</strong> {{ selectedEmail?.sender_email }} <br />
              <strong>To:</strong> {{ selectedEmail?.recipient_email }} <br />
              <strong>Received:</strong> {{ new Date(selectedEmail?.timestamp).toLocaleString() }}
            </v-card-subtitle>
            <v-card-text class="modal-card-text">
              <pre>{{ selectedEmail?.message }}</pre>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" text @click="closeEmailDialog">Close</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import axios from "axios";
import { useToast } from "vue-toastification";

export default {
  data() {
    return {
      emails: [],
      sentEmails: [], // Add this line for sent emails
      loading: true,
      emailDialogVisible: false,
      confirmDeleteDialogVisible: false,
      selectedEmail: null,
      emailToDeleteId: null,
      storedEmail: null,
      isAuthenticated: false,
      drawer: false,
      showSentEmails: false, // Add this line to toggle between inbox and sent emails
    };
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  mounted() {
    this.getInboxEmails();
  },
  methods: {

    async fetchSentEmails() {
      this.showSentEmails = true; // Show sent emails section
      this.loading = true;

      const userEmail = this.$route.params.id; // Get user email from route
      const storedAuth = localStorage.getItem("token"); // Retrieve the auth token

      try {
        const response = await axios.get(`/api/emails/sent/${userEmail}`, {
          headers: {
            Authorization: `Bearer ${storedAuth}`,
          },
        });

        if (response.status === 200) {
          this.sentEmails = response.data; // Populate the sentEmails array
        } else {
          this.toast.error("Failed to fetch sent emails.");
        }
      } catch (error) {
        this.toast.error(`Error fetching sent emails: ${error.message}`);
      } finally {
        this.loading = false;
      }
    },
    showInbox() {
      this.showSentEmails = false; // Show the inbox section
      this.getInboxEmails(); // Fetch the inbox emails
    },

    async getInboxEmails() {
      const userEmail = this.$route.params.id;
      if (!userEmail) {
        this.toast.error("Email address is missing.");
        this.loading = false;
        return;
      }

      const storedAuth = localStorage.getItem("token");
      const storedEmail = localStorage.getItem("email");
      this.storedEmail = userEmail;

      try {
        const response = await axios.get(`/api/emails/inbox/${userEmail}`, {
          headers: {
            Authorization: `Bearer ${storedAuth}`,
          },
        });

        if (response.status === 200) {
          this.emails = response.data;
        } else {
          this.toast.error("Failed to fetch inbox emails.");
        }
      } catch (error) {
        this.toast.error(`Error fetching inbox emails: ${error.message}`);
      } finally {
        this.loading = false;
      }
    },
    async fetchSentEmails() {
      this.showSentEmails = true; // Show sent emails section
      this.loading = true;

      const userEmail = this.$route.params.id;
      const storedAuth = localStorage.getItem("token");

      try {
        const response = await axios.get(`/api/emails/sent/${userEmail}`, {
          headers: {
            Authorization: `Bearer ${storedAuth}`,
          },
        });

        if (response.status === 200) {
          this.sentEmails = response.data;
        } else {
          this.toast.error("Failed to fetch sent emails.");
        }
      } catch (error) {
        this.toast.error(`Error fetching sent emails: ${error.message}`);
      } finally {
        this.loading = false;
      }
    },
    showConfirmDeleteModal(emailId) {
      this.emailToDeleteId = emailId;
      this.confirmDeleteDialogVisible = true;
    },
    async confirmDeletion() {
      if (!this.emailToDeleteId) return;

      const storedAuth = localStorage.getItem("token");

      try {
        const response = await axios.delete(`/api/email/delete/${this.emailToDeleteId}`, {
          headers: {
            Authorization: `Bearer ${storedAuth}`,
          },
        });

        if (response.status === 200) {
          this.toast.success("Email deleted successfully!");
          this.emails = this.emails.filter(email => email.email_id !== this.emailToDeleteId);
          this.sentEmails = this.sentEmails.filter(email => email.email_id !== this.emailToDeleteId);
        } else {
          this.toast.error("Failed to delete email.");
        }
      } catch (error) {
        this.toast.error(`Error deleting email: ${error.message}`);
      } finally {
        this.emailToDeleteId = null;
        this.confirmDeleteDialogVisible = false;
      }
    },
    cancelDeletion() {
      this.emailToDeleteId = null;
      this.confirmDeleteDialogVisible = false;
    },
    viewEmail(email) {
      this.selectedEmail = email;
      this.emailDialogVisible = true;
    },
    closeEmailDialog() {
      this.emailDialogVisible = false;
      this.selectedEmail = null;
    },
  },
};
</script>

<style scoped>
.v-card {
  margin-bottom: 20px;
  border-radius: 12px;
  transition: box-shadow 0.3s ease;
}

.v-card:hover {
  box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.2);
}

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

.card-title {
  font-size: 18px;
  font-weight: bold;
}

.card-subtitle {
  color: #757575;
}

.hover-card {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.hover-card:hover {
  transform: scale(1.02);
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}

.empty-state-alert {
  background-color: #f5f5f5;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}

.modal-card {
  padding: 20px;
  border-radius: 8px;
}

.modal-card-subtitle {
  color: #757575;
  font-size: 14px;
}

.modal-card-text {
  white-space: pre-wrap;
  word-wrap: break-word;
}

.close-btn {
  transition: background-color 0.3s ease;
}

.close-btn:hover {
  background-color: rgba(255, 0, 0, 0.1);
}
.clickable-list-item {
    cursor: pointer;
  }
  
</style>