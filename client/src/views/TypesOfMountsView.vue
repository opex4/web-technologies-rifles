<script setup lang="ts">
import axios from 'axios';
import { onBeforeMount, ref } from 'vue';
import type { TypeOfMount } from '@/types/TypeOfMount.ts';
import type { TypeOfMountCardData } from '@/types/TypeOfMountCardData.ts';
import TypeOfMountCard from '@/components/TypeOfMountCard.vue';

const mounts = ref([] as TypeOfMount[]);
const mountCardData = ref([] as TypeOfMountCardData[]);
const form = ref({ title: '' });
const editingId = ref<number | null>(null);
const titleIsEmpty = ref(false);

onBeforeMount(async () => {
    await loadMounts();
    getMountCardData();
});

async function loadMounts() {
    mounts.value = await axios.get('/api/types_of_mounts/')
        .then(res => res.data as TypeOfMount[]);
}

function getMountCardData() {
    mountCardData.value = mounts.value.map(mount => ({
        id: mount.id,
        title: mount.title
    }));
}

async function submitForm() {
    if (form.value.title.trim() === '') {
        titleIsEmpty.value = true;
        return;
    }
    titleIsEmpty.value = false;

    try {
        let response;
        if (editingId.value !== null) {
            response = await axios.put(`/api/types_of_mounts/${editingId.value}/`, form.value);
            const index = mounts.value.findIndex(m => m.id === editingId.value);
            if (index !== -1) mounts.value[index] = response.data;
            alert('Тип крепления обновлён');
        } else {
            response = await axios.post('/api/types_of_mounts/', form.value);
            mounts.value.push(response.data);
            alert('Тип крепления добавлен');
        }
        resetForm();
        getMountCardData();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка сохранения');
    }
}

function resetForm() {
    form.value = { title: '' };
    editingId.value = null;
    titleIsEmpty.value = false;
}

function startEditing(id: number) {
    const original = mounts.value.find(m => m.id === id);
    if (!original) return;
    form.value = { title: original.title };
    editingId.value = original.id;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function deleteMount(id: number) {
    try {
        await axios.delete(`/api/types_of_mounts/${id}/`);
        mounts.value = mounts.value.filter(m => m.id !== id);
        getMountCardData();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось удалить');
    }
}
</script>

<template>
    <form @submit.prevent="submitForm">
        <fieldset>
            <legend>{{ editingId !== null ? 'Редактирование типа крепления' : 'Создание нового типа крепления' }}</legend>
            <div class="mb-3">
                <label class="form-label d-flex">Название<div class="text-danger ms-2" v-if="titleIsEmpty">Обязательное поле</div></label>
                <input type="text" class="form-control" placeholder="Введите название" v-model="form.title" required>
            </div>
            <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    {{ editingId !== null ? 'Сохранить изменения' : 'Создать тип крепления' }}
                </button>
                <button v-if="editingId !== null" type="button" class="btn btn-secondary" @click="resetForm">Отмена</button>
            </div>
        </fieldset>
    </form>

    <div class="d-flex flex-column gap-3 mt-4 mb-2">
        <div v-for="mount in mountCardData" :key="mount.id">
            <type-of-mount-card 
                :mount="mount"
                @deleteMount="deleteMount"
                @updateMount="startEditing"
            />
        </div>
    </div>
</template>