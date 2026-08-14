<script setup lang="ts">
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import type { ArmedConflict } from '@/types/ArmedConflict.ts';
import ConflictCard from '@/components/ConflictCard.vue';

const conflicts = ref<ArmedConflict[]>([]);
const form = ref({
    title: '',
    started_at: '',
    finished_at: null as string | null
});
const editingId = ref<number | null>(null);

onBeforeMount(async () => {
    await loadConflicts();
});

async function loadConflicts() {
    conflicts.value = await axios.get('/api/armed_conflicts/')
        .then(res => res.data as ArmedConflict[]);
}

async function submitForm() {
    try {
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
    <form @submit.prevent="submitForm">
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
                <label class="form-label">Дата окончания</label>
                <input type="date" class="form-control" v-model="form.finished_at">
            </div>
            <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    {{ editingId !== null ? 'Сохранить изменения' : 'Создать конфликт' }}
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
        <div v-for="conflict in conflicts" :key="conflict.id">
            <ConflictCard 
                :conflict="conflict"
                @deleteConflict="deleteConflict"
                @updateConflict="startEditing"
            />
        </div>
    </div>
</template>