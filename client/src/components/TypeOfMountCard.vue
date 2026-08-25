<script setup lang="ts">
import type { TypeOfMountCardData } from '@/types/TypeOfMountCardData.ts';

const props = defineProps<{
    mount: TypeOfMountCardData,
}>();

const emit = defineEmits<{
    (e: 'deleteMount', id: number): void;
    (e: 'updateMount', id: number): void;
}>();

const onDelMount = () => {
    if (confirm(`Вы уверены, что хотите удалить "${props.mount.title}"?`)) {
        emit('deleteMount', props.mount.id);
    }
};

const onUpdateMount = () => {
    emit('updateMount', props.mount.id);
};
</script>

<template>
    <div class="card border-light">
        <div class="card-header border-light">
            <div class="container">
                <div class="d-flex justify-content-between align-items-center">
                    <h2 class="d-flex justify-content-center align-items-center m-0">
                        {{ mount.title }}
                    </h2>
                    <div class="d-flex justify-content-end">
                        <button type="button" class="btn btn-success m-1" @click="onUpdateMount">Update</button>
                        <button type="button" class="btn btn-danger m-1" @click="onDelMount">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>