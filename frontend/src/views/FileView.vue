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
                    <v-row>
                        <v-col cols="12" md="8">
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
                                <span>Uploaded At: <span class="word-color">{{ new
                                    Date(file.uploaded_at).toLocaleString()
                                        }}</span></span>
                            </v-card-subtitle>
                        </v-col>
                        <v-col cols="12" md="4" class="d-flex align-center justify-center">
                            <v-img :src="getFileImage(file.file_type)" max-width="300" max-height="300"></v-img>
                        </v-col>
                    </v-row>
                    <v-card-actions class="d-flex justify-end mt-2">
                        <v-btn color="success" @click="downloadFile(file)">
                            <v-icon left>mdi-download</v-icon>
                            Download
                        </v-btn>
                        <v-btn color="primary" @click="editFile(file)">
                            <v-icon left>mdi-pencil</v-icon>
                            Edit
                        </v-btn>

                        <v-btn color="red" @click="showDeleteConfirmation(file)">
                            <v-icon left>mdi-delete</v-icon>
                            Delete
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
        <v-alert v-else type="info" class="mt-6">You have no files uploaded yet.</v-alert>

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
                        Add
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- All Files Section -->
        <h2 class="text-2xl font-bold mb-6 word-color mt-8">All Files ({{ filteredAllFiles.length }})</h2>
        <v-text-field v-model="search" label="Search by file name or username or type" prepend-inner-icon="mdi-magnify"
            class="mb-4" outlined dense></v-text-field>

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
                    <v-row>
                        <v-col cols="12" md="8">
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
                                <span>Uploaded At: <span class="word-color">{{ new
                                    Date(file.uploaded_at).toLocaleString()
                                        }}</span></span>
                            </v-card-subtitle>
                            <v-card-subtitle class="text-gray-600 d-flex align-center mb-2">
                                <v-icon small class="mr-1">mdi-account</v-icon>
                                <span>Username: <span class="word-color">{{ file.username }}</span></span>
                            </v-card-subtitle>
                        </v-col>
                        <v-col cols="12" md="4" class="d-flex align-center justify-center">
                            <v-img :src="getFileImage(file.file_type)" max-width="300" max-height="300"></v-img>
                        </v-col>
                    </v-row>
                    <v-row class="mt-2">
                        <v-col class="d-flex justify-end">
                            <v-btn color="primary" @click="downloadFile(file)">
                                <v-icon left color="white">mdi-download</v-icon>
                                Download
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-card>
            </v-col>
        </v-row>
        <v-alert v-else type="info" class="mt-6">No files found.</v-alert>

        <!-- Edit File Modal -->
        <v-dialog v-model="showEditDialog" max-width="600">
            <v-card>
                <v-card-title class="headline pa-6">
                    <v-icon color="primary" left>mdi-pencil</v-icon>
                    Edit File
                </v-card-title>
                <v-card-text class="pa-6">
                    <v-form ref="editFileForm" v-model="editFileFormValid">
                        <v-text-field v-model="editedFile.file_name" label="File Name" outlined dense disabled
                            class="mb-4"></v-text-field>
                        <v-text-field v-model="editedFile.file_path" label="File Path" outlined dense disabled
                            class="mb-4"></v-text-field>
                        <v-select v-model="editedFile.file_type" :items="fileTypes" label="File Type" outlined dense
                            disabled class="mb-4"></v-select>
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

        <!-- Delete File Dialog -->
        <v-dialog v-model="showDeleteDialog" max-width="500">
            <v-card>
                <v-card-title class="headline pa-6">
                    <v-icon color="red" left>mdi-alert</v-icon>
                    Confirm Delete
                </v-card-title>
                <v-card-text class="pa-6">
                    Are you sure you want to delete the file <strong>{{ fileToDelete.file_name }}</strong>?
                </v-card-text>
                <v-card-actions class="pa-6">
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="showDeleteDialog = false">
                        <v-icon left>mdi-cancel</v-icon>
                        Cancel
                    </v-btn>
                    <v-btn color="red darken-1" text @click="confirmDeleteFile">
                        <v-icon left>mdi-delete</v-icon>
                        Delete
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
                file_type_id: null, // Default file type ID
                visibility: '',
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
            showDeleteDialog: false,
            fileToDelete: {},
        };
    },
    computed: {
        // Filter files for the "All Files" section based on search and file type
        filteredAllFiles() {
            return this.allFiles.filter(file => {
                const searchLower = this.search.toLowerCase();
                const fileNameMatch = file.file_name.toLowerCase().includes(searchLower);
                const fileTypeMatch = file.file_type.toLowerCase().includes(searchLower);
                const usernameMatch = file.username.toLowerCase().includes(searchLower);
                const typeMatch = this.selectedFileType ? file.file_type === this.selectedFileType : true;
                return (fileNameMatch || fileTypeMatch || usernameMatch) && typeMatch;
            });
        },
    },
    async created() {
        await this.fetchFiles();
    },
    methods: {
        downloadFile(file) {
            const link = document.createElement("a");
            link.href = file.file_url; // Make sure file_url is a valid direct link to the file
            link.setAttribute("download", file.file_name);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        },
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
                const token = localStorage.getItem('token');

                // Generate file path dynamically
                this.newFile.file_path = `/path/to/${this.newFile.file_type}s/${this.newFile.file_name}`;

                const response = await axios.post('/api/files/', this.newFile, {
                    headers: { Authorization: `Bearer ${token}` },
                });

                this.myFiles.push(response.data);
                this.newFile = { file_name: '', file_path: '', file_type: '', file_type_id: 1, visibility: 'public' };
                this.showAddModal = false;
                useToast().success('File uploaded successfully.');
                await this.fetchFiles();
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
        showDeleteConfirmation(file) {
            this.fileToDelete = file;
            this.showDeleteDialog = true;
        },
        async confirmDeleteFile() {
            try {
                await axios.delete(`/api/files/${this.fileToDelete.file_id}`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`,
                    },
                });
                this.myFiles = this.myFiles.filter(f => f.file_id !== this.fileToDelete.file_id);
                useToast().success('File deleted successfully.');
                await this.fetchFiles(); // Refresh the file list
            } catch (error) {
                console.error('Error deleting file:', error);
                useToast().error('Failed to delete file. Please try again.');
            } finally {
                this.showDeleteDialog = false;
            }
        },
        filterByFileType(type) {
            this.selectedFileType = type;
        },
        getFileImage(fileType) {
            const images = {
                document: [
                    '/files/documents/document-01.svg',
                    '/files/documents/document-02.svg',
                    '/files/documents/document-03.svg',
                ],
                image: [
                    '/files/images/image-01.svg',
                    '/files/images/image-02.svg',
                    '/files/images/image-03.svg',
                    '/files/images/image-04.svg',
                    '/files/images/image-05.svg',
                    '/files/images/image-06.svg',
                ],
                video: [
                    '/files/videos/video-01.svg',
                    '/files/videos/video-02.svg',
                    '/files/videos/video-03.svg',
                    '/files/videos/video-04.svg',
                ],
                default: ['/files/unknown-file-type.svg']
            };

            const fileList = images[fileType] || images.default;
            return fileList[Math.floor(Math.random() * fileList.length)];
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
