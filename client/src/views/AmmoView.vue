<script setup lang="ts">
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import type { AmmoType } from '@/types/AmmoType.ts';
import AmmoCard from '@/components/AmmoCard.vue';

const ammoList = ref<AmmoType[]>([]);
const form = ref({
    title: ''
});
const editingId = ref<number | null>(null);

onBeforeMount(async () => {
    await loadAmmo();
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
    <form @submit.prevent="submitForm">
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
        <div v-for="ammo in ammoList" :key="ammo.id">
            <AmmoCard 
                :ammo="ammo"
                @deleteAmmo="deleteAmmo"
                @updateAmmo="startEditing"
            />
        </div>
    </div>
</template>