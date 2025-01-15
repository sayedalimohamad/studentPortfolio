<template>
  <v-app>
    <v-main class="bg-grey-lighten-4">
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
                        <div :class="['message-content', { 'user-message': message.isUser, 'ai-message': !message.isUser }]">
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
                  <v-text-field ref="messageInput" v-model="newMessage" label="Type your message..." append-inner-icon="mdi-send" @click:append-inner="sendMessage" variant="outlined" hide-details :loading="isLoading" :disabled="isLoading"></v-text-field>
                  <v-btn @click="clearChat" icon class="ml-2">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </v-form>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios' // Import your custom Axios instance

const messages = ref([])
const newMessage = ref('')
const isLoading = ref(false)
const chatContainer = ref(null)
const messageInput = ref(null)

const greetings = ['hello', 'hi', 'hey']

const sendMessage = async () => {
  if (!newMessage.value.trim() || isLoading.value) return

  const userMessage = newMessage.value.trim()
  messages.value.push({ content: userMessage, isUser: true })
  newMessage.value = ''
  isLoading.value = true

  if (greetings.includes(userMessage.toLowerCase())) {
    messages.value.push({ content: 'Welcome! How can I assist you today?', isUser: false })
    isLoading.value = false
    await nextTick()
    scrollToBottom()
    messageInput.value.focus()
    return
  }

  try {
    const response = await axios.post('/api/ask', { question: userMessage })
    messages.value.push({ content: response.data.response, isUser: false })
  } catch (error) {
    console.error('Error:', error)
    messages.value.push({
      content: 'Sorry, there was an error processing your request.',
      isUser: false
    })
  } finally {
    isLoading.value = false
    await nextTick()
    scrollToBottom()
    messageInput.value.focus()
  }
}

const clearChat = () => {
  messages.value = []
}

const formatMessage = (message) => {
  // Replace newlines with <br> tags for HTML rendering
  message = message.replace(/\n/g, '<br>')

  // Bold specific parts of the response
  message = message.replace(/(Sure! Here's what I found:|Here's the full information:)/g, '<strong>$1</strong>')

  return message
}

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.chat-messages {
  margin-top: 16px;
  max-height: 400px;
  overflow-y: auto;
  padding: 16px;
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-messages::-webkit-scrollbar {
  width: 8px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background-color: #00ACC1;
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-track {
  background-color: #e0e0e0;
  border-radius: 4px;
}

.message-content {
  margin-top: 4px;
  padding: 12px 16px;
  border-radius: 16px;
  display: inline-block;
  max-width: 80%;
  word-wrap: break-word;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-message {
  background-color: #00ACC1;
  color: white;
  float: right;
}

.ai-message {
  background-color: #e0f7fa;
  margin-left: 8px;
}

.v-card-title {
  background-color: #00ACC1;
  color: white;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.v-card-actions {
  background-color: #ffffff;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}

.v-text-field {
  background-color: #ffffff;
  border-radius: 8px;
}

.ai-chat-title {
  background-color: #e0f7fa !important;
  color: #101010;
}

.v-btn:hover {
  transform: scale(1.1);
  transition: transform 0.2s;
}

.v-chip:hover {
  transform: scale(1.05);
  transition: transform 0.2s;
}
.v-icon, .ai-chat-title {
  color:  #00ACC1;
}
</style>