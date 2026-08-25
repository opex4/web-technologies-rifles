<script setup lang="ts">
import type { AttachmentCardData } from '@/types/AttachmentCardData.ts';

const props = defineProps<{
    attachment: AttachmentCardData,
}>();

const emit = defineEmits<{
    (e: 'deleteAttachment', id: number): void;
    (e: 'updateAttachment', id: number): void;
}>();

const onDelAttachment = () => {
    if (confirm(`Вы уверены, что хотите удалить "${props.attachment.title}"?`)) {
        emit('deleteAttachment', props.attachment.id);
    }
};

const onUpdateAttachment = () => {
    emit('updateAttachment', props.attachment.id);
};
</script>

<template>
    <div class="card border-light">
        <div class="card-header border-light">
            <div class="container">
                <div class="d-flex justify-content-between align-items-center">
                    <h2 class="d-flex justify-content-center align-items-center m-0">
                        {{ attachment.title }}
                    </h2>
                    <div class="d-flex justify-content-end">
                        <button type="button" class="btn btn-success m-1" @click="onUpdateAttachment">Update</button>
                        <button type="button" class="btn btn-danger m-1" @click="onDelAttachment">Delete</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-body">
            <p class="m-0">
                Тип крепления: <strong>{{ attachment.mountName }}</strong>
            </p>
        </div>
    </div>
</template>