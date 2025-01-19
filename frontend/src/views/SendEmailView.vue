<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>
            <span class="headline">Send Email</span>
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="sendEmail" v-model="formValid">
              <v-text-field
                v-model="recipient"
                label="To"
                type="email"
                required
                :rules="[emailRule]"
                :error-messages="recipientErrorMessage"
              ></v-text-field>
              <v-text-field
                v-model="subject"
                label="Subject"
                required
              ></v-text-field>
              <v-textarea
                v-model="message"
                label="Message"
                required
                rows="6"
              ></v-textarea>
              <v-btn :disabled="!formValid" type="submit" color="primary" block>
                Send
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      recipient: '',
      subject: '',
      message: '',
      formValid: false,
      emailRule: [
        v => !!v || 'Email is required',
        v => /.+@.+\..+/.test(v) || 'Enter a valid email',
      ],
      recipientErrorMessage: '', // Added to handle error messages for recipient
    };
  },
  methods: {
    async sendEmail() {
      const toast = useToast();
      const storedAuth = localStorage.getItem('token');
      const userEmail = localStorage.getItem('email');

      // Check if recipient email and other required fields are valid
      if (!this.recipient || !this.subject || !this.message) {
        this.recipientErrorMessage = 'Please fill out all required fields.';
        return;
      }

      const emailData = {
        sender_email: userEmail, // Use sender_email (from the logged-in user)
        recipient_email: this.recipient, // Use recipient_email (input from the user)
        subject: this.subject,
        message: this.message,
      };

      try {
        // Make the request to the backend API
        const response = await axios.post('/api/emails/send', emailData, {
          headers: {
            Authorization: `Bearer ${storedAuth}`, // Add the Bearer token for authentication
          },
        });

        if (response.status === 201) {
          toast.success('Email sent successfully!');
          this.resetForm();
          this.$router.push(`/inbox/${userEmail}`);
        } else {
          toast.error('An error occurred while sending the email.');
        }
      } catch (error) {
        console.error('Error sending email:', error);
        toast.error('An error occurred while sending the email.');
      }
    },
    resetForm() {
      // Reset the form fields
      this.recipient = '';
      this.subject = '';
      this.message = '';
      this.formValid = false;
    },
  },
};
</script>

