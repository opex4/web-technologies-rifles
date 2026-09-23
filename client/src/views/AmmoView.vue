<script setup lang="ts">
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import type { AmmoType } from '@/types/AmmoType.ts';
import AmmoCard from '@/components/AmmoCard.vue';
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";
import SearchSelectLabel from "@/components/ui/SearchSelectLabel.vue";
import Stats from "@/components/ui/Stats.vue";

const userStore = useUserInfoStore();
const {
    moderatorPerm,
    secondPerm,
} = storeToRefs(userStore);

const ammoList = ref<AmmoType[]>([]);
const form = ref({
    title: ''
});
const editingId = ref<number | null>(null);

const strTitles = computed(() => ammoList.value.map(a => a.title));
const filterTitle = ref<string>("");

onBeforeMount(async () => {
    await loadAmmo();
});

const ammoCardData = computed<AmmoType[]>(() => {
    let data = ammoList.value.map(ammo => {
        return {
            id: ammo.id,
            title: ammo.title,
        };
    });

    if (filterTitle.value) {
        data = data.filter(a => a.title === filterTitle.value);
    }

    return data;
});

async function loadAmmo() {
    ammoList.value = await axios.get('/api/ammo_types/')
        .then(res => res.data as AmmoType[]);
}

async function submitForm() {
    try {
        let response;

        if (editingId.value !== null) {
            response = await axios.put(`/api/ammo_types/${editingId.value}/`, form.value);

            const index = ammoList.value.findIndex(a => a.id === editingId.value);
            if (index !== -1) {
                ammoList.value[index] = response.data;
            }

            alert('Калибр обновлен');
        } else {
            response = await axios.post('/api/ammo_types/', form.value);
            ammoList.value.push(response.data);
            alert('Калибр добавлен');
        }

        resetForm();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка добавления или обновления калибра');
    }
}

function resetForm() {
    form.value = {
        title: ''
    };
    editingId.value = null;
}

function startEditing(id: number) {
    const original = ammoList.value.find(a => a.id === id);
    if (!original) return;

    form.value = {
        title: original.title
    };

    editingId.value = original.id;

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function deleteAmmo(id: number) {
    try {
        await axios.delete(`/api/ammo_types/${id}/`);
        ammoList.value = ammoList.value.filter(a => a.id !== id);
    } catch (error) {
        console.error('Ошибка при удалении:', error);
        alert('Не удалось удалить калибр');
    }
}
</script>

<template>
    <form @submit.prevent="submitForm" v-if="moderatorPerm">
        <fieldset>
            <legend>{{ editingId !== null ? 'Редактирование калибра' : 'Создание нового калибра' }}</legend>
            <div class="mb-3">
                <label class="form-label">Название калибра</label>
                <input type="text" class="form-control" placeholder="Введите название" v-model="form.title" required>
            </div>
            <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    {{ editingId !== null ? 'Сохранить изменения' : 'Создать калибр' }}
                </button>
                <button v-if="editingId !== null" type="button" class="btn btn-secondary" @click="resetForm">
                    Отмена
                </button>
            </div>
        </fieldset>
    </form>

    <fieldset class="mt-4 mb-2">
        <legend>Фильтрация карточек</legend>
        <label class="form-label d-flex">Название:</label>
        <search-select-label :items="strTitles" v-model="filterTitle" />
    </fieldset>

    <stats v-if="moderatorPerm" url="ammo_types" />

    <div class="d-flex flex-column gap-3 mt-4 mb-2">
        <div v-for="ammo in ammoCardData" :key="ammo.id">
            <AmmoCard :ammo="ammo" @deleteAmmo="deleteAmmo" @updateAmmo="startEditing" />
        </div>
    </div>
</template>