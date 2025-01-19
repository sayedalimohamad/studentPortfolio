<template>
  <v-container>
    <v-row justify="center mt-6">
      <v-col cols="12" md="8">
        
        <v-card class="mx-2 my-2">
          <span>
              <v-btn icon @click="$router.go(-1)" class="float-right  mx-2 my-2 " color="red" style="transform: scale(.6);">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </span>
          <v-card-title class="text-left headline font-weight-bold text-uppercase mt-6 mb-2">
            <span class="headline">Send Email</span>
            
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="sendEmail" v-model="formValid">
              <v-text-field v-model="recipient" label="To" type="email" required :rules="[emailRule]"
                :error-messages="recipientErrorMessage"></v-text-field>
              <v-text-field v-model="subject" label="Subject" required></v-text-field>
              <v-textarea v-model="message" label="Message" required rows="6"></v-textarea>
              <div block class="float-right mb-4 mt-2">
                <v-btn @click="$router.go(-1)" color="light" tonal class="mr-4">
                  <v-icon>mdi-keyboard-backspace</v-icon>
                  Back
                </v-btn>
                <v-btn :disabled="!formValid" type="submit" color="primary" >
                  <v-icon>mdi-email-fast</v-icon>
                  Send
                </v-btn>
              </div>
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
