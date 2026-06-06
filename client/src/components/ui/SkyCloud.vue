<template>
    <div class="absolute inset-0 sky-gradient"></div>
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
        <div class="cloud cloud-1 absolute w-24 h-12 bg-white rounded-full"></div>
        <div class="cloud cloud-2 absolute w-32 h-16 bg-white rounded-full"></div>
        <div class="cloud cloud-3 absolute w-20 h-10 bg-white rounded-full"></div>
        <div class="cloud cloud-4 absolute w-28 h-14 bg-white rounded-full"></div>
        <div class="cloud cloud-5 absolute w-36 h-18 bg-white rounded-full"></div>
    </div>
</template>

<script setup lang="ts">

</script>

<style scoped>
.sky-gradient {
    background: linear-gradient(to bottom,
            #87CEEB 0%,
            /* 天空蓝 */
            #E0F6FF 50%,
            /* 浅蓝 */
            #87CEEB 100%
            /* 白色 */
        );
}

.cloud {
    filter: blur(2px);
    box-shadow:
        0 0 30px rgba(255, 255, 255, 0.6),
        inset 0 -8px 15px rgba(200, 220, 240, 0.4);
}

.cloud::before,
.cloud::after {
    content: '';
    position: absolute;
    background: white;
    border-radius: 50%;
}

.cloud::before {
    width: 50%;
    height: 70%;
    top: 25%;
    left: -15%;
}

.cloud::after {
    width: 45%;
    height: 60%;
    top: 35%;
    right: -10%;
}

@keyframes cloud-drift-1 {
    0% {
        left: -150px;
        top: 5%;
    }

    100% {
        left: calc(100% + 150px);
        top: 8%;
    }
}

@keyframes cloud-drift-2 {
    0% {
        left: -200px;
        top: 15%;
    }

    100% {
        left: calc(100% + 200px);
        top: 12%;
    }
}

@keyframes cloud-drift-3 {
    0% {
        left: -120px;
        top: 25%;
    }

    100% {
        left: calc(100% + 120px);
        top: 22%;
    }
}

@keyframes cloud-drift-4 {
    0% {
        left: -180px;
        top: 35%;
    }

    100% {
        left: calc(100% + 180px);
        top: 38%;
    }
}

@keyframes cloud-drift-5 {
    0% {
        left: -220px;
        top: 45%;
    }

    100% {
        left: calc(100% + 220px);
        top: 42%;
    }
}

.cloud-1 {
    opacity: 0.7;
    animation: cloud-drift-1 35s linear infinite;
    animation-delay: 0s;
}

.cloud-2 {
    opacity: 0.6;
    animation: cloud-drift-2 45s linear infinite;
    animation-delay: -15s;
}

.cloud-3 {
    opacity: 0.75;
    animation: cloud-drift-3 25s linear infinite;
    animation-delay: -8s;
}

.cloud-4 {
    opacity: 0.65;
    animation: cloud-drift-4 40s linear infinite;
    animation-delay: -20s;
}

.cloud-5 {
    opacity: 0.55;
    animation: cloud-drift-5 50s linear infinite;
    animation-delay: -30s;
}
</style>