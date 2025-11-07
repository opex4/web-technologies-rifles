<script setup lang="ts">
import type {Rifle} from "@/types/Rifle.ts";
import type {AmmoType} from "@/types/AmmoType.ts";
import type {Country} from "@/types/Country.ts";
import type {Constructor} from "@/types/Constructor.ts";
import type {ArmedConflict} from "@/types/ArmedConflict.ts";


defineProps<{
    rifle: Rifle,
    ammoTypes: AmmoType[],
    countries: Country[],
    constructors: Constructor[],
    armedConflicts: ArmedConflict[]
}>();
</script>

<template>
    <div class="card border-light">
        <div class="card-header border-light">
            <h2 class="m-0">
                {{ rifle.title }}
            </h2>
        </div>
        <div class="card-body">
            <p class="m-0">
                {{ rifle.description }}
            </p>
        </div>
        <div class="border-top border-bottom">
            <div class="row row-cols-2">
                <div>
                    <ul class="list-group list-group-flush border-end">
                        <li class="list-group-item">
                            Дата создания: {{ rifle.created_at }}
                        </li>
                        <li class="list-group-item">
                            Патрон: {{ ammoTypes[rifle.ammo_type - 1].title }}
                        </li>
                        <li class="list-group-item">
                            Страна происхождения: {{ countries[rifle.country_of_origin - 1].name }}
                        </li>
                    </ul>
                </div>
                <div class="p-2">
                    Конструкторы:
                    <ul>
                        <li v-for="constructor_id in rifle.constructors">
                            {{ constructors[constructor_id - 1].name }}
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="card-body">
            Применено в конфликтах:
            <ul class="d-flex m-0">
                <li class="my-1 mx-3" v-for="conflict_id in rifle.used_in_conflicts">
                    {{ armedConflicts[conflict_id - 1].title }}
                </li>
            </ul>
        </div>
    </div>
</template>