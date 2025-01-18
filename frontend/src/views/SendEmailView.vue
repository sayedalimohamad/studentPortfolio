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
    };
  },
  methods: {
    async sendEmail() {
      const toast = useToast();
      const storedAuth = localStorage.getItem('authToken');
      const userEmail = JSON.parse(localStorage.getItem('user')).email; // Retrieve user email

      const emailData = {
        sender_email: userEmail, // Use sender_email instead of sender_id
        recipient_email: this.recipient, // Use recipient_email instead of recipient
        subject: this.subject,
        message: this.message,
      };

      try {
        const response = await axios.post('/api/emails/send', emailData, {
          headers: {
            Authorization: `Bearer ${storedAuth}`,
          },
        });

        if (response.status === 201) { // Backend returns 201 for successful creation
          toast.success('Email sent successfully!');
          this.resetForm();
        } else {
          toast.error('An error occurred while sending the email.');
        }
      } catch (error) {
        console.error('Error sending email:', error);
        toast.error('An error occurred while sending the email.');
      }
    },
    resetForm() {
      this.recipient = '';
      this.subject = '';
      this.message = '';
      this.formValid = false;
    },
  },
};
</script>