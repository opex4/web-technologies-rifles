<script setup lang="ts">

import type {Country} from "@/types/Country.ts";
import axios from 'axios';
import {onBeforeMount, ref} from "vue";
import type {AmmoType} from "@/types/AmmoType.ts";
import type {Constructor} from "@/types/Constructor.ts";
import type {ArmedConflict} from "@/types/ArmedConflict.ts";
import type {Rifle} from "@/types/Rifle.ts";
import RifleCard from "@/components/RifleCard.vue";


const countries = ref([] as Country[]);
const ammoTypes = ref([] as AmmoType[]);
const constructors = ref([] as Constructor[]);
const armedConflicts = ref([] as ArmedConflict[]);
const rifles = ref([] as Rifle[]);


onBeforeMount(async () => {
    await loadAll();
})

async function loadAll() {
    await loadCountries();
    await loadAmmoTypes();
    await loadConstructors();
    await loadArmedConflicts();
    await loadRifles();
}

async function loadCountries() {
    countries.value = await axios.get('/api/countries')
        .then(res => res.data as Country[]);
}

async function loadAmmoTypes() {
    ammoTypes.value = await axios.get('/api/ammo_types')
        .then(res => res.data as AmmoType[]);
}

async function loadConstructors() {
    constructors.value = await axios.get('/api/constructors')
        .then(res => res.data as Constructor[]);
}

async function loadArmedConflicts() {
    armedConflicts.value = await axios.get('/api/armed_conflicts')
        .then(res => res.data as ArmedConflict[]);
}

async function loadRifles() {
    rifles.value = await axios.get('/api/rifles')
        .then(res => res.data as Rifle[]);
}

</script>

<template>
    <div class="container">
        <div class="d-flex flex-column gap-3 mt-4 mb-2">
            <div v-for="rifle in rifles">
                <rifle-card :rifle="rifle"
                            :ammo-types="ammoTypes"
                            :armed-conflicts="armedConflicts"
                            :countries="countries"
                            :constructors="constructors"
                />
            </div>
        </div>
        <button class="w-100 btn btn-primary justify-content-center mb-4" @click="loadAll">
            Обновить
        </button>
    </div>
</template>

