<template>
    <v-container class="fill-height d-flex align-center justify-center" fluid>
        <v-row align="center" justify="center" class="text-center">
            <v-col cols="12" md="8" lg="6">
                <!-- Modern 404 Illustration -->
                <v-img
                    src="page-not-found.svg"
                    alt="404 Illustration"
                    class="mx-auto d-block"
                    max-width="800"
                ></v-img>

                <!-- Title -->
                <h1 class="text-h3 font-weight-bold mb-4">Oops! Page Not Found</h1>

                <!-- Subtitle -->
                <p class="text-body-1 mb-6">
                    The page you're looking for doesn't exist or has been moved. Let's get you back on track.
                </p>

                <!-- Action Button -->
                <v-btn
                    color="primary"
                    large
                    @click="goHome"
                    rounded
                >
                    Go Back Home
                </v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    name: 'NotFoundView',
    methods: {
        goHome() {
            this.$router.push({ name: 'Home' });
        },
    },
};
</script>

<style scoped>
.fill-height {
    height: 100vh;
}

.text-h3 {
    color: #2c3e50; /* Dark gray for better readability */
}

.text-body-1 {
    color: #7f8c8d; /* Light gray for subtitles */
}

.v-btn {
    text-transform: none; /* Keep button text in normal case */
}
</style>