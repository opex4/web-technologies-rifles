<script setup lang="ts">
    import axios from 'axios';
    import { onBeforeMount, ref } from "vue";
    import type {AmmoType} from "@/types/AmmoType.ts";
    import type {Constructor} from "@/types/Constructor.ts";
    import type {ArmedConflict} from "@/types/ArmedConflict.ts";
    import type {Rifle} from "@/types/Rifle.ts";
    import type {Country} from "@/types/Country.ts";
    import type {RifleCardData} from "@/types/RifleCardData.ts";
    import type {TypeOfMount} from "@/types/TypeOfMount.ts";
    import RifleCard from "@/components/RifleCard.vue";

    const countries = ref([] as Country[]);
    const ammoTypes = ref([] as AmmoType[]);
    const constructors = ref([] as Constructor[]);
    const armedConflicts = ref([] as ArmedConflict[]);
    const rifles = ref([] as Rifle[]);
    const rifleCardData = ref([] as RifleCardData[]);
    const typesOfMounts = ref([] as TypeOfMount[]);
    const form = ref({
        title: '',
        description: '',
        created_at: '',
        ammo_type: null as number,
        country_of_origin: null as number,
        constructors: [] as number[],
        used_in_conflicts: [] as number[],
        types_of_mounts: [] as number[]
    });
    const editingId = ref<number | null>(null);
    const constructorIsEmpty = ref(false);
    const ammoIsEmpty = ref(false);
    const countryIsEmpty = ref(false);

    onBeforeMount(async () => {
        await loadAll();
        await getRifleCardData();
    })

    async function getRifleCardData () {
        rifleCardData.value = rifles.value.map(rifle => {
            const ammo = ammoTypes.value.find(a => a.id === rifle.ammo_type);
            const country = countries.value.find(c => c.id === rifle.country_of_origin);
            
            return {
                id: rifle.id,
                title: rifle.title,
                description: rifle.description,
                created_at: rifle.created_at,
                ammoName: ammo!.title,
                countryName: country!.name,
                constructorNames: rifle.constructors.map(id => 
                    constructors.value.find(c => c.id === id)!.name
                ),
                conflictNames: rifle.used_in_conflicts.map(id => 
                    armedConflicts.value.find(c => c.id === id)!.title
                ),
                mountNames: rifle.types_of_mounts.map(id => 
                    typesOfMounts.value.find(m => m.id === id)!.title
                ),
            };
        });
    }

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
            let response;
        
            if (editingId.value !== null) {
                response = await axios.put(`/api/rifles/${editingId.value}/`, form.value);
                
                const index = rifles.value.findIndex(r => r.id === editingId.value);
                if (index !== -1) {
                    rifles.value[index] = response.data;
                }
                
                alert('Винтовка обновлена');
            } else {
                response = await axios.post('/api/rifles/', form.value);
                rifles.value.push(response.data);
                alert('Винтовка добавлена');
            }
        
            resetForm();
            getRifleCardData();
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
            types_of_mounts: []
        };
        editingId.value = null;
        constructorIsEmpty.value = false;
        ammoIsEmpty.value = false;
        countryIsEmpty.value = false;
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
            types_of_mounts: original.types_of_mounts
        };
        
        editingId.value = original.id;
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    async function deleteRifle(id: number) {
        try {
            await axios.delete(`/api/rifles/${id}/`);
            rifles.value = rifles.value.filter(r => r.id !== id);
            getRifleCardData();
        } catch (error) {
            console.error('Ошибка при удалении:', error);
            alert('Не удалось удалить винтовку');
        }
    }
</script>

<template>
    <form @submit.prevent="submitForm">
        <fieldset>
        <legend>{{ editingId !== null ? 'Редактирование винтовки' : 'Создание новой винтовки' }}</legend>
        <div class="mb-3">
            <label class="form-label">Название</label>
            <input type="text" class="form-control" placeholder="Введите название" v-model="form.title" required>
        </div>
        <div class="mb-3">
            <label class="form-label">Описание</label>
            <textarea class="form-control" rows="3" placeholder="Добавьте описание" v-model="form.description" required></textarea>
        </div>
        <div class="mb-3">
            <label class="form-label">Дата создания</label>
            <input type="date" class="form-control" v-model="form.created_at" required>
        </div>
        <div class="row mb-3">
            <div class="col-md-6">
                <label class="form-label d-flex">Патрон<div class="text-danger ms-2" v-if="ammoIsEmpty">Обязательное поле</div></label>
                <select class="form-select" v-model="form.ammo_type">
                    <option :value="null" disabled>Выберите патрон</option>
                    <option v-for="ammo in ammoTypes" :key="ammo.id" :value="ammo.id">
                        {{ ammo.title }}
                    </option>
                </select>
            </div>
            <div class="col-md-6">
                <label class="form-label d-flex">Страна происхождения<div class="text-danger ms-2" v-if="countryIsEmpty">Обязательное поле</div></label>
                <select class="form-select" v-model="form.country_of_origin">
                    <option :value="null" disabled>Выберите страну</option>
                    <option v-for="country in countries" :key="country.id" :value="country.id">
                        {{ country.name }}
                    </option>
                </select>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-label d-flex">Конструкторы<div class="text-danger ms-2" v-if="constructorIsEmpty">Обязательное поле</div></label>
            <select class="form-select" multiple size="5" v-model="form.constructors">
                <option v-for="constructor in constructors" :key="constructor.id" :value="constructor.id">
                    {{ constructor.name }}
                </option>
            </select>
            <div class="form-text">Зажмите Ctrl для выбора нескольких элементов</div>
        </div>
        <div class="mb-3">
            <label class="form-label">Типы креплений</label>
            <select class="form-select" multiple size="5" v-model="form.types_of_mounts">
                <option v-for="mount in typesOfMounts" :key="mount.id" :value="mount.id">
                    {{ mount.title }}
                </option>
            </select>
            <div class="form-text">Зажмите Ctrl для выбора нескольких элементов</div>
        </div>
        <div class="mb-3">
            <label class="form-label">Применено в конфликтах</label>
            <select class="form-select" multiple size="5" v-model="form.used_in_conflicts">
                <option v-for="conflict in armedConflicts" :key="conflict.id" :value="conflict.id">
                    {{ conflict.title }}
                </option>
            </select>
            <div class="form-text">Зажмите Ctrl для выбора нескольких элементов</div>
        </div>
        <div class="d-flex gap-2">
            <button type="submit" class="btn btn-primary">
                {{ editingId !== null ? 'Сохранить изменения' : 'Создать винтовку' }}
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
    <div v-for="rifle in rifleCardData" :key="rifle.id">
            <rifle-card 
                :rifle="rifle"
                @deleteRifle="deleteRifle"
                @updateRifle="startEditing"
            />
        </div>
    </div>
</template>
