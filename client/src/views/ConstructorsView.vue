<script setup lang="ts">
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import type { Constructor } from '@/types/Constructor.ts';
import ConstructorCard from '@/components/ConstructorCard.vue';
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";

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

onBeforeMount(async () => {
    await loadConstructors();
});

async function loadConstructors() {
    constructors.value = await axios.get('/api/constructors/')
        .then(res => res.data as Constructor[]);
}

async function submitForm() {
    try {
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
    <form @submit.prevent="submitForm" v-if="moderatorPerm && secondPerm">
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
                <label class="form-label">Дата смерти</label>
                <input type="date" class="form-control" v-model="form.died_at">
            </div>
            <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    {{ editingId !== null ? 'Сохранить изменения' : 'Создать конструктора' }}
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

    <div class="d-flex flex-column gap-3 mt-4 mb-2">
        <div v-for="constructor in constructors" :key="constructor.id">
            <ConstructorCard 
                :constructor="constructor"
                @deleteConstructor="deleteConstructor"
                @updateConstructor="startEditing"
            />
        </div>
    </div>
</template>