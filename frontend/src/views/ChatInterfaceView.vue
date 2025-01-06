<template>
  <v-app>
    <v-main class="bg-grey-lighten-4">
      <v-container class="fill-height">
        <v-row justify="center" align="center">
          <v-col cols="12" sm="10" md="8" lg="6">
            <v-card class="elevation-12">
              <v-card-title class="text-h5 font-weight-bold text-center py-4">
                AI Chat Assistant
              </v-card-title>
              
              <v-card-text>
                <div class="chat-messages" ref="chatContainer">
                  <template v-if="messages.length">
                    <v-slide-y-transition group>
                      <div v-for="(message, index) in messages" :key="index" class="mb-4">
                        <v-chip
                          :color="message.isUser ? 'primary' : 'grey-lighten-3'"
                          :text-color="message.isUser ? 'white' : 'black'"
                          label
                        >
                          {{ message.isUser ? 'You' : 'AI' }}
                        </v-chip>
                        <div :class="['message-content', { 'text-right': message.isUser }]">
                          {{ message.content }}
                        </div>
                      </div>
                    </v-slide-y-transition>
                  </template>
                  <div v-else class="text-center text-subtitle-1 text-grey-darken-1 my-8">
                    Start a conversation by sending a message.
                  </div>
                </div>
              </v-card-text>

              <v-card-actions>
                <v-form @submit.prevent="sendMessage" class="d-flex align-center w-100">
                  <v-text-field
                    v-model="newMessage"
                    label="Type your message..."
                    append-inner-icon="mdi-send"
                    @click:append-inner="sendMessage"
                    variant="outlined"
                    hide-details
                    :loading="isLoading"
                    :disabled="isLoading"
                  ></v-text-field>
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

const sendMessage = async () => {
  if (!newMessage.value.trim() || isLoading.value) return

  const userMessage = newMessage.value.trim()
  messages.value.push({ content: userMessage, isUser: true })
  newMessage.value = ''
  isLoading.value = true

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
  }
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
  max-height: 400px;
  overflow-y: auto;
  padding: 16px;
}

.message-content {
  margin-top: 4px;
  padding: 8px 12px;
  border-radius: 8px;
  background-color: #f5f5f5;
  display: inline-block;
  max-width: 80%;
}

.text-right .message-content {
  background-color: #e3f2fd;
  float: right;
}
</style>