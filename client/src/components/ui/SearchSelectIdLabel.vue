<script setup lang="ts">
import { ref, computed } from 'vue';

export interface SelectItem {
    id: number;
    label: string;
}

const props = defineProps<{
    items: SelectItem[];
    modelValue?: number | null;
}>();

const emit = defineEmits<{
    'update:modelValue': [value: number | null];
}>();

const searchQuery = ref('');
const isOpen = ref(false);
const inputRef = ref<HTMLInputElement | null>(null);

const selectedLabel = computed(() => {
    if (props.modelValue === null || props.modelValue === undefined) return '';
    const item = props.items.find(i => i.id === props.modelValue);
    return item ? item.label : '';
});

const filteredItems = computed(() => {
    if (!searchQuery.value) return props.items;
    const query = searchQuery.value.toLowerCase();
    return props.items.filter(item => item.label.toLowerCase().includes(query));
});

function selectItem(item: SelectItem | null) {
    searchQuery.value = '';
    isOpen.value = false;
    if (item === null){
        emit('update:modelValue', null);
    } else {
        emit('update:modelValue', item.id);
    }
    inputRef.value?.blur();
}
</script>

<template>
    <div class="badge bg-primary mb-2">
            Выбрано: {{ selectedLabel ? selectedLabel : '' }}
    </div>
    <div class="dropdown w-100" :class="{ show: isOpen }">
        <input ref="inputRef" type="text" class="form-control" placeholder="Поиск..." v-model="searchQuery"
            @focus="isOpen = true" @blur="isOpen = false" />
        <ul class="dropdown-menu w-100" :class="{ show: isOpen }">
            <li>
                <a class="dropdown-item text-muted" href="#" @mousedown.prevent="selectItem(null)">
                    Очистить выбор
                </a>
            </li>
            <li v-for="item in filteredItems" :key="item.id">
                <a class="dropdown-item" href="#" @mousedown.prevent="selectItem(item)"
                    :class="{ active: modelValue === item.id }">
                    {{ item.label }}
                </a>
            </li>
        </ul>
    </div>
</template>