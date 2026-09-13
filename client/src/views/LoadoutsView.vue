<script setup lang="ts">
import axios from 'axios';
import { onBeforeMount, ref, computed } from 'vue';
import type { Loadout } from '@/types/Loadout.ts';
import type { LoadoutCardData } from '@/types/LoadoutCardData.ts';
import type { Rifle } from '@/types/Rifle.ts';
import type { Attachment } from '@/types/Attachment.ts';
import type { TypeOfMount } from '@/types/TypeOfMount.ts';
import LoadoutCard from '@/components/LoadoutCard.vue';
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";

const userStore = useUserInfoStore();
const {
    builderPerm,
    secondPerm,
} = storeToRefs(userStore);

const loadouts = ref([] as Loadout[]);
const loadoutCardData = ref([] as LoadoutCardData[]);
const rifles = ref([] as Rifle[]);
const attachments = ref([] as Attachment[]);
const mounts = ref([] as TypeOfMount[]);

const rifleMountsAttachments = computed(() => {
    const rifle = rifles.value.find(r => r.id === form.value.rifle);
    if (!rifle) return [];

    return rifle.types_of_mounts.map(mountId => {
        const mount = mounts.value.find(m => m.id === mountId);
        if (!mount) return null;
        return {
            mount,
            availableAttachments: attachments.value.filter(a => a.type_of_mount === mountId),
        };
    }).filter(item => item !== null);
});

const form = ref({
    title: '',
    rifle: null as number | null,
    attachments: {} as Record<number, number | null>,
});

const editingId = ref<number | null>(null);
const titleIsEmpty = ref(false);
const rifleIsEmpty = ref(false);

onBeforeMount(async () => {
    await Promise.all([loadLoadouts(), loadRifles(), loadAttachments(), loadTypesOfMounts()]);
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

    async function loadTypesOfMounts() {
        mounts.value = await axios.get('/api/types_of_mounts/')
            .then(res => res.data as TypeOfMount[]);
    }

function getLoadoutCardData() {
    loadoutCardData.value = loadouts.value.map(loadout => {
        const rifle = rifles.value.find(r => r.id === loadout.rifle);
        return {
            id: loadout.id,
            title: loadout.title,
            rifleName: rifle.title,
            creatorName: loadout.creator,
            attachmentNames: loadout.attachments.map(id => {
                const att = attachments.value.find(a => a.id === id);
                return att.title;
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

    const attachmentIds = Object.values(form.value.attachments)
        .filter((id): id is number => id !== null);

    const payload = {
        title: form.value.title,
        rifle: form.value.rifle,
        attachments: attachmentIds,
    };

    try {
        let response;
        if (editingId.value !== null) {
            response = await axios.put(`/api/loadouts/${editingId.value}/`, payload);
            const index = loadouts.value.findIndex(l => l.id === editingId.value);
            if (index !== -1) loadouts.value[index] = response.data;
            alert('Сборка обновлена');
        } else {
            response = await axios.post('/api/loadouts/', payload);
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
        attachments: {},
    };
    editingId.value = null;
    titleIsEmpty.value = false;
    rifleIsEmpty.value = false;
}

function startEditing(id: number) {
    const original = loadouts.value.find(l => l.id === id);
    if (!original) return;

    form.value.title = original.title;
    form.value.rifle = original.rifle;

    const attachmentsMap: Record<number, number | null> = {};
    original.attachments.forEach(attId => {
        const att = attachments.value.find(a => a.id === attId);
        if (att) {
            attachmentsMap[att.type_of_mount] = attId;
        }
    });
    form.value.attachments = attachmentsMap;

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
    <form @submit.prevent="submitForm" v-if="builderPerm && secondPerm">
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
            </div>
            <div class="mb-3" v-if="rifleMountsAttachments.length > 0">
                <label class="form-label">Типы креплений:</label>
                <div v-for="item in rifleMountsAttachments" :key="item.mount.id">
                    <label class="form-label small text-muted">{{ item.mount.title }}</label>
                    <select class="form-select" v-model="form.attachments[item.mount.id]">
                        <option :value="null">Не выбрано</option>
                        <option v-for="attachment in item.availableAttachments" :key="attachment.id" :value="attachment.id">
                            {{ attachment.title }}
                        </option>
                    </select>
                </div>
            </div>
            <div class="mb-3 text-muted" v-else-if="form.rifle !== null">
                У выбранной винтовки нет типов креплений
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