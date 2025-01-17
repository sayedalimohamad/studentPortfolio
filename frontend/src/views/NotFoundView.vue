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
                    style="filter: grayscale(.2) invert(.2);"
                ></v-img>

                <!-- Title -->
                <h1 class=" font-weight-bold mb-4" style="color: #00ACC1;">Oops! Page Not Found</h1>

                <!-- Subtitle -->
                <p class=" mb-6 ">
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
</style>