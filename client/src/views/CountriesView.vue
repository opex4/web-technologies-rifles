<script setup lang="ts">
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import type { Country } from '@/types/Country.ts';
import CountryCard from '@/components/CountryCard.vue';
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";
import SearchSelectLabel from "@/components/ui/SearchSelectLabel.vue";

const userStore = useUserInfoStore();
const {
    moderatorPerm,
    secondPerm,
} = storeToRefs(userStore);

const countries = ref<Country[]>([]);
const form = ref({
    name: ''
});
const editingId = ref<number | null>(null);

const strTitles = computed(() => countries.value.map(c => c.name));
const filterTitle = ref<string>("");

onBeforeMount(async () => {
    await loadCountries();
});

const countriesCardData = computed<Country[]>(() => {
        let data = countries.value.map(country => {
        return {
            id: country.id,
            name: country.name,
        };
    });

    if (filterTitle.value) {
        data = data.filter(c => c.name === filterTitle.value);
    }

    return data;
})

async function loadCountries() {
    countries.value = await axios.get('/api/countries/')
        .then(res => res.data as Country[]);
}

async function submitForm() {
    try {
        let response;
        
        if (editingId.value !== null) {
            response = await axios.put(`/api/countries/${editingId.value}/`, form.value);
            
            const index = countries.value.findIndex(c => c.id === editingId.value);
            if (index !== -1) {
                countries.value[index] = response.data;
            }
            
            alert('Страна обновлена');
        } else {
            response = await axios.post('/api/countries/', form.value);
            countries.value.push(response.data);
            alert('Страна добавлена');
        }
        
        resetForm();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка добавления или обновления страны');
    }
}

function resetForm() {
    form.value = {
        name: ''
    };
    editingId.value = null;
}

function startEditing(id: number) {
    const original = countries.value.find(c => c.id === id);
    if (!original) return;
    
    form.value = {
        name: original.name
    };
    
    editingId.value = original.id;
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function deleteCountry(id: number) {
    try {
        await axios.delete(`/api/countries/${id}/`);
        countries.value = countries.value.filter(c => c.id !== id);
    } catch (error) {
        console.error('Ошибка при удалении:', error);
        alert('Не удалось удалить страну');
    }
}
</script>

<template>
    <form @submit.prevent="submitForm" v-if="moderatorPerm && secondPerm">
        <fieldset>
            <legend>{{ editingId !== null ? 'Редактирование страны' : 'Создание новой страны' }}</legend>
            <div class="mb-3">
                <label class="form-label">Название страны</label>
                <input type="text" class="form-control" placeholder="Введите название" v-model="form.name" required>
            </div>
            <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    {{ editingId !== null ? 'Сохранить изменения' : 'Создать страну' }}
                </button>
                <button 
                    v-if="editingId !== null" 
                    type="button" 
                    class="btn btn-secondary"
                    @click="resetForm"
                >
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

    <div class="d-flex flex-column gap-3 mt-4 mb-2">
        <div v-for="country in countriesCardData" :key="country.id">
            <CountryCard 
                :country="country"
                @deleteCountry="deleteCountry"
                @updateCountry="startEditing"
            />
        </div>
    </div>
</template>