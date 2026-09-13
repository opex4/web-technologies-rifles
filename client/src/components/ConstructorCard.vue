<script setup lang="ts">
import type { Constructor } from "@/types/Constructor.ts";
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";

const userStore = useUserInfoStore();
const {
    moderatorPerm,
    secondPerm,
} = storeToRefs(userStore);

const props = defineProps<{
    constructor: Constructor,
}>();

const emit = defineEmits<{
    (e: 'deleteConstructor', id: number): void;
    (e: 'updateConstructor', id: number): void;
}>();

const onDelConstructor = () => {
    if (confirm(`Вы уверены, что хотите удалить "${props.constructor.name}"?`)) {
        emit('deleteConstructor', props.constructor.id);
    }
};

const onUpdateConstructor = () => {
    emit('updateConstructor', props.constructor.id);
};
</script>

<template>
    <div class="card border-light">
        <div class="card-header border-light">
            <div class="container">
                <div class="d-flex justify-content-between align-items-center">
                    <h2 class="d-flex justify-content-center align-items-center m-0">
                        {{ constructor.name }}
                    </h2>
                    <div class="d-flex justify-content-end" v-if="moderatorPerm && secondPerm">
                        <button type="button" class="btn btn-success m-1" @click="onUpdateConstructor">Update</button>
                        <button type="button" class="btn btn-danger m-1" @click="onDelConstructor">Delete</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-body">
            <p class="m-0">
                Дата рождения: {{ constructor.born_at }}
            </p>
            <p class="m-0" v-if="constructor.died_at">
                Дата смерти: {{ constructor.died_at }}
            </p>
        </div>
    </div>
</template>