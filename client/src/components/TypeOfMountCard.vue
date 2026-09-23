<script setup lang="ts">
import type { TypeOfMountCardData } from '@/types/TypeOfMountCardData.ts';
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";

const userStore = useUserInfoStore();
const {
    builderPerm,
    secondPerm,
} = storeToRefs(userStore);

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
                    <div class="d-flex justify-content-end" v-if="builderPerm">
                        <button type="button" class="btn btn-success m-1" @click="onUpdateMount" v-if="secondPerm">Update</button>
                        <button type="button" class="btn btn-danger m-1" @click="onDelMount">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>