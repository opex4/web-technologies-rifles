<script setup lang="ts">
import axios from 'axios';
import { onBeforeMount, ref, computed, watch } from 'vue';
import type { AmmoType } from "@/types/AmmoType.ts";
import type { Constructor } from "@/types/Constructor.ts";
import type { ArmedConflict } from "@/types/ArmedConflict.ts";
import type { Rifle } from "@/types/Rifle.ts";
import type { Country } from "@/types/Country.ts";
import type { RifleCardData } from "@/types/RifleCardData.ts";
import type { TypeOfMount } from "@/types/TypeOfMount.ts";
import RifleCard from "@/components/RifleCard.vue";
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";
import SearchSelectIdLabel from "@/components/ui/SearchSelectIdLabel.vue";
import SearchSelectLabel from "@/components/ui/SearchSelectLabel.vue";

const countries = ref([] as Country[]);
const ammoTypes = ref([] as AmmoType[]);
const constructors = ref([] as Constructor[]);
const armedConflicts = ref([] as ArmedConflict[]);
const rifles = ref([] as Rifle[]);
const typesOfMounts = ref([] as TypeOfMount[]);
const form = ref({
    title: '',
    description: '',
    created_at: '',
    ammo_type: null as number,
    country_of_origin: null as number,
    constructors: [] as number[],
    used_in_conflicts: [] as number[],
    types_of_mounts: [] as number[],
});
const editingId = ref<number | null>(null);
const constructorIsEmpty = ref(false);
const ammoIsEmpty = ref(false);
const countryIsEmpty = ref(false);
const userStore = useUserInfoStore();
const {
    moderatorPerm,
    secondPerm,
} = storeToRefs(userStore);
const pictureRef = ref<HTMLInputElement>();
const preview = ref<string | null>(null);

const filterTitle = ref<string>("");
const filterDateFrom = ref<string>("");
const filterDateTo = ref<string>("");
const filterAmmo = ref<string>("");
const filterCountry = ref<string>("");
const filterConstructor = ref<string>("");
const filterConflict = ref<string>("");
const filterMount = ref<string>("");
const filterHasPicture = ref<boolean>(false);
const filterNoPicture = ref<boolean>(false);

const titlesStr = computed(() => rifles.value.map(r => r.title));
const ammoStr = computed(() => ammoTypes.value.map(a => a.title));
const countryStr = computed(() => countries.value.map(c => c.name));
const constructorStr = computed(() => constructors.value.map(c => c.name));
const conflictStr = computed(() => armedConflicts.value.map(c => c.title));
const mountStr = computed(() => typesOfMounts.value.map(m => m.title));

const searchSelectAmmo = computed(() =>
    ammoTypes.value.map(a => ({ id: a.id, label: a.title }))
);
const searchSelectCountry = computed(() =>
    countries.value.map(c => ({ id: c.id, label: c.name }))
);

const searchConstructor = ref<string>("");
const searchMount = ref<string>("");
const searchConflict = ref<string>("");
const filteredConstructors = computed(() => {
    const search = searchConstructor.value.toLowerCase();
    return constructors.value.filter(c => 
        form.value.constructors.includes(c.id) || 
        c.name.toLowerCase().includes(search)
    );
});
const filteredMounts = computed(() => {
    const search = searchMount.value.toLowerCase();
    return typesOfMounts.value.filter(m => 
        form.value.types_of_mounts.includes(m.id) || 
        m.title.toLowerCase().includes(search)
    );
});
const filteredConflicts = computed(() => {
    const search = searchConflict.value.toLowerCase();
    return armedConflicts.value.filter(c => 
        form.value.used_in_conflicts.includes(c.id) || 
        c.title.toLowerCase().includes(search)
    );
});

watch(filterHasPicture, (newValue) => {
    if (newValue && filterNoPicture.value) filterNoPicture.value = false;
});
watch(filterNoPicture, (newValue) => {
    if (newValue && filterHasPicture.value) filterHasPicture.value = false;
});

onBeforeMount(async () => {
    await loadAll();
})

const rifleCardData = computed<RifleCardData[]>(() => {
    if (rifles.value.length === 0 || countries.value.length === 0 || ammoTypes.value.length === 0) {
        return [];
    }
    if (constructors.value.length === 0 || armedConflicts.value.length === 0 || typesOfMounts.value.length === 0) {
        return [];
    }
    let data = rifles.value.map(rifle => {
        const ammo = ammoTypes.value.find(a => a.id === rifle.ammo_type);
        const country = countries.value.find(c => c.id === rifle.country_of_origin);

        return {
            id: rifle.id,
            title: rifle.title,
            description: rifle.description,
            created_at: rifle.created_at,
            ammoName: ammo.title,
            countryName: country.name,
            constructorNames: rifle.constructors.map(id =>
                constructors.value.find(c => c.id === id).name
            ),
            conflictNames: rifle.used_in_conflicts.map(id =>
                armedConflicts.value.find(c => c.id === id).title
            ),
            mountNames: rifle.types_of_mounts.map(id =>
                typesOfMounts.value.find(m => m.id === id).title
            ),
            picture: rifle.picture,
        };
    });

    if (filterTitle.value) {
        data = data.filter(r => r.title === filterTitle.value);
    }
    if (filterDateFrom.value) {
        data = data.filter(r => r.created_at >= filterDateFrom.value);
    }
    if (filterDateTo.value) {
        data = data.filter(r => r.created_at <= filterDateTo.value);
    }
    if (filterAmmo.value) {
        data = data.filter(r => r.ammoName === filterAmmo.value);
    }
    if (filterCountry.value) {
        data = data.filter(r => r.countryName === filterCountry.value);
    }
    if (filterConstructor.value) {
        data = data.filter(r => r.constructorNames.includes(filterConstructor.value));
    }
    if (filterConflict.value) {
        data = data.filter(r => r.conflictNames.includes(filterConflict.value));
    }
    if (filterMount.value) {
        data = data.filter(r => r.mountNames.includes(filterMount.value));
    }
    if (filterHasPicture.value) {
        data = data.filter(r => r.picture);
    }
    if (filterNoPicture.value) {
        data = data.filter(r => !r.picture);
    }

    return data;
});

async function loadAll() {
    await loadCountries();
    await loadAmmoTypes();
    await loadConstructors();
    await loadArmedConflicts();
    await loadTypesOfMounts();
    await loadRifles();
}

async function loadCountries() {
    countries.value = await axios.get('/api/countries/')
        .then(res => res.data as Country[]);
}

async function loadAmmoTypes() {
    ammoTypes.value = await axios.get('/api/ammo_types/')
        .then(res => res.data as AmmoType[]);
}

async function loadConstructors() {
    constructors.value = await axios.get('/api/constructors/')
        .then(res => res.data as Constructor[]);
}

async function loadArmedConflicts() {
    armedConflicts.value = await axios.get('/api/armed_conflicts/')
        .then(res => res.data as ArmedConflict[]);
}

async function loadTypesOfMounts() {
    typesOfMounts.value = await axios.get('/api/types_of_mounts/')
        .then(res => res.data as TypeOfMount[]);
}

async function loadRifles() {
    rifles.value = await axios.get('/api/rifles/')
        .then(res => res.data as Rifle[]);
}

async function submitForm() {
    if (form.value.ammo_type === null) {
        ammoIsEmpty.value = true;
        return;
    }
    ammoIsEmpty.value = false;

    if (form.value.country_of_origin === null) {
        countryIsEmpty.value = true;
        return;
    }
    countryIsEmpty.value = false;

    if (form.value.constructors.length === 0) {
        constructorIsEmpty.value = true;
        return;
    }
    constructorIsEmpty.value = false;

    try {
        const formData = new FormData();
        formData.append('title', form.value.title);
        formData.append('description', form.value.description);
        formData.append('created_at', form.value.created_at);
        formData.append('ammo_type', String(form.value.ammo_type));
        formData.append('country_of_origin', String(form.value.country_of_origin));
        form.value.constructors.forEach(id => formData.append('constructors', String(id)));
        form.value.used_in_conflicts.forEach(id => formData.append('used_in_conflicts', String(id)));
        form.value.types_of_mounts.forEach(id => formData.append('types_of_mounts', String(id)));

        const file = pictureRef.value?.files?.[0];
        if (file) {
            formData.append('picture', file);
        } else {
            formData.append('picture', '');
        }

        let response;

        if (editingId.value !== null) {
            response = await axios.put(`/api/rifles/${editingId.value}/`, formData);

            const index = rifles.value.findIndex(r => r.id === editingId.value);
            if (index !== -1) {
                rifles.value[index] = response.data;
            }

            alert('Винтовка обновлена');
        } else {
            response = await axios.post('/api/rifles/', formData);
            rifles.value.push(response.data);
            alert('Винтовка добавлена');
        }

        resetForm();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка добавления или обновления винтовки');
    }
}

function resetForm() {
    form.value = {
        title: '',
        description: '',
        created_at: '',
        ammo_type: null,
        country_of_origin: null,
        constructors: [],
        used_in_conflicts: [],
        types_of_mounts: [],
    };
    editingId.value = null;
    constructorIsEmpty.value = false;
    ammoIsEmpty.value = false;
    countryIsEmpty.value = false;
    onDelPicture();
}

function startEditing(id: number) {
    const original = rifles.value.find(r => r.id === id);
    if (!original) return;

    form.value = {
        title: original.title,
        description: original.description,
        created_at: original.created_at,
        ammo_type: original.ammo_type,
        country_of_origin: original.country_of_origin,
        constructors: original.constructors,
        used_in_conflicts: original.used_in_conflicts,
        types_of_mounts: original.types_of_mounts,
    };

    preview.value = original.picture || null;
    if (pictureRef.value) {
        pictureRef.value.value = '';
    }

    editingId.value = original.id;

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function deleteRifle(id: number) {
    try {
        await axios.delete(`/api/rifles/${id}/`);
        rifles.value = rifles.value.filter(r => r.id !== id);
    } catch (error) {
        console.error('Ошибка при удалении:', error);
        alert('Не удалось удалить винтовку');
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
</script>

<template>
    <form @submit.prevent="submitForm" v-if="moderatorPerm && secondPerm">
        <fieldset>
            <legend>{{ editingId !== null ? 'Редактирование винтовки' : 'Создание новой винтовки' }}</legend>
            <div class="mb-3">
                <label class="form-label">Название</label>
                <input type="text" class="form-control" placeholder="Введите название" v-model="form.title" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Описание</label>
                <textarea class="form-control" rows="3" placeholder="Добавьте описание" v-model="form.description"
                    required></textarea>
            </div>
            <div class="mb-3">
                <label class="form-label">Дата создания</label>
                <input type="date" class="form-control" v-model="form.created_at" required>
            </div>
            <div class="row mb-3">
                <div class="col-md-6">
                    <label class="form-label d-flex">Патрон<div class="text-danger ms-2" v-if="ammoIsEmpty">Обязательное
                            поле</div></label>
                    <search-select-id-label :items="searchSelectAmmo" v-model="form.ammo_type" />
                </div>
                <div class="col-md-6">
                    <label class="form-label d-flex">Страна происхождения<div class="text-danger ms-2"
                            v-if="countryIsEmpty">Обязательное поле</div></label>
                    <search-select-id-label :items="searchSelectCountry" v-model="form.country_of_origin" />
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label d-flex">Конструкторы<div class="text-danger ms-2" v-if="constructorIsEmpty">
                        Обязательное поле</div></label>
                <input type="text" class="form-control mb-2" placeholder="Поиск конструктора..."
                    v-model="searchConstructor" />
                <select class="form-select" multiple size="5" v-model="form.constructors">
                    <option v-for="constructor in filteredConstructors" :key="constructor.id" :value="constructor.id">
                        {{ constructor.name }}
                    </option>
                </select>
                <div class="form-text">Зажмите Ctrl для выбора нескольких элементов</div>
            </div>
            <div class="mb-3">
                <label class="form-label">Типы креплений</label>
                <input type="text" class="form-control mb-2" placeholder="Поиск крепления..."
                    v-model="searchMount" />
                <select class="form-select" multiple size="5" v-model="form.types_of_mounts">
                    <option v-for="mount in filteredMounts" :key="mount.id" :value="mount.id">
                        {{ mount.title }}
                    </option>
                </select>
                <div class="form-text">Зажмите Ctrl для выбора нескольких элементов</div>
            </div>
            <div class="mb-3">
                <label class="form-label">Применено в конфликтах</label>
                <input type="text" class="form-control mb-2" placeholder="Поиск конфликта..."
                    v-model="searchConflict" />
                <select class="form-select" multiple size="5" v-model="form.used_in_conflicts">
                    <option v-for="conflict in filteredConflicts" :key="conflict.id" :value="conflict.id">
                        {{ conflict.title }}
                    </option>
                </select>
                <div class="form-text">Зажмите Ctrl для выбора нескольких элементов</div>
            </div>
            <div class="mb-3">
                <label for="formFile" class="form-label">Загрузить картинку</label>
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
                    {{ editingId !== null ? 'Сохранить изменения' : 'Создать винтовку' }}
                </button>
                <button v-if="editingId !== null" type="button" class="btn btn-secondary" @click="resetForm">
                    Отмена
                </button>
            </div>
        </fieldset>
    </form>

    <fieldset class="mt-4 mb-2">
        <legend>Фильтрация карточек</legend>
        <label class="form-label d-flex mt-2">Название:</label>
        <search-select-label :items="titlesStr" v-model="filterTitle" />
        <label class="form-label d-flex mt-2">Страна:</label>
        <search-select-label :items="countryStr" v-model="filterCountry" />

        <div class="mb-2"></div>
        <div class="row mb-3">
            <div class="col-md-6">
                <label class="form-label">Дата создания от:</label>
                <input type="date" class="form-control" v-model="filterDateFrom">
            </div>
            <div class="col-md-6">
                <label class="form-label">Дата создания до:</label>
                <input type="date" class="form-control" v-model="filterDateTo">
            </div>
        </div>

        <label class="form-label d-flex mt-2">Патрон:</label>
        <search-select-label :items="ammoStr" v-model="filterAmmo" />
        <label class="form-label d-flex mt-2">Конструктор:</label>
        <search-select-label :items="constructorStr" v-model="filterConstructor" />
        <label class="form-label d-flex mt-2">Тип крепления:</label>
        <search-select-label :items="mountStr" v-model="filterMount" />
        <label class="form-label d-flex mt-2">Применено в конфликте:</label>
        <search-select-label :items="conflictStr" v-model="filterConflict" />

        <label class="form-label d-flex mt-2">Картинка:</label>
        <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="filterHasPicture">
            <label class="form-check-label">С картинкой</label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="filterNoPicture">
            <label class="form-check-label">Без картинки</label>
        </div>
    </fieldset>

    <div class="d-flex flex-column gap-3 mt-4 mb-2">
        <div v-for="rifle in rifleCardData" :key="rifle.id">
            <rifle-card :rifle="rifle" @deleteRifle="deleteRifle" @updateRifle="startEditing" />
        </div>
    </div>
</template>