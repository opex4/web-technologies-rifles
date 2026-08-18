<script setup lang="ts">
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';

interface TypeOfMount {
    id: number;
    title: string;
}

const mounts = ref([] as TypeOfMount[]);
const form = ref({ title: '' });

onBeforeMount(async () => {
    await loadMounts();
});

async function loadMounts() {
    const res = await axios.get('/api/types_of_mounts/');
    mounts.value = res.data;
}

async function submitForm() {
    try {
        const response = await axios.post('/api/types_of_mounts/', form.value);
        mounts.value.push(response.data);
        form.value = { title: '' };
        alert('Тип крепления добавлен');
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка добавления');
    }
}

async function deleteMount(id: number) {
    try {
        await axios.delete(`/api/types_of_mounts/${id}/`);
        mounts.value = mounts.value.filter(m => m.id !== id);
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось удалить');
    }
}
</script>

<template>
    <h2 class="mt-4">Типы креплений</h2>

    <form @submit.prevent="submitForm" class="mb-4">
        <div class="row g-2">
            <div class="col-md-8">
                <input 
                    type="text" 
                    class="form-control" 
                    placeholder="Название типа крепления" 
                    v-model="form.title" 
                    required
                >
            </div>
            <div class="col-md-4">
                <button type="submit" class="btn btn-primary w-100">Добавить</button>
            </div>
        </div>
    </form>

    <div class="list-group">
        <div 
            v-for="mount in mounts" 
            :key="mount.id" 
            class="list-group-item d-flex justify-content-between align-items-center"
        >
            <span>{{ mount.title }}</span>
            <button 
                class="btn btn-sm btn-outline-danger" 
                @click="deleteMount(mount.id)"
            >
                Удалить
            </button>
        </div>
    </div>
</template>