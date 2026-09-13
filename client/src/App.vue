<script setup lang="ts">
    import { storeToRefs } from "pinia";
    import { useUserInfoStore } from "@/stores/user_info_store.ts";
    import { onBeforeMount } from "vue";

    const userInfoStore = useUserInfoStore();
    const {
        isAuth,
        moderatorPerm,
        builderPerm,
    } = storeToRefs(userInfoStore);

    onBeforeMount(async () => {
        await userInfoStore.fetchUserInfo();
    })
</script>

<template>
    <div class="container" v-if="isAuth">
        <nav class="nav nav-pills flex-column flex-sm-row mt-4">
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/"
            >Оружие</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/countries"
            >Страны</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/constructors"
            >Конструкторы</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/ammo"
            >Аммуниция</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/conflicts"
            >Конфликты</router-link>
            <router-link 
                v-if="builderPerm"
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/types_of_mounts"
            >Типы креплений</router-link>
            <router-link 
                v-if="builderPerm"
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/attachments"
            >Обвесы</router-link>
            <router-link 
                v-if="builderPerm"
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/loadouts"
            >Сборки</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/user"
            >Пользователь</router-link>
            <a class="flex-sm-fill text-sm-center nav-link" href="/admin" v-if="moderatorPerm">Админка</a>
        </nav>
    </div>
    <div class="container">
        <router-view/>
    </div>
</template>

