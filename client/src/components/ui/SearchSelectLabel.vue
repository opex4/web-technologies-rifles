<script setup lang="ts">
import { ref, computed } from 'vue';

const props = defineProps<{
    items: string[];
    modelValue?: string | null;
}>();

const emit = defineEmits<{
    'update:modelValue': [value: string | null];
}>();

const searchQuery = ref('');
const isOpen = ref(false);
const inputRef = ref<HTMLInputElement | null>(null);
const uniqueItems = computed(() => Array.from(new Set(props.items)));

const filteredItems = computed(() => {
    if (!searchQuery.value) return uniqueItems.value;
    const query = searchQuery.value.toLowerCase();
    return uniqueItems.value.filter(item => item.toLowerCase().includes(query));
});

function selectItem(item: string | null) {
    searchQuery.value = '';
    isOpen.value = false;
    emit('update:modelValue', item);
    inputRef.value?.blur();
}
</script>

<template>
    <div class="badge bg-primary mb-2">
        Выбрано: {{ modelValue ? modelValue : '' }}
    </div>
    <div class="dropdown w-100" :class="{ show: isOpen }">
        <input 
            ref="inputRef" 
            type="text" 
            class="form-control" 
            placeholder="Поиск..." 
            v-model="searchQuery"
            @focus="isOpen = true" 
            @blur="isOpen = false" 
        />
        <ul class="dropdown-menu w-100" :class="{ show: isOpen }">
            <li>
                <a class="dropdown-item text-muted" href="#" @mousedown.prevent="selectItem(null)">
                    Очистить выбор
                </a>
            </li>
            <li v-for="item in filteredItems" :key="item">
                <a 
                    class="dropdown-item" 
                    href="#" 
                    @mousedown.prevent="selectItem(item)"
                    :class="{ active: modelValue === item }"
                >
                    {{ item }}
                </a>
            </li>
        </ul>
    </div>
</template>