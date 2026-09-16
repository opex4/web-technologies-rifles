<script setup lang="ts">
import type { RifleCardData } from "@/types/RifleCardData.ts";
import { Rifle } from '../types/Rifle';
import { storeToRefs } from "pinia";
import { useUserInfoStore } from "@/stores/user_info_store.ts";

const userStore = useUserInfoStore();
const {
    moderatorPerm,
    secondPerm,
} = storeToRefs(userStore);

const props = defineProps<{
    rifle: RifleCardData,
}>();

const emit = defineEmits<{
    (e: 'deleteRifle', id: number): void;
    (e: 'updateRifle', rifle: RifleCardData): void;
}>();

const onDelRifle = () => {
    if (confirm(`Вы уверены, что хотите удалить "${props.rifle.title}"?`)) {
        emit('deleteRifle', props.rifle.id);
    }
};

const onUpdateRifle = () => {
    emit('updateRifle', props.rifle.id);
};
</script>

<template>
    <div class="card border-light">
        <div class="card-header border-light">
            <div class="container">
                <div class="d-flex justify-content-between align-items-center">
                    <h2 class="d-flex justify-content-center align-items-center m-0">
                        {{ rifle.title }}
                    </h2>
                    <div class="d-flex justify-content-end" v-if="moderatorPerm && secondPerm">
                        <button type="button" class="btn btn-success m-1" @click="onUpdateRifle">Update</button>
                        <button type="button" class="btn btn-danger m-1" @click="onDelRifle">Delete</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-body">
            <p class="m-0">
                {{ rifle.description }}
            </p>
        </div>
        <div class="border-top border-bottom">
            <div class="row row-cols-2 g-0">
                <div>
                    <ul class="list-group list-group-flush border-end">
                        <li class="list-group-item">
                            Дата создания: {{ rifle.created_at }}
                        </li>
                        <li class="list-group-item">
                            Патрон: {{ rifle.ammoName }}
                        </li>
                        <li class="list-group-item">
                            Страна происхождения: {{ rifle.countryName }}
                        </li>
                    </ul>
                </div>
                <div class="card-body">
                    Конструкторы:
                    <ul class="m-0">
                        <li v-for="constructor in rifle.constructorNames" :key="constructor">
                            {{ constructor }}
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="row row-cols-2 g-0">
            <div class="d-flex flex-column">
                <div class="card-body border-end">
                    <div>
                        Применено в конфликтах:
                        <ul class="m-0">
                            <li class="my-1 mx-3" v-for="conflict in rifle.conflictNames" :key="conflict">
                                {{ conflict }}
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="card-body border-top border-end flex-grow-1">
                    Типы креплений:
                    <ul class="m-0">
                        <li class="my-1 mx-3" v-for="mount in rifle.mountNames" :key="mount">
                            {{ mount }}
                        </li>
                    </ul>
                </div>
            </div>
            <div>
                <div class="card-body d-flex flex-column">
                    <span>Картинка:</span>
                    <img v-if="rifle.picture" :src="rifle.picture" :alt="rifle.title" class="img-fluid rounded mt-2 cp"
                        data-bs-toggle="modal" :data-bs-target="'#imageModal-' + rifle.id">
                </div>
            </div>
        </div>
    </div>
    <div class="modal" :id="'imageModal-' + rifle.id" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ rifle.title }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body text-center">
                    <img :src="rifle.picture" class="img-fluid lg rounded" :alt="rifle.title">
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