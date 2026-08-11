<script setup lang="ts">

</script>

<template>
    <div class="container">
        <nav class="nav nav-pills flex-column flex-sm-row mt-4">
            <router-link class="flex-sm-fill text-sm-center nav-link" to="/">Rifles</router-link>
            <router-link class="flex-sm-fill text-sm-center nav-link" to="/countries">Countries</router-link>
            <router-link class="flex-sm-fill text-sm-center nav-link" to="/constructors">Constructors</router-link>
            <router-link class="flex-sm-fill text-sm-center nav-link" to="/ammo">Ammo</router-link>
            <router-link class="flex-sm-fill text-sm-center nav-link" to="/conflicts">Conflicts</router-link>
        </nav>
    </div>
    <div class="container">
        <router-view/>
    </div>
</template>

