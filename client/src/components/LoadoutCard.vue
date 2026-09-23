<script setup lang="ts">
import type { LoadoutCardData } from '@/types/LoadoutCardData.ts';
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";

const userStore = useUserInfoStore();
const {
    username,
    builderPerm,
    secondPerm,
} = storeToRefs(userStore);

const props = defineProps<{
    loadout: LoadoutCardData,
}>();

const emit = defineEmits<{
    (e: 'deleteLoadout', id: number): void;
    (e: 'updateLoadout', id: number): void;
}>();

const onDelLoadout = () => {
    if (confirm(`Вы уверены, что хотите удалить "${props.loadout.title}"?`)) {
        emit('deleteLoadout', props.loadout.id);
    }
};

const onUpdateLoadout = () => {
    emit('updateLoadout', props.loadout.id);
};
</script>

<template>
    <div class="card border-light">
        <div class="card-header border-light">
            <div class="container">
                <div class="d-flex justify-content-between align-items-center">
                    <h2 class="d-flex justify-content-center align-items-center m-0">
                        {{ loadout.title }}
                    </h2>
                    <div class="d-flex justify-content-end" v-if="builderPerm && loadout.creatorName === username">
                        <button type="button" class="btn btn-success m-1" @click="onUpdateLoadout" v-if="secondPerm">Update</button>
                        <button type="button" class="btn btn-danger m-1" @click="onDelLoadout">Delete</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">
                            Винтовка: {{ loadout.rifleName }}
                        </li>
                        <li class="list-group-item">
                            Создатель: {{ loadout.creatorName }}
                        </li>
                    </ul>
                </div>
                <div class="col-md-6">
                    Обвесы:
                    <ul class="m-0">
                        <li v-for="name in loadout.attachmentNames" :key="name">
                            {{ name }}
                        </li>
                        <li v-if="loadout.attachmentNames.length === 0" class="text-muted">
                            Не выбрано
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>