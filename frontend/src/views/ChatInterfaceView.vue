<template>
  <v-app>
    <v-container class="fill-height">
      <v-row justify="center" align="center">
        <v-col cols="12" sm="10" md="8" lg="6">
          <v-card class="elevation-12 rounded-lg">
            <v-card-title class="text-h5 font-weight-bold text-center py-4 ai-chat-title d-flex align-center justify-center">
              <v-icon size="36px" class="mr-2">mdi-robot</v-icon>
              <span>AI Chat Assistant</span>
            </v-card-title>

            <v-card-text>
              <div class="chat-messages" ref="chatContainer">
                <template v-if="messages.length">
                  <v-slide-y-transition group>
                    <div v-for="(message, index) in messages" :key="index" class="mb-4">
                      <v-chip :color="message.isUser ? 'primary' : 'secondary'" :text-color="message.isUser ? 'white' : 'black'" label>
                        {{ message.isUser ? 'You' : 'AI' }}
                      </v-chip>
                      <div
                        :class="['message-content', { 'user-message': message.isUser, 'ai-message': !message.isUser }]"
                        :style="!message.isUser ? { backgroundColor: determineBackgroundColor(message.content) } : {}"
                      >
                        <div v-html="formatMessage(message.content)"></div>
                      </div>
                    </div>
                  </v-slide-y-transition>
                </template>
                <div v-else class="text-center text-subtitle-1 text-grey-darken-1 my-8">
                  Start a conversation by sending a message.
                </div>
              </div>
            </v-card-text>

            <v-card-actions class="pa-4">
              <v-form @submit.prevent="sendMessage" class="d-flex align-center w-100">
                <v-text-field
                  ref="messageInput"
                  v-model="newMessage"
                  label="Type your message..."
                  append-inner-icon="mdi-send"
                  @click:append-inner="sendMessage"
                  variant="outlined"
                  hide-details
                  :loading="isLoading"
                  :disabled="isLoading"
                ></v-text-field>
                <v-btn @click="clearChat" icon class="ml-2">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-form>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import axios from 'axios'; // Import your custom Axios instance

const messages = ref([]);
const newMessage = ref('');
const isLoading = ref(false);
const chatContainer = ref(null);
const messageInput = ref(null);

const greetings = ['hello', 'hi', 'hey'];

const sendMessage = async () => {
  if (!newMessage.value.trim() || isLoading.value) return;

  const userMessage = newMessage.value.trim();
  messages.value.push({ content: userMessage, isUser: true });
  newMessage.value = '';
  isLoading.value = true;

  if (greetings.includes(userMessage.toLowerCase())) {
    messages.value.push({ content: 'Welcome! How can I assist you today?', isUser: false });
    isLoading.value = false;
    await nextTick();
    scrollToBottom();
    messageInput.value.focus();
    return;
  }

  try {
    const response = await axios.post('/api/ask', { question: userMessage });
    messages.value.push({ content: response.data.response, isUser: false });
  } catch (error) {
    console.error('Error:', error);
    messages.value.push({
      content: 'Sorry, there was an error processing your request.',
      isUser: false,
    });
  } finally {
    isLoading.value = false;
    await nextTick();
    scrollToBottom();
    messageInput.value.focus();
  }
};

const clearChat = () => {
  messages.value = [];
};

const formatMessage = (message) => {
  // Replace newlines with <br> tags for HTML rendering
  message = message.replace(/\n/g, '<br>');

  // Bold specific parts of the response
  message = message.replace(/(Sure! Here's what I found:|Here's the full information:)/g, '<strong>$1</strong>');

  return message;
};

const determineBackgroundColor = (messageContent) => {
  if (messageContent.toLowerCase().includes('error')) {
    return '#e74c3c80'; 
  } else if (messageContent.toLowerCase().includes('welcome')) {
    return '#fbc53180'; 
  }
  return '#0097a780'; 
};

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

onMounted(() => {
  scrollToBottom();
});
</script>

<style scoped>
.chat-messages {
  margin-top: 16px;
  height: 400px; /* Set a specific height for the chat box */
  overflow-y: auto;
  padding: 16px;
  background-color: var(--v-theme-background); /* Theme background */
  border-radius: var(--v-border-radius-lg);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-messages::-webkit-scrollbar {
  width: 8px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background-color: var(--v-theme-primary); /* Primary color */
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-track {
  background-color: var(--v-theme-surface); /* Surface color */
  border-radius: 4px;
}

.message-content {
  margin-top: 4px;
  padding: 12px 16px;
  border-radius: 16px;
  display: inline-block;
  max-width: 80%;
  word-wrap: break-word;
  box-shadow: var(--v-theme-shadow-2); /* Use theme shadow */
}

.user-message {
  background-color: var(--v-theme-primary);
  color: var(--v-theme-on-primary); /* Text on primary */
  /* float: right; */
}

.ai-message {
  margin-left: 8px;
  color: var(--v-theme-on-secondary); /* Text on secondary */
}

.v-card-title {
  background-color: var(--v-theme-primary);
  color: var(--v-theme-on-primary);
}

.v-card-actions {
  background-color: var(--v-theme-surface);
}

.ai-chat-title {
  background-color: var(--v-theme-secondary);
  color: var(--v-theme-on-secondary);
}
</style>
