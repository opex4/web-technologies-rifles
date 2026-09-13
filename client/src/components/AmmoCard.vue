<script setup lang="ts">
import type { AmmoType } from "@/types/AmmoType.ts";
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";

const userStore = useUserInfoStore();
const {
    moderatorPerm,
    secondPerm,
} = storeToRefs(userStore);

const props = defineProps<{
    ammo: AmmoType,
}>();

const emit = defineEmits<{
    (e: 'deleteAmmo', id: number): void;
    (e: 'updateAmmo', id: number): void;
}>();

const onDelAmmo = () => {
    if (confirm(`Вы уверены, что хотите удалить "${props.ammo.title}"?`)) {
        emit('deleteAmmo', props.ammo.id);
    }
};

const onUpdateAmmo = () => {
    emit('updateAmmo', props.ammo.id);
};
</script>

<template>
    <div class="card border-light">
        <div class="card-header border-light">
            <div class="container">
                <div class="d-flex justify-content-between align-items-center">
                    <h2 class="d-flex justify-content-center align-items-center m-0">
                        {{ ammo.title }}
                    </h2>
                    <div class="d-flex justify-content-end" v-if="moderatorPerm && secondPerm">
                        <button type="button" class="btn btn-success m-1" @click="onUpdateAmmo">Update</button>
                        <button type="button" class="btn btn-danger m-1" @click="onDelAmmo">Delete</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>