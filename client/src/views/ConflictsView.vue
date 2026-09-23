<script setup lang="ts">
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import type { ArmedConflict } from '@/types/ArmedConflict.ts';
import ConflictCard from '@/components/ConflictCard.vue';
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";
import SearchSelectLabel from "@/components/ui/SearchSelectLabel.vue";
import Stats from "@/components/ui/Stats.vue";

const userStore = useUserInfoStore();
const {
    moderatorPerm,
    secondPerm,
} = storeToRefs(userStore);

const conflicts = ref<ArmedConflict[]>([]);
const form = ref({
    title: '',
    started_at: '',
    finished_at: null as string | null
});
const editingId = ref<number | null>(null);

const strTitles = computed(() => conflicts.value.map(l => l.title));
const filterTitle = ref<string>("");
const filterDateFrom = ref<string>("");
const filterDateTo = ref<string>("");
const correctDate = ref<boolean>(true);

onBeforeMount(async () => {
    await loadConflicts();
});

async function loadConflicts() {
    conflicts.value = await axios.get('/api/armed_conflicts/')
        .then(res => res.data as ArmedConflict[]);
}

const conflictsCardData = computed<ArmedConflict[]>(() => {
    let data = conflicts.value.map(conflict => {
        return {
            id: conflict.id,
            title: conflict.title,
            started_at: conflict.started_at,
            finished_at: conflict.finished_at,
        };
    });

    if (filterTitle.value) {
        data = data.filter(c => c.title === filterTitle.value);
    }
    if (filterDateFrom.value) {
        data = data.filter(c => c.started_at >= filterDateFrom.value);
    }
    if (filterDateTo.value) {
        data = data.filter(c => c.started_at <= filterDateTo.value);
    }

    return data;
})

async function submitForm() {
    try {
        if (form.value.finished_at && form.value.finished_at < form.value.started_at) {
            correctDate.value = false;
            return;
        }
        correctDate.value = true;

        const dataToSend = {
            ...form.value,
            finished_at: form.value.finished_at || null
        };

        let response;

        if (editingId.value !== null) {
            response = await axios.put(`/api/armed_conflicts/${editingId.value}/`, dataToSend);

            const index = conflicts.value.findIndex(c => c.id === editingId.value);
            if (index !== -1) {
                conflicts.value[index] = response.data;
            }

            alert('Конфликт обновлен');
        } else {
            response = await axios.post('/api/armed_conflicts/', dataToSend);
            conflicts.value.push(response.data);
            alert('Конфликт добавлен');
        }

        resetForm();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка добавления или обновления конфликта');
    }
}

function resetForm() {
    form.value = {
        title: '',
        started_at: '',
        finished_at: null
    };
    editingId.value = null;
}

function startEditing(id: number) {
    const original = conflicts.value.find(c => c.id === id);
    if (!original) return;

    form.value = {
        title: original.title,
        started_at: original.started_at,
        finished_at: original.finished_at
    };

    editingId.value = original.id;

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function deleteConflict(id: number) {
    try {
        await axios.delete(`/api/armed_conflicts/${id}/`);
        conflicts.value = conflicts.value.filter(c => c.id !== id);
    } catch (error) {
        console.error('Ошибка при удалении:', error);
        alert('Не удалось удалить конфликт');
    }
}
</script>

<template>
    <form @submit.prevent="submitForm" v-if="moderatorPerm">
        <fieldset>
            <legend>{{ editingId !== null ? 'Редактирование конфликта' : 'Создание нового конфликта' }}</legend>
            <div class="mb-3">
                <label class="form-label">Название конфликта</label>
                <input type="text" class="form-control" placeholder="Введите название" v-model="form.title" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Дата начала</label>
                <input type="date" class="form-control" v-model="form.started_at" required>
            </div>
            <div class="mb-3">
                <label class="form-label d-flex">Дата окончания
                    <div class="text-danger ms-2" v-if="!correctDate">Дата окончания не может быть раньше даты начала.</div>
                </label>
                <input type="date" class="form-control" v-model="form.finished_at">
            </div>
            <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    {{ editingId !== null ? 'Сохранить изменения' : 'Создать конфликт' }}
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
        <div class="mb-2"></div>
        <div class="row mb-3">
            <div class="col-md-6">
                <label class="form-label">Дата начала от:</label>
                <input type="date" class="form-control" v-model="filterDateFrom">
            </div>
            <div class="col-md-6">
                <label class="form-label">Дата начала до:</label>
                <input type="date" class="form-control" v-model="filterDateTo">
            </div>
        </div>
    </fieldset>

    <stats v-if="moderatorPerm" url="armed_conflicts" />

    <div class="d-flex flex-column gap-3 mt-4 mb-2">
        <div v-for="conflict in conflictsCardData" :key="conflict.id">
            <ConflictCard :conflict="conflict" @deleteConflict="deleteConflict" @updateConflict="startEditing" />
        </div>
    </div>
</template>