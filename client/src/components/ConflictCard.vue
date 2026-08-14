<script setup lang="ts">
import type { ArmedConflict } from "@/types/ArmedConflict.ts";

const props = defineProps<{
    conflict: ArmedConflict,
}>();

const emit = defineEmits<{
    (e: 'deleteConflict', id: number): void;
    (e: 'updateConflict', id: number): void;
}>();

const onDelConflict = () => {
    if (confirm(`Вы уверены, что хотите удалить "${props.conflict.title}"?`)) {
        emit('deleteConflict', props.conflict.id);
    }
};

const onUpdateConflict = () => {
    emit('updateConflict', props.conflict.id);
};
</script>

<template>
    <div class="card border-light">
        <div class="card-header border-light">
            <div class="container">
                <div class="d-flex justify-content-between align-items-center">
                    <h2 class="d-flex justify-content-center align-items-center m-0">
                        {{ conflict.title }}
                    </h2>
                    <div class="d-flex justify-content-end">
                        <button type="button" class="btn btn-success m-1" @click="onUpdateConflict">Update</button>
                        <button type="button" class="btn btn-danger m-1" @click="onDelConflict">Delete</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-body">
            <p class="m-0">
                Дата начала: {{ conflict.started_at }}
            </p>
            <p class="m-0" v-if="conflict.finished_at">
                Дата окончания: {{ conflict.finished_at }}
            </p>
        </div>
    </div>
</template>