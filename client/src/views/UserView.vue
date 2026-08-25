<script setup lang="ts">
    import { storeToRefs } from "pinia";
    import { useUserInfoStore } from "@/stores/user_info_store.ts";
    import axios from 'axios';
    import { onBeforeMount, ref } from "vue";
    import Cookies from 'js-cookie';    
    import { useRouter } from "vue-router";

    const router = useRouter();
    const userInfoStore = useUserInfoStore();
    const {
        username,
        isStaff,
        isAuth,
    } = storeToRefs(userInfoStore);

    onBeforeMount(async () => {
        userInfoStore.fetchUserInfo();
    })

    async function onLogout() {
        const r = await axios.post("/api/users/logout/");
        await userInfoStore.fetchUserInfo();
        if (!isAuth.value){
            router.replace({ name: 'LoginView' });
        }
    }

</script>

<template>
    <legend>Пользователь</legend>
    <div>
        <p>Имя пользователя: {{ username }}</p>
        <p>Персонал: {{ isStaff ? 'Да' : 'Нет' }}</p>
        <p>Авторизация: {{ isAuth  ? 'Авторизован' : 'Не авторизован' }}</p>
        <button type="button" class="btn btn-danger" @click="onLogout">Выйти</button>
    </div>
</template>