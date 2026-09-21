<script setup lang="ts">
import { ref, onBeforeMount } from 'vue';
import type { Sats } from '@/types/Stats.ts';
import axios from 'axios';

const props = defineProps<{
    url: string;
}>();

const sats = ref<Sats>();

onBeforeMount(async () => {
    await loadStats();
});

async function loadStats() {
    sats.value = await axios.get(`/api/${props.url}/stats/`)
        .then(res => res.data as Sats);
}
</script>

<template>
    <legend class="mt-2">Статистика</legend>
    <div class="d-flex justify-content-between gap-2">
        <div class="d-flex justify-content-between">
            <span>Всего записей: {{ sats?.count }}</span>
        </div>
        <div class="d-flex justify-content-between">
            <span>Средний ID: {{ sats?.avg?.toFixed(2) }}</span>
        </div>
        <div class="d-flex justify-content-between">
            <span>Макс. ID: {{ sats?.max }}</span>
        </div>
        <div class="d-flex justify-content-between">
            <span>Мин. ID: {{ sats?.min }}</span>
        </div>
    </div>
</template>