<script setup lang="ts">
import axios from 'axios';
import { onBeforeMount, ref, computed } from 'vue';
import type { TypeOfMount } from '@/types/TypeOfMount.ts';
import type { TypeOfMountCardData } from '@/types/TypeOfMountCardData.ts';
import TypeOfMountCard from '@/components/TypeOfMountCard.vue';
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";
import SearchSelectLabel from "@/components/ui/SearchSelectLabel.vue";
import Stats from "@/components/ui/Stats.vue";

const userStore = useUserInfoStore();
const {
    builderPerm,
    secondPerm,
    moderatorPerm,
} = storeToRefs(userStore);

const mounts = ref([] as TypeOfMount[]);
const form = ref({ title: '' });
const editingId = ref<number | null>(null);
const titleIsEmpty = ref(false);

const strTitles = computed(() => mounts.value.map(m => m.title));
const filterTitle = ref<string>("");

onBeforeMount(async () => {
    await loadMounts();
});

async function loadMounts() {
    mounts.value = await axios.get('/api/types_of_mounts/')
        .then(res => res.data as TypeOfMount[]);
}

const mountCardData = computed<TypeOfMountCardData[]>(() => {
    let data = mounts.value.map(mount => ({
        id: mount.id,
        title: mount.title
    }));

    if (filterTitle.value) {
        data = data.filter(m => m.title === filterTitle.value);
    }

    return data;
});

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
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось удалить');
    }
}
</script>

<template>
    <form @submit.prevent="submitForm" v-if="builderPerm">
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

    <fieldset class="mt-4 mb-2">
        <legend>Фильтрация карточек</legend>
        <label class="form-label d-flex">Название:</label>
        <search-select-label :items="strTitles" v-model="filterTitle" />
    </fieldset>

    <stats v-if="moderatorPerm" url="types_of_mounts" />

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