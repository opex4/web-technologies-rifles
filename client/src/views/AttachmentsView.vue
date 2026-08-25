<script setup lang="ts">
import axios from 'axios';
import { onBeforeMount, ref } from 'vue';
import type { Attachment } from '@/types/Attachment.ts';
import type { AttachmentCardData } from '@/types/AttachmentCardData.ts';
import type { TypeOfMount } from '@/types/TypeOfMount.ts';
import AttachmentCard from '@/components/AttachmentCard.vue';

const attachments = ref([] as Attachment[]);
const attachmentCardData = ref([] as AttachmentCardData[]);
const typesOfMounts = ref([] as TypeOfMount[]);
const form = ref({
    title: '',
    type_of_mount: null as number | null
});
const editingId = ref<number | null>(null);
const titleIsEmpty = ref(false);
const mountIsEmpty = ref(false);

onBeforeMount(async () => {
    await Promise.all([loadAttachments(), loadTypesOfMounts()]);
    getAttachmentCardData();
});

async function loadAttachments() {
    attachments.value = await axios.get('/api/attachments/')
        .then(res => res.data as Attachment[]);
}

async function loadTypesOfMounts() {
    typesOfMounts.value = await axios.get('/api/types_of_mounts/')
        .then(res => res.data as TypeOfMount[]);
}

function getAttachmentCardData() {
    attachmentCardData.value = attachments.value.map(att => {
        const mount = typesOfMounts.value.find(m => m.id === att.type_of_mount);
        return {
            id: att.id,
            title: att.title,
            mountName: mount ? mount.title : 'Неизвестно'
        };
    });
}

async function submitForm() {
    if (form.value.title.trim() === '') {
        titleIsEmpty.value = true;
        return;
    }
    titleIsEmpty.value = false;

    if (form.value.type_of_mount === null) {
        mountIsEmpty.value = true;
        return;
    }
    mountIsEmpty.value = false;

    try {
        let response;
        if (editingId.value !== null) {
            response = await axios.put(`/api/attachments/${editingId.value}/`, form.value);
            const index = attachments.value.findIndex(a => a.id === editingId.value);
            if (index !== -1) attachments.value[index] = response.data;
            alert('Обвес обновлён');
        } else {
            response = await axios.post('/api/attachments/', form.value);
            attachments.value.push(response.data);
            alert('Обвес добавлен');
        }
        resetForm();
        getAttachmentCardData();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка сохранения');
    }
}

function resetForm() {
    form.value = { title: '', type_of_mount: null };
    editingId.value = null;
    titleIsEmpty.value = false;
    mountIsEmpty.value = false;
}

function startEditing(id: number) {
    const original = attachments.value.find(a => a.id === id);
    if (!original) return;
    form.value = {
        title: original.title,
        type_of_mount: original.type_of_mount
    };
    editingId.value = original.id;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function deleteAttachment(id: number) {
    try {
        await axios.delete(`/api/attachments/${id}/`);
        attachments.value = attachments.value.filter(a => a.id !== id);
        getAttachmentCardData();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось удалить');
    }
}
</script>

<template>
    <form @submit.prevent="submitForm">
        <fieldset>
            <legend>{{ editingId !== null ? 'Редактирование обвеса' : 'Создание нового обвеса' }}</legend>
            <div class="mb-3">
                <label class="form-label d-flex">Название<div class="text-danger ms-2" v-if="titleIsEmpty">Обязательное поле</div></label>
                <input type="text" class="form-control" placeholder="Введите название" v-model="form.title" required>
            </div>
            <div class="mb-3">
                <label class="form-label d-flex">Тип крепления<div class="text-danger ms-2" v-if="mountIsEmpty">Обязательное поле</div></label>
                <select class="form-select" v-model="form.type_of_mount" required>
                    <option :value="null" disabled>Выберите тип крепления</option>
                    <option v-for="mount in typesOfMounts" :key="mount.id" :value="mount.id">
                        {{ mount.title }}
                    </option>
                </select>
            </div>
            <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    {{ editingId !== null ? 'Сохранить изменения' : 'Создать обвес' }}
                </button>
                <button v-if="editingId !== null" type="button" class="btn btn-secondary" @click="resetForm">Отмена</button>
            </div>
        </fieldset>
    </form>

    <div class="d-flex flex-column gap-3 mt-4 mb-2">
        <div v-for="attachment in attachmentCardData" :key="attachment.id">
            <attachment-card 
                :attachment="attachment"
                @deleteAttachment="deleteAttachment"
                @updateAttachment="startEditing"
            />
        </div>
    </div>
</template>