<script setup lang="ts">
import type { Country } from "@/types/Country.ts";

const props = defineProps<{
    country: Country,
}>();

const emit = defineEmits<{
    (e: 'deleteCountry', id: number): void;
    (e: 'updateCountry', id: number): void;
}>();

const onDelCountry = () => {
    if (confirm(`Вы уверены, что хотите удалить "${props.country.name}"?`)) {
        emit('deleteCountry', props.country.id);
    }
};

const onUpdateCountry = () => {
    emit('updateCountry', props.country.id);
};
</script>

<template>
    <div class="card border-light">
        <div class="card-header border-light">
            <div class="container">
                <div class="d-flex justify-content-between align-items-center">
                    <h2 class="d-flex justify-content-center align-items-center m-0">
                        {{ country.name }}
                    </h2>
                    <div class="d-flex justify-content-end">
                        <button type="button" class="btn btn-success m-1" @click="onUpdateCountry">Update</button>
                        <button type="button" class="btn btn-danger m-1" @click="onDelCountry">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>