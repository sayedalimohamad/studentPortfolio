<template>
    <v-container class="py-12">
        <v-row class="mb-8">
            <v-col cols="12" class="text-center">
                <h1 class="text-3xl font-bold word-color">Files</h1>
                <p class="text-lg text-gray-700 mt-2">Manage and view files here.</p>
            </v-col>
        </v-row>

        <!-- Add New File Button -->
        <v-row class="mb-8">
            <v-col cols="12" class="text-right">
                <v-btn color="primary" dark @click="showAddModal = true">
                    <v-icon left color="white">mdi-plus</v-icon>
                    Add New File
                </v-btn>
            </v-col>
        </v-row>

        <!-- My Files Section -->
        <h2 class="text-2xl font-bold mb-6 word-color">My Files ({{ myFiles.length }})</h2>
        <v-row v-if="myFiles.length > 0" dense>
            <v-col v-for="file in myFiles" :key="file.file_id" cols="12" md="6" lg="4">
                <v-card class="mb-4 pa-4">
                    <v-card-title class="d-flex align-center">
                        <v-avatar class="mr-3">
                            <v-icon color="primary">mdi-file</v-icon>
                        </v-avatar>
                        <span class="text-lg font-bold word-color">{{ file.file_name }}</span>
                    </v-card-title>
                    <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
                        <v-icon small class="mr-1">mdi-folder</v-icon>
                        <span>File Path: <span class="word-color">{{ file.file_path }}</span></span>
                    </v-card-subtitle>
                    <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
                        <v-icon small class="mr-1">mdi-file-find</v-icon>
                        <span>File Type: <span class="word-color">{{ file.file_type }}</span></span>
                    </v-card-subtitle>
                    <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
                        <v-icon small class="mr-1">mdi-eye</v-icon>
                        <span>Visibility: <span>
                                <v-chip class="ma-1 ml-2"
                                    :color="file.visibility === 'public' ? 'primary' : (file.visibility === 'supervisors' ? 'success' : 'error')"
                                    text-color="white" small>
                                    <strong class="mx-2">{{ file.visibility.toUpperCase() }}</strong>
                                </v-chip>
                            </span></span>
                    </v-card-subtitle>
                    <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
                        <v-icon small class="mr-1">mdi-calendar</v-icon>
                        <span>Uploaded At: <span class="word-color">{{ new Date(file.uploaded_at).toLocaleString()
                                }}</span></span>
                    </v-card-subtitle>
                    <v-card-actions>
                        <v-btn color="primary" @click="editFile(file)">
                            <v-icon left>mdi-pencil</v-icon>
                            Edit
                        </v-btn>
                        <v-btn color="red" @click="deleteFile(file.file_id)">
                            <v-icon left>mdi-delete</v-icon>
                            Delete
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
        <v-alert v-else type="info" class="mt-6">You have no files uploaded yet.</v-alert>

        <!-- All Files Section -->
        <h2 class="text-2xl font-bold mb-6 word-color mt-8">All Files ({{ filteredAllFiles.length }})</h2>
        <v-text-field v-model="search" label="Search by file name or type" prepend-inner-icon="mdi-magnify" class="mb-4"
            outlined dense></v-text-field>

        <!-- File Type Navigation -->
        <v-row class="mb-6">
            <v-col cols="12">
                <v-chip-group v-model="selectedFileType" mandatory active-class="primary--text">
                    <v-chip @click="filterByFileType('')">All</v-chip>
                    <v-chip v-for="type in fileTypes" :key="type" @click="filterByFileType(type)">
                        {{ type.charAt(0).toUpperCase() + type.slice(1) }}
                    </v-chip>
                </v-chip-group>
            </v-col>
        </v-row>

        <v-row v-if="filteredAllFiles.length > 0" dense>
            <v-col v-for="file in filteredAllFiles" :key="file.file_id" cols="12" md="6" lg="4">
                <v-card class="mb-4 pa-4">
                    <v-card-title class="d-flex align-center">
                        <v-avatar class="mr-3">
                            <v-icon color="primary">mdi-file</v-icon>
                        </v-avatar>
                        <span class="text-lg font-bold word-color">{{ file.file_name }}</span>
                    </v-card-title>
                    <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
                        <v-icon small class="mr-1">mdi-folder</v-icon>
                        <span>File Path: <span class="word-color">{{ file.file_path }}</span></span>
                    </v-card-subtitle>
                    <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
                        <v-icon small class="mr-1">mdi-file-find</v-icon>
                        <span>File Type: <span class="word-color">{{ file.file_type }}</span></span>
                    </v-card-subtitle>
                    <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
                        <v-icon small class="mr-1">mdi-eye</v-icon>
                        <span>Visibility: <span>
                                <v-chip class="ma-1 ml-2"
                                    :color="file.visibility === 'public' ? 'primary' : (file.visibility === 'supervisors' ? 'success' : 'error')"
                                    text-color="white" small>
                                    <strong class="mx-2">{{ file.visibility.toUpperCase() }}</strong>
                                </v-chip>
                            </span></span>
                    </v-card-subtitle>
                    <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
                        <v-icon small class="mr-1">mdi-calendar</v-icon>
                        <span>Uploaded At: <span class="word-color">{{ new Date(file.uploaded_at).toLocaleString()
                                }}</span></span>
                    </v-card-subtitle>
                </v-card>
            </v-col>
        </v-row>
        <v-alert v-else type="info" class="mt-6">No files found.</v-alert>

        <!-- Add New File Modal -->
        <v-dialog v-model="showAddModal" max-width="600">
            <v-card>
                <v-card-title class="headline pa-6">
                    <v-icon color="primary" left>mdi-plus</v-icon>
                    Add New File
                </v-card-title>
                <v-card-text class="pa-6">
                    <v-form ref="addFileForm" v-model="addFileFormValid">
                        <v-text-field v-model="newFile.file_name" label="File Name"
                            :rules="[v => !!v || 'File Name is required']" required outlined dense
                            class="mb-4"></v-text-field>
                        <v-text-field v-model="newFile.file_path" label="File Path"
                            :rules="[v => !!v || 'File Path is required']" required outlined dense
                            class="mb-4"></v-text-field>
                        <v-select v-model="newFile.file_type" :items="fileTypes" label="File Type"
                            :rules="[v => !!v || 'File Type is required']" required outlined dense
                            class="mb-4"></v-select>
                        <v-select v-model="newFile.visibility" :items="visibilityOptions" label="Visibility"
                            :rules="[v => !!v || 'Visibility is required']" required outlined dense
                            class="mb-4"></v-select>
                    </v-form>
                </v-card-text>
                <v-card-actions class="pa-6">
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="showAddModal = false">
                        <v-icon left>mdi-cancel</v-icon>
                        Cancel
                    </v-btn>
                    <v-btn color="green darken-1" text @click="uploadFile" :disabled="!addFileFormValid">
                        <v-icon left>mdi-check</v-icon>
                        Save
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- Edit File Modal -->
        <v-dialog v-model="showEditDialog" max-width="600">
            <v-card>
                <v-card-title class="headline pa-6">
                    <v-icon color="primary" left>mdi-pencil</v-icon>
                    Edit File
                </v-card-title>
                <v-card-text class="pa-6">
                    <v-form ref="editFileForm" v-model="editFileFormValid">
                        <v-text-field v-model="editedFile.file_name" label="File Name"
                            :rules="[v => !!v || 'File Name is required']" required outlined dense
                            class="mb-4"></v-text-field>
                        <v-text-field v-model="editedFile.file_path" label="File Path"
                            :rules="[v => !!v || 'File Path is required']" required outlined dense
                            class="mb-4"></v-text-field>
                        <v-select v-model="editedFile.file_type" :items="fileTypes" label="File Type"
                            :rules="[v => !!v || 'File Type is required']" required outlined dense
                            class="mb-4"></v-select>
                        <v-select v-model="editedFile.visibility" :items="visibilityOptions" label="Visibility"
                            :rules="[v => !!v || 'Visibility is required']" required outlined dense
                            class="mb-4"></v-select>
                    </v-form>
                </v-card-text>
                <v-card-actions class="pa-6">
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="showEditDialog = false">
                        <v-icon left>mdi-cancel</v-icon>
                        Cancel
                    </v-btn>
                    <v-btn color="green darken-1" text @click="updateFile" :disabled="!editFileFormValid">
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
    name: 'FileView',
    data() {
        return {
            myFiles: [], // Files uploaded by the current user
            allFiles: [], // All files (filtered by privacy)
            search: '',
            selectedFileType: '', // Selected file type for filtering
            newFile: {
                file_name: '',
                file_path: '',
                file_type: '',
                file_type_id: 1, // Default file type ID
                visibility: 'public',
            },
            editedFile: {
                file_id: null,
                file_name: '',
                file_path: '',
                file_type: '',
                file_type_id: 1,
                visibility: '',
            },
            showAddModal: false,
            showEditDialog: false,
            addFileFormValid: false,
            editFileFormValid: false,
            fileTypes: ['document', 'image', 'video'],
            visibilityOptions: ['public', 'supervisors', 'private'],
        };
    },
    computed: {
        // Filter files for the "All Files" section based on search and file type
        filteredAllFiles() {
            return this.allFiles.filter(file => {
                const fileNameMatch = file.file_name.toLowerCase().includes(this.search.toLowerCase());
                const fileTypeMatch = file.file_type.toLowerCase().includes(this.search.toLowerCase());
                const typeMatch = this.selectedFileType ? file.file_type === this.selectedFileType : true;
                return (fileNameMatch || fileTypeMatch) && typeMatch;
            });
        },
    },
    async created() {
        await this.fetchFiles();
    },
    methods: {
        async fetchFiles() {
            try {
                // Fetch files uploaded by the current user
                const myFilesResponse = await axios.get('/api/files/my-files', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`,
                    },
                });
                this.myFiles = myFilesResponse.data;

                // Fetch all files (filtered by privacy)
                const allFilesResponse = await axios.get('/api/files/all', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`,
                    },
                });
                this.allFiles = allFilesResponse.data;
            } catch (error) {
                console.error('Error fetching files:', error);
                useToast().error('Failed to fetch files. Please try again.');
            }
        },
        async uploadFile() {
            try {
                const response = await axios.post('/api/files', this.newFile, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`,
                    },
                });
                this.myFiles.push(response.data);
                this.newFile = { file_name: '', file_path: '', file_type: '', file_type_id: 1, visibility: 'public' };
                this.showAddModal = false;
                useToast().success('File uploaded successfully.');
                await this.fetchFiles(); // Refresh the file list
            } catch (error) {
                console.error('Error uploading file:', error);
                useToast().error('Failed to upload file. Please try again.');
            }
        },
        editFile(file) {
            this.editedFile = { ...file };
            this.showEditDialog = true;
        },
        async updateFile() {
            try {
                await axios.put(`/api/files/${this.editedFile.file_id}`, this.editedFile, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`,
                    },
                });
                const index = this.myFiles.findIndex(f => f.file_id === this.editedFile.file_id);
                this.myFiles[index] = this.editedFile;
                this.showEditDialog = false;
                useToast().success('File updated successfully.');
                await this.fetchFiles(); // Refresh the file list
            } catch (error) {
                console.error('Error updating file:', error);
                useToast().error('Failed to update file. Please try again.');
            }
        },
        async deleteFile(fileId) {
            try {
                await axios.delete(`/api/files/${fileId}`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`,
                    },
                });
                this.myFiles = this.myFiles.filter(f => f.file_id !== fileId);
                useToast().success('File deleted successfully.');
                await this.fetchFiles(); // Refresh the file list
            } catch (error) {
                console.error('Error deleting file:', error);
                useToast().error('Failed to delete file. Please try again.');
            }
        },
        filterByFileType(type) {
            this.selectedFileType = type;
        },
    },
};
</script>

<style scoped>
.word-color {
    color: #0097A7;
}

.v-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    padding: 16px;
    margin-bottom: 16px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.v-card-title {
    padding-bottom: 24px;
}

.v-card-subtitle {
    padding-bottom: 8px;
}

.v-card-text p {
    margin: 0;
    line-height: 1.5;
}

.v-avatar {
    background-color: #e0f7fa;
}

.v-icon {
    color: #0097A7;
}

</style>