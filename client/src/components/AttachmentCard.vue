<script setup lang="ts">
import type { AttachmentCardData } from '@/types/AttachmentCardData.ts';
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";

const userStore = useUserInfoStore();
const {
    builderPerm,
    secondPerm,
} = storeToRefs(userStore);

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
                    <div class="d-flex justify-content-end" v-if="builderPerm">
                        <button type="button" class="btn btn-success m-1" @click="onUpdateAttachment" v-if="secondPerm">Update</button>
                        <button type="button" class="btn btn-danger m-1" @click="onDelAttachment">Delete</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-body">
            <p class="m-0">
                Тип крепления: {{ attachment.mountName }}
            </p>
        </div>
        <div v-if="attachment.picture" class="card-body border-top d-flex flex-column align-items-center">
            <span>Картинка:</span>
            <img
                :src="attachment.picture"
                :alt="attachment.title"
                class="img-fluid rounded mt-2 cp"
                data-bs-toggle="modal"
                :data-bs-target="'#attachmentImageModal-' + attachment.id"
            >
        </div>
    </div>

    <div class="modal fade" :id="'attachmentImageModal-' + attachment.id" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ attachment.title }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body text-center">
                    <img :src="attachment.picture" class="img-fluid lg" :alt="attachment.title">
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.cp {
    cursor: pointer;
}

.img-fluid.lg {
    width: 100%;
    height: 100%;
}
</style>