<script setup lang="ts">
    import { ref, onBeforeMount } from "vue";
    import { storeToRefs } from "pinia";
    import { useUserInfoStore } from "@/stores/user_info_store.ts";
    import axios from 'axios';
    import { useRouter } from "vue-router";

    const router = useRouter();
    const username = ref<string>('');
    const password = ref<string>(''); 
    const confirmPassword = ref<string>('');
    const userInfoStore = useUserInfoStore();
    const {
        isAuth,
    } = storeToRefs(userInfoStore);
    const isReg = ref<boolean>(false);

    function showAuthOrRegister() {
        isReg.value = !isReg.value;
        username.value = '';
        password.value = '';
        confirmPassword.value = '';
    }

    async function onLoginFormSubmit() {
        if (!isReg.value){
            try{
                const r = await axios.post("/api/users/login/", {
                    username: username.value,
                    password: password.value,
                });

                username.value = '';
                password.value = '';

                await userInfoStore.fetchUserInfo();

                if (isAuth.value){
                    router.replace({ name: 'RiflesView' });
                }
            } catch (error: any) {
                if (error.response?.data?.status == "failed"){
                    alert('Неверный пароль');
                }
                username.value = '';
                password.value = '';               
            }
        } else {
            if (password.value != confirmPassword.value){
                alert('Пароли не совпадают');
                confirmPassword.value = '';
                return;
            }

            try{
                const r = await axios.post("/api/users/create/", {
                    username: username.value,
                    password: password.value,
                });

                await userInfoStore.fetchUserInfo();

                if (isAuth.value){
                    router.replace({ name: 'RiflesView' });
                }   
            }
            catch (error: any) {
                if (error.response?.data?.status == "usernameFailed"){
                    alert('Пользователь с таким именем уже существует');
                }
                username.value = '';
                password.value = '';
                confirmPassword.value = '';                
            }         
        }
        
    }

    onBeforeMount(async () => {
        await userInfoStore.fetchUserInfo();
        if (isAuth.value){
            router.replace({ name: 'RiflesView' });
        }
    })

</script>

<template>
    <div class="mt-4">
        <legend>{{ isReg == false ? 'Авторизация' : 'Регистрация' }}</legend>
        <form @submit.stop.prevent="onLoginFormSubmit">
            <div class="mb-3">
                <label for="username" class="form-label">Имя пользователя</label>
                <input type="text" class="form-control" v-model="username">
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Пароль</label>
                <input type="password" class="form-control" v-model="password">
            </div>
            <div class="mb-3" v-if="isReg">
                <label for="confirmPassword" class="form-label">Повторение пароля</label>
                <input type="password" class="form-control" v-model="confirmPassword">
            </div>
            <div class="d-flex gap-2">
                <button 
                    type="submit" 
                    class="btn btn-primary"
                >{{ isReg == false ? 'Войти' : 'Зарегистрироваться' }}</button>
                <button
                    type="button" 
                    class="btn btn-secondary"
                    @click="showAuthOrRegister"
                >{{ isReg == false ? 'У меня ещё нет аккаунта' : 'У меня уже есть аккаунт' }}</button>
            </div>
        </form>
    </div>
</template>

