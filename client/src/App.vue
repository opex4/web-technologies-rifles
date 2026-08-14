<script setup lang="ts">

</script>

<template>
    <div class="container">
        <nav class="nav nav-pills flex-column flex-sm-row mt-4">
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/"
            >Rifles</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/countries"
            >Countries</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/constructors"
            >Constructors</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/ammo"
            >Ammo</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/conflicts"
            >Conflicts</router-link>
        </nav>
    </div>
    <div class="container">
        <router-view/>
    </div>
</template>

