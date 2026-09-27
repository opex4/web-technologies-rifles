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
import SearchSelectIdLabel from "@/components/ui/SearchSelectIdLabel.vue";
import SearchSelectLabel from "@/components/ui/SearchSelectLabel.vue";
import Stats from "@/components/ui/Stats.vue";

const userStore = useUserInfoStore();
const {
    builderPerm,
    secondPerm,
    moderatorPerm,
} = storeToRefs(userStore);

const loadouts = ref([] as Loadout[]);
const rifles = ref([] as Rifle[]);
const attachments = ref([] as Attachment[]);
const mounts = ref([] as TypeOfMount[]);
interface UserName {
    username: string;
}
const usernames = ref([] as UserName[]);

const strCreators = computed(() => usernames.value.map(u => u.username));
const strRifles = computed(() => rifles.value.map(r => r.title));
const strAtts = computed(() => attachments.value.map(a => a.title));
const strTitles = computed(() => loadouts.value.map(l => l.title));
const filterCreator = ref<string>("");
const filterRifle = ref<string>("");
const filterAtt = ref<string>("");
const filterTitle = ref<string>("");

const rifleMountsAttachments = computed(() => {
    const rifle = rifles.value.find(r => r.id === form.value.rifle);
    if (!rifle) return [];

    return rifle.types_of_mounts.map(mountId => {
        const mount = mounts.value.find(m => m.id === mountId);
        if (!mount) return null;
        return {
            mountId: mount.id,
            mountTitle: mount.title,
            availableAttachments: attachments.value
                .filter(a => a.type_of_mount === mountId)
                .map(a => ({ id: a.id, label: a.title })),
        };
    }).filter(item => item !== null);
});

const searchSelectRifle = computed(() =>
    rifles.value.map(r => ({ id: r.id, label: r.title }))
);

const form = ref({
    title: '',
    rifle: null as number | null,
    attachments: {} as Record<number, number | null>,
});

const editingId = ref<number | null>(null);
const titleIsEmpty = ref(false);
const rifleIsEmpty = ref(false);

onBeforeMount(async () => {
    if (moderatorPerm.value) {
        await loadUserNames();
    }
    await Promise.all([loadAttachments(), loadTypesOfMounts(), loadLoadouts(), loadRifles()]);
});

const loadoutCardData = computed<LoadoutCardData[]>(() => {
    if (loadouts.value.length === 0 || rifles.value.length === 0) {
        return [];
    }

    return loadouts.value.map(loadout => {
        const rifle = rifles.value.find(r => r.id === loadout.rifle);
        return {
            id: loadout.id,
            title: loadout.title,
            rifleName: rifle.title,
            creatorName: loadout.creator,
            attachmentNames: loadout.attachments.map(id => {
                const att = attachments.value.find(a => a.id === id);
                return att?.title;
            })
        };
    });
});

const filteredLoadoutCardData = computed<LoadoutCardData[]>(() => {
    let data = loadoutCardData.value;

    if (filterCreator.value) {
        data = data.filter(l => l.creatorName === filterCreator.value);
    }
    if (filterRifle.value) {
        data = data.filter(l => l.rifleName === filterRifle.value);
    }
    if (filterAtt.value) {
        data = data.filter(l => l.attachmentNames.includes(filterAtt.value));
    }
    if (filterTitle.value) {
        data = data.filter(l => l.title === filterTitle.value);
    }

    return data;
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

async function loadUserNames() {
    usernames.value = await axios.get('/api/users/list/')
        .then(res => res.data as UserName[]);
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
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Не удалось удалить');
    }
}

function onRifleChange() {
    form.value.attachments = {};
}
</script>

<template>
    <form @submit.prevent="submitForm" v-if="builderPerm">
        <fieldset>
            <legend>{{ editingId !== null ? 'Редактирование сборки' : 'Создание новой сборки' }}</legend>
            <div class="mb-3">
                <label class="form-label d-flex">Название<div class="text-danger ms-2" v-if="titleIsEmpty">Обязательное
                        поле</div></label>
                <input type="text" class="form-control" placeholder="Введите название" v-model="form.title" required>
            </div>
            <div class="mb-3">
                <label class="form-label d-flex">Винтовка<div class="text-danger ms-2" v-if="rifleIsEmpty">
                        Обязательное поле</div></label>
                <search-select-id-label :items="searchSelectRifle" v-model="form.rifle"
                    @update:modelValue="onRifleChange" />
            </div>
            <div class="mb-3" v-if="rifleMountsAttachments.length > 0">
                <label class="form-label">Типы креплений:</label>
                <div v-for="item in rifleMountsAttachments" :key="item.mountId">
                    <label class="form-label small text-muted">{{ item.mountTitle }}</label>
                    <search-select-id-label :items="item.availableAttachments"
                        v-model="form.attachments[item.mountId]" />
                </div>
            </div>
            <div class="mb-3 text-muted" v-else-if="form.rifle !== null">
                У выбранной винтовки нет типов креплений
            </div>
            <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary">
                    {{ editingId !== null ? 'Сохранить изменения' : 'Создать сборку' }}
                </button>
                <button v-if="editingId !== null" type="button" class="btn btn-secondary"
                    @click="resetForm">Отмена</button>
            </div>
        </fieldset>
    </form>

    <fieldset class="mt-4 mb-2">
        <legend>Фильтрация карточек</legend>
        <label class="form-label d-flex">Название:</label>
        <search-select-label :items="strTitles" v-model="filterTitle" />
        <label class="form-label d-flex mt-2" v-if="moderatorPerm">Создатель:</label>
        <search-select-label :items="strCreators" v-model="filterCreator" />
        <label class="form-label d-flex mt-2">Винтовка:</label>
        <search-select-label :items="strRifles" v-model="filterRifle" />
        <label class="form-label d-flex mt-2">Обвес:</label>
        <search-select-label :items="strAtts" v-model="filterAtt" />
    </fieldset>

    <stats v-if="moderatorPerm" url="loadouts" />
    
    <div class="d-flex flex-column gap-3 mt-4 mb-2">
        <div v-for="loadout in filteredLoadoutCardData" :key="loadout.id">
            <loadout-card :loadout="loadout" @deleteLoadout="deleteLoadout" @updateLoadout="startEditing" />
        </div>
    </div>
</template>