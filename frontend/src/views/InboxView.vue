<template>
  <v-container>
    <v-row>
      <!-- Empty state with an icon -->
      <v-col v-if="emails.length === 0 && !loading" class="text-center">
        <v-alert type="info" border="left" prominent class="empty-state-alert">
          <v-icon large color="primary">mdi-inbox</v-icon>
          <div>No emails available.</div>
        </v-alert>
      </v-col>

      <!-- Email cards -->
      <v-col v-for="email in emails" :key="email.email_id" cols="12" sm="6" md="4">
        <v-card elevation="4" class="hover-card">
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
            <v-btn @click="viewEmail(email)" color="primary" rounded>View Email</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Loading spinner with overlay -->
    <div v-if="loading" class="loading-overlay">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </div>

    <!-- Modal for viewing email -->
    <v-dialog v-model="emailDialogVisible" max-width="600px">
      <v-card class="modal-card">
        <v-card-title>
          <v-btn icon @click="closeEmailDialog" class="float-right close-btn" color="red">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-icon left>mdi-email</v-icon>
          <span>{{ selectedEmail?.subject }}</span>
          <v-spacer></v-spacer>
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
</template>


<script>
import axios from "axios";
import { useToast } from "vue-toastification";

export default {
  data() {
    return {
      emails: [],
      loading: true,
      emailDialogVisible: false,
      selectedEmail: null,
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
    async getInboxEmails() {
      const userEmail = this.$route.params.id;
      if (!userEmail) {
        this.toast.error("Email address is missing.");
        this.loading = false;
        return;
      }

      const storedAuth = localStorage.getItem("token");

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

.v-alert {
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px;
  border-radius: 8px;
}

.empty-state-alert {
  background-color: #f5f5f5;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
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

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
