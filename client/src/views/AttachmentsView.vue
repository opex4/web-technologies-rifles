<script setup lang="ts">
import axios from 'axios';
import { onBeforeMount, ref, watch, computed } from 'vue';
import type { Attachment } from '@/types/Attachment.ts';
import type { AttachmentCardData } from '@/types/AttachmentCardData.ts';
import type { TypeOfMount } from '@/types/TypeOfMount.ts';
import AttachmentCard from '@/components/AttachmentCard.vue';
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";
import SearchSelectIdLabel from "@/components/ui/SearchSelectIdLabel.vue";
import SearchSelectLabel from "@/components/ui/SearchSelectLabel.vue";
import Stats from "@/components/ui/Stats.vue";

const userStore = useUserInfoStore();
const {
    builderPerm,
    secondPerm,
    moderatorPerm,
} = storeToRefs(userStore);

const attachments = ref([] as Attachment[]);
const typesOfMounts = ref([] as TypeOfMount[]);
const form = ref({
    title: '',
    type_of_mount: null as number | null
});
const editingId = ref<number | null>(null);
const titleIsEmpty = ref(false);
const mountIsEmpty = ref(false);
const pictureRef = ref<HTMLInputElement>();
const preview = ref<string | null>(null);

const searchSelectTypeOfMount = computed(() => typesOfMounts.value.map(m => ({ id: m.id, label: m.title })));

const strTitles = computed(() => attachments.value.map(a => a.title));
const strMounts = computed(() => typesOfMounts.value.map(m => m.title));
const filterTitles = ref<string>("");
const filterMounts = ref<string>("");
const filterIsPicture = ref<boolean>(false);
const filterIsNotPicture = ref<boolean>(false);

onBeforeMount(async () => {
    await Promise.all([loadAttachments(), loadTypesOfMounts()]);
});

async function loadAttachments() {
    attachments.value = await axios.get('/api/attachments/')
        .then(res => res.data as Attachment[]);
}

async function loadTypesOfMounts() {
    typesOfMounts.value = await axios.get('/api/types_of_mounts/')
        .then(res => res.data as TypeOfMount[]);
}

const attachmentCardData = computed<AttachmentCardData[]>(() => {
    let data = attachments.value.map(att => {
        const mount = typesOfMounts.value.find(m => m.id === att.type_of_mount);
        return {
            id: att.id,
            title: att.title,
            mountName: mount.title,
            picture: att.picture,
        };
    });

    if (filterIsPicture.value) {
        data = data.filter(a => a.picture);
    }
    if (filterIsNotPicture.value) {
        data = data.filter(a => !a.picture);
    }
    if (filterTitles.value) {
        data = data.filter(a => a.title === filterTitles.value);
    }
    if (filterMounts.value) {
        data = data.filter(a => a.mountName === filterMounts.value);
    }

    return data;
})

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
        const formData = new FormData();
        formData.append('title', form.value.title);
        formData.append('type_of_mount', String(form.value.type_of_mount));

        const file = pictureRef.value?.files?.[0];
        if (file) {
            formData.append('picture', file);
        } else {
            formData.append('picture', '');
        }

        let response;
        if (editingId.value !== null) {
            response = await axios.put(`/api/attachments/${editingId.value}/`, formData);
            const index = attachments.value.findIndex(a => a.id === editingId.value);
            if (index !== -1) attachments.value[index] = response.data;
            alert('Обвес обновлён');
        } else {
            response = await axios.post('/api/attachments/', formData);
            attachments.value.push(response.data);
            alert('Обвес добавлен');
        }
        resetForm();
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
    onDelPicture();
}

function startEditing(id: number) {
    const original = attachments.value.find(a => a.id === id);
    if (!original) return;
    form.value = {
        title: original.title,
        type_of_mount: original.type_of_mount
    };
    preview.value = original.picture || null;
    if (pictureRef.value) {
        pictureRef.value.value = '';
    }
    editingId.value = original.id;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function deleteAttachment(id: number) {
    try {
        await axios.delete(`/api/attachments/${id}/`);
        attachments.value = attachments.value.filter(a => a.id !== id);
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось удалить');
    }
}

function onFileChange() {
    const file = pictureRef.value?.files?.[0];
    if (preview.value) {
        URL.revokeObjectURL(preview.value);
    }
    preview.value = file ? URL.createObjectURL(file) : null;
}

function onDelPicture() {
    if (pictureRef.value) {
        pictureRef.value.value = '';
    }
    if (preview.value) {
        URL.revokeObjectURL(preview.value);
    }
    preview.value = null;
}

watch(filterIsPicture, (newValue, oldValue) => {
    if (filterIsNotPicture.value && filterIsPicture.value) {
        filterIsNotPicture.value = false;
    }
});

watch(filterIsNotPicture, (newValue, oldValue) => {
    if (filterIsNotPicture.value && filterIsPicture.value) {
        filterIsPicture.value = false;
    }
});
</script>

<template>
    <form @submit.prevent="submitForm" v-if="builderPerm">
        <fieldset>
            <legend>{{ editingId !== null ? 'Редактирование обвеса' : 'Создание нового обвеса' }}</legend>
            <div class="mb-3">
                <label class="form-label d-flex">Название<div class="text-danger ms-2" v-if="titleIsEmpty">Обязательное
                        поле</div></label>
                <input type="text" class="form-control" placeholder="Введите название" v-model="form.title" required>
            </div>
            <div class="mb-3">
                <label class="form-label d-flex">Тип крепления<div class="text-danger ms-2" v-if="mountIsEmpty">
                    Обязательное поле</div></label>
                <search-select-id-label :items="searchSelectTypeOfMount" v-model="form.type_of_mount" />
            </div>
            <div class="mb-3">
                <label class="form-label">Загрузить картинку</label>
                <input class="form-control" type="file" accept="image/*" ref="pictureRef" @change="onFileChange">
                <div v-if="preview" class="mt-3 d-flex gap-2 align-items-end">
                    <img :src="preview" alt="Картинка" class="mw-200">
                    <div>
                        <button type="button" class="btn btn-secondary" @click="onDelPicture">Удалить картинку</button>
                    </div>
                </div>
            </div>
            <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    {{ editingId !== null ? 'Сохранить изменения' : 'Создать обвес' }}
                </button>
                <button v-if="editingId !== null" type="button" class="btn btn-secondary"
                    @click="resetForm">Отмена</button>
            </div>
        </fieldset>
    </form>

    <fieldset class="mt-4 mb-2">
        <legend>Фильтрация карточек</legend>
        <label class="form-label d-flex">Название:</label>
        <search-select-label :items="strTitles" v-model="filterTitles" />
        <label class="form-label d-flex">Крепление:</label>
        <search-select-label :items="strMounts" v-model="filterMounts" />
        <label class="form-label d-flex">Картинка:</label>
        <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="filterIsPicture">
            <label class="form-check-label">С картинкой</label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="filterIsNotPicture">
            <label class="form-check-label">Без картинки</label>
        </div>
    </fieldset>

    <stats v-if="moderatorPerm" url="attachments" />

    <div class="d-flex flex-column gap-3 mt-4 mb-2">
        <div v-for="attachment in attachmentCardData" :key="attachment.id">
            <attachment-card :attachment="attachment" @deleteAttachment="deleteAttachment"
                @updateAttachment="startEditing" />
        </div>
    </div>
</template>