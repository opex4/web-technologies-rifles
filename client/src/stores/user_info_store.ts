import { defineStore } from 'pinia';
import type {User} from "@/types/User.ts";
import { ref, computed } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';

export const useUserInfoStore = defineStore('userInfoStore', () => {
    const userInfo = ref<User>();
    const username = ref<string>("");
    const isAuth = ref<boolean>(null);
    const isStaff = ref<boolean>(false);
    const permissions = ref<string[]>([]);
    const type = ref<string>();
    const second = ref<boolean>(null);

    const readerPerm  = computed<boolean>(() => type.value === 'reader' || type.value === 'builder' || type.value === 'moderator');
    const builderPerm = computed<boolean>(() => type.value === 'builder' || type.value === 'moderator');
    const moderatorPerm = computed<boolean>(() => type.value === 'moderator');
    const secondPerm = computed<boolean>(() => second.value === true);

    async function fetchUserInfo() {
        userInfo.value = await axios.get('/api/users/my/')
            .then(res => res.data as User);

        username.value = userInfo.value?.username;
        isAuth.value = userInfo.value?.isAuth;
        isStaff.value = userInfo.value?.isStaff;
        permissions.value = userInfo.value?.permissions;
        type.value = userInfo.value?.type;
        second.value = userInfo.value?.second;

        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    }

    return {
        userInfo,
        username,
        isAuth,
        isStaff,
        type,
        second,
        fetchUserInfo,

        readerPerm,
        builderPerm,
        moderatorPerm,
        secondPerm,
    }
})