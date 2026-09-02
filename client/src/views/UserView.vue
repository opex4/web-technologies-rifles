<script setup lang="ts">
    import { storeToRefs } from "pinia";
    import { useUserInfoStore } from "@/stores/user_info_store.ts";
    import axios from 'axios';
    import { onBeforeMount, ref, watch } from "vue";
    import { useRouter } from "vue-router";
    import QRcode from 'qrcode';

    const router = useRouter();
    const userInfoStore = useUserInfoStore();
    const {
        userInfo,
        username,
        isStaff,
        isAuth,
        type,
        second,
    } = storeToRefs(userInfoStore);
    const key = ref<string>();
    const totpUrl = ref<string>("");
    const qrcodeUrl = ref();

    watch(totpUrl, async () => {
        qrcodeUrl.value = await QRcode.toDataURL(totpUrl.value)
    })

    onBeforeMount(async () => {
        await userInfoStore.fetchUserInfo();
    })

    async function onLogout() {
        const r = await axios.post("/api/users/logout/");
        await userInfoStore.fetchUserInfo();
        if (!isAuth.value){
            router.replace({ name: 'LoginView' });
        }
    }

    async function onActivate () {
        const r = await axios.post("/api/users/second-login/", {
            key: key.value,
        });
        userInfoStore.fetchUserInfo();
    }

    async function getTotpKey() {
        const r = await axios.get("/api/users/get-totp/");
        totpUrl.value = r.data.url;
    }

</script>

<template>
    <legend>Пользователь</legend>
    <div class="d-flex flex-row-reverse">
        <div class="d-flex flex-column gap-3 mt-4 mb-2">
            <span>Имя пользователя: {{ username }}</span>
            <span>Персонал: {{ isStaff ? 'Да' : 'Нет' }}</span>
            <span>Авторизация: {{ isAuth  ? 'Авторизован' : 'Не авторизован' }}</span>
            <span>Тип пользователя: {{ type }}</span>
            <span>Второй фактор: {{ second ? "Активирован" : "Не активирован" }}</span>
            <button type="button" class="btn btn-danger mt-2" @click="onLogout">Выйти</button>  
        </div>
        <div class="d-flex flex-column gap-3 m-4 mb-2" v-if="!second">
            <input type="text" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm" v-model="key">
            <button type="button" class="btn btn-primary" @click="onActivate">Активировать второй фактор</button>
        </div>
        <div class="d-flex flex-column gap-3 m-4 mb-2" v-if="!second">
            <img  :src="qrcodeUrl" alt="QRCode" v-if="qrcodeUrl">
            <button type="button" class="btn btn-primary" @click="getTotpKey">Запросить второй фактор</button>
        </div>
    </div>
</template>