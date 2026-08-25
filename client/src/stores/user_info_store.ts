import { defineStore } from 'pinia';
import type {User} from "@/types/User.ts";
import { ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

export const useUserInfoStore = defineStore('userInfoStore', () => {
    const userInfo = ref<User>();
    const username = ref<string>("");
    const isAuth = ref<boolean>(false);
    const isStaff = ref<boolean>(false);

    async function fetchUserInfo() {
        userInfo.value = await axios.get('/api/users/my/')
            .then(res => res.data as User);

        username.value = userInfo.value?.username;
        isAuth.value = userInfo.value?.isAuth;
        isStaff.value = userInfo.value?.isStaff;

        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    }

    return {
        userInfo,
        username,
        isAuth,
        isStaff,
        fetchUserInfo,
    }
})