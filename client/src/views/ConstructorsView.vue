<script setup lang="ts">
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import type { Constructor } from '@/types/Constructor.ts';
import ConstructorCard from '@/components/ConstructorCard.vue';
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";
import SearchSelectLabel from "@/components/ui/SearchSelectLabel.vue";
import Stats from "@/components/ui/Stats.vue";

const userStore = useUserInfoStore();
const {
    moderatorPerm,
    secondPerm,
} = storeToRefs(userStore);

const constructors = ref<Constructor[]>([]);
const form = ref({
    name: '',
    born_at: '',
    died_at: null as string | null
});
const editingId = ref<number | null>(null);

const strTitles = computed(() => constructors.value.map(c => c.name));
const filterTitle = ref<string>("");
const filterBornDateFrom = ref<string>("");
const filterBornDateTo = ref<string>("");
const filterDieDateFrom = ref<string>("");
const filterDieDateTo = ref<string>("");
const correctDate = ref<boolean>(true);

onBeforeMount(async () => {
    await loadConstructors();
});

const constructorsCardData = computed<ArmedConflict[]>(() => {
    let data = constructors.value.map(constructor => {
        return {
            id: constructor.id,
            name: constructor.name,
            born_at: constructor.born_at,
            died_at: constructor.died_at,
        };
    });

    if (filterTitle.value) {
        data = data.filter(c => c.name === filterTitle.value);
    }
    if (filterBornDateFrom.value) {
        data = data.filter(c => c.born_at >= filterBornDateFrom.value);
    }
    if (filterBornDateTo.value) {
        data = data.filter(c => c.born_at <= filterBornDateTo.value);
    }
    if (filterDieDateFrom.value) {
        data = data.filter(c => c.died_at >= filterDieDateFrom.value);
    }
    if (filterDieDateTo.value) {
        data = data.filter(c => c.died_at <= filterDieDateTo.value);
    }

    return data;
})

async function loadConstructors() {
    const r = await axios.get('/api/constructors/');
    constructors.value = r.data;
}

async function submitForm() {
    try {
        if (form.value.died_at && form.value.died_at < form.value.born_at) {
            correctDate.value = false;
            return;
        }
        correctDate.value = true;

        const dataToSend = {
            ...form.value,
            died_at: form.value.died_at || null
        };

        let response;

        if (editingId.value !== null) {
            response = await axios.put(`/api/constructors/${editingId.value}/`, dataToSend);

            const index = constructors.value.findIndex(c => c.id === editingId.value);
            if (index !== -1) {
                constructors.value[index] = response.data;
            }

            alert('Конструктор обновлен');
        } else {
            response = await axios.post('/api/constructors/', dataToSend);
            constructors.value.push(response.data);
            alert('Конструктор добавлен');
        }

        resetForm();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка добавления или обновления конструктора');
    }
}

function resetForm() {
    form.value = {
        name: '',
        born_at: '',
        died_at: null
    };
    editingId.value = null;
}

function startEditing(id: number) {
    const original = constructors.value.find(c => c.id === id);
    if (!original) return;

    form.value = {
        name: original.name,
        born_at: original.born_at,
        died_at: original.died_at
    };

    editingId.value = original.id;

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function deleteConstructor(id: number) {
    try {
        await axios.delete(`/api/constructors/${id}/`);
        constructors.value = constructors.value.filter(c => c.id !== id);
    } catch (error) {
        console.error('Ошибка при удалении:', error);
        alert('Не удалось удалить конструктора');
    }
}
</script>

<template>
    <form @submit.prevent="submitForm" v-if="moderatorPerm">
        <fieldset>
            <legend>{{ editingId !== null ? 'Редактирование конструктора' : 'Создание нового конструктора' }}</legend>
            <div class="mb-3">
                <label class="form-label">Имя конструктора</label>
                <input type="text" class="form-control" placeholder="Введите имя" v-model="form.name" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Дата рождения</label>
                <input type="date" class="form-control" v-model="form.born_at" required>
            </div>
            <div class="mb-3">
                <label class="form-label d-flex">Дата смерти
                    <div class="text-danger ms-2" v-if="!correctDate">Дата смерти не может быть раньше даты рождения.</div>
                </label>
                <input type="date" class="form-control" v-model="form.died_at">
            </div>
            <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    {{ editingId !== null ? 'Сохранить изменения' : 'Создать конструктора' }}
                </button>
                <button v-if="editingId !== null" type="button" class="btn btn-secondary" @click="resetForm">
                    Отмена
                </button>
            </div>
        </fieldset>
    </form>

    <fieldset class="mt-4 mb-2">
        <legend>Фильтрация конструкторов</legend>
        <label class="form-label d-flex">Название:</label>
        <search-select-label :items="strTitles" v-model="filterTitle" />
        <div class="mb-2"></div>
        <div class="row mb-3">
            <div class="col-md-6">
                <label class="form-label">Дата рождения от:</label>
                <input type="date" class="form-control" v-model="filterBornDateFrom">
            </div>
            <div class="col-md-6">
                <label class="form-label">Дата рождения до:</label>
                <input type="date" class="form-control" v-model="filterBornDateTo">
            </div>
        </div>
        <div class="row mb-3">
            <div class="col-md-6">
                <label class="form-label">Дата смерти от:</label>
                <input type="date" class="form-control" v-model="filterDieDateFrom">
            </div>
            <div class="col-md-6">
                <label class="form-label">Дата смерти до:</label>
                <input type="date" class="form-control" v-model="filterDieDateTo">
            </div>
        </div>
    </fieldset>

    <stats v-if="moderatorPerm" url="constructors" />

    <div class="d-flex flex-column gap-3 mt-4 mb-2">
        <div v-for="constructor in constructorsCardData" :key="constructor.id">
            <constructor-card :constructor="constructor" @deleteConstructor="deleteConstructor"
                @updateConstructor="startEditing" />
        </div>
    </div>
</template>