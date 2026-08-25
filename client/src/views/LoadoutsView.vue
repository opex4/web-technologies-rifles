<script setup lang="ts">
import axios from 'axios';
import { onBeforeMount, ref } from 'vue';
import type { Loadout } from '@/types/Loadout.ts';
import type { LoadoutCardData } from '@/types/LoadoutCardData.ts';
import type { Rifle } from '@/types/Rifle.ts';
import type { Attachment } from '@/types/Attachment.ts';
import type { UserProfile } from '@/types/UserProfile.ts';
import LoadoutCard from '@/components/LoadoutCard.vue';

const loadouts = ref([] as Loadout[]);
const loadoutCardData = ref([] as LoadoutCardData[]);
const rifles = ref([] as Rifle[]);
const attachments = ref([] as Attachment[]);
const userProfiles = ref([] as UserProfile[]);

const form = ref({
    title: '',
    rifle: null as number | null,
    creator: null as number | null,
    attachments: [] as number[]
});
const editingId = ref<number | null>(null);
const titleIsEmpty = ref(false);
const rifleIsEmpty = ref(false);
const creatorIsEmpty = ref(false);

onBeforeMount(async () => {
    await Promise.all([loadLoadouts(), loadRifles(), loadAttachments(), loadUserProfiles()]);
    getLoadoutCardData();
});

async function loadLoadouts() {
    loadouts.value = await axios.get('/api/loadouts/')
        .then(res => res.data as Loadout[]);
}

async function loadRifles() {
    rifles.value = await axios.get('/api/rifles/')
        .then(res => res.data as Rifle[]);
}

async function loadAttachments() {
    attachments.value = await axios.get('/api/attachments/')
        .then(res => res.data as Attachment[]);
}

async function loadUserProfiles() {
    userProfiles.value = await axios.get('/api/user_profiles/')
        .then(res => res.data as UserProfile[]);
}

function getLoadoutCardData() {
    loadoutCardData.value = loadouts.value.map(loadout => {
        const rifle = rifles.value.find(r => r.id === loadout.rifle);
        const creator = userProfiles.value.find(u => u.id === loadout.creator);
        return {
            id: loadout.id,
            title: loadout.title,
            rifleName: rifle ? rifle.title : 'Неизвестно',
            creatorName: creator ? creator.user_username : 'Неизвестно',
            attachmentNames: loadout.attachments.map(id => {
                const att = attachments.value.find(a => a.id === id);
                return att ? att.title : 'Неизвестно';
            })
        };
    });
}

async function submitForm() {
    if (form.value.title.trim() === '') {
        titleIsEmpty.value = true;
        return;
    }
    titleIsEmpty.value = false;

    if (form.value.rifle === null) {
        rifleIsEmpty.value = true;
        return;
    }
    rifleIsEmpty.value = false;

    if (form.value.creator === null) {
        creatorIsEmpty.value = true;
        return;
    }
    creatorIsEmpty.value = false;

    try {
        let response;
        if (editingId.value !== null) {
            response = await axios.put(`/api/loadouts/${editingId.value}/`, form.value);
            const index = loadouts.value.findIndex(l => l.id === editingId.value);
            if (index !== -1) loadouts.value[index] = response.data;
            alert('Сборка обновлена');
        } else {
            response = await axios.post('/api/loadouts/', form.value);
            loadouts.value.push(response.data);
            alert('Сборка создана');
        }
        resetForm();
        getLoadoutCardData();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка сохранения');
    }
}

function resetForm() {
    form.value = {
        title: '',
        rifle: null,
        creator: null,
        attachments: []
    };
    editingId.value = null;
    titleIsEmpty.value = false;
    rifleIsEmpty.value = false;
    creatorIsEmpty.value = false;
}

function startEditing(id: number) {
    const original = loadouts.value.find(l => l.id === id);
    if (!original) return;
    form.value = {
        title: original.title,
        rifle: original.rifle,
        creator: original.creator,
        attachments: original.attachments
    };
    editingId.value = original.id;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function deleteLoadout(id: number) {
    try {
        await axios.delete(`/api/loadouts/${id}/`);
        loadouts.value = loadouts.value.filter(l => l.id !== id);
        getLoadoutCardData();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось удалить');
    }
}
</script>

<template>
    <form @submit.prevent="submitForm">
        <fieldset>
            <legend>{{ editingId !== null ? 'Редактирование сборки' : 'Создание новой сборки' }}</legend>
            <div class="mb-3">
                <label class="form-label d-flex">Название<div class="text-danger ms-2" v-if="titleIsEmpty">Обязательное поле</div></label>
                <input type="text" class="form-control" placeholder="Введите название" v-model="form.title" required>
            </div>
            <div class="row mb-3">
                <div class="col-md-6">
                    <label class="form-label d-flex">Винтовка<div class="text-danger ms-2" v-if="rifleIsEmpty">Обязательное поле</div></label>
                    <select class="form-select" v-model="form.rifle" required>
                        <option :value="null" disabled>Выберите винтовку</option>
                        <option v-for="rifle in rifles" :key="rifle.id" :value="rifle.id">
                            {{ rifle.title }}
                        </option>
                    </select>
                </div>
                <div class="col-md-6">
                    <label class="form-label d-flex">Создатель<div class="text-danger ms-2" v-if="creatorIsEmpty">Обязательное поле</div></label>
                    <select class="form-select" v-model="form.creator" required>
                        <option :value="null" disabled>Выберите пользователя</option>
                        <option v-for="profile in userProfiles" :key="profile.id" :value="profile.id">
                            {{ profile.user_username }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label">Обвесы</label>
                <select class="form-select" multiple size="5" v-model="form.attachments">
                    <option v-for="attachment in attachments" :key="attachment.id" :value="attachment.id">
                        {{ attachment.title }}
                    </option>
                </select>
                <div class="form-text">Зажмите Ctrl для выбора нескольких элементов</div>
            </div>
            <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    {{ editingId !== null ? 'Сохранить изменения' : 'Создать сборку' }}
                </button>
                <button v-if="editingId !== null" type="button" class="btn btn-secondary" @click="resetForm">Отмена</button>
            </div>
        </fieldset>
    </form>

    <div class="d-flex flex-column gap-3 mt-4 mb-2">
        <div v-for="loadout in loadoutCardData" :key="loadout.id">
            <loadout-card 
                :loadout="loadout"
                @deleteLoadout="deleteLoadout"
                @updateLoadout="startEditing"
            />
        </div>
    </div>
</template>