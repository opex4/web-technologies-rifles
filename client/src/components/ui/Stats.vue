<script setup lang="ts">
import { ref, onBeforeMount } from 'vue';
import type { Stats } from '@/types/Stats.ts';
import axios from 'axios';

const props = defineProps<{
    url: string;
}>();

const stats = ref<Stats>();

onBeforeMount(async () => {
    await loadStats();
});

async function loadStats() {
    const r = await axios.get(`/api/${props.url}/stats/`);
    stats.value = r.data;
}
</script>

<template>
    <legend class="mt-2">Статистика</legend>
    <div class="d-flex justify-content-between gap-2">
        <div class="d-flex justify-content-between">
            <span>Всего записей: {{ stats?.count }}</span>
        </div>
        <div class="d-flex justify-content-between">
            <span>Средний ID: {{ stats?.avg?.toFixed(2) }}</span>
        </div>
        <div class="d-flex justify-content-between">
            <span>Макс. ID: {{ stats?.max }}</span>
        </div>
        <div class="d-flex justify-content-between">
            <span>Мин. ID: {{ stats?.min }}</span>
        </div>
    </div>
</template>