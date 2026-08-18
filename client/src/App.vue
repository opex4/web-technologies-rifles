<script setup lang="ts">

</script>

<template>
    <div class="container">
        <nav class="nav nav-pills flex-column flex-sm-row mt-4">
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/"
            >Оружие</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/countries"
            >Страны</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/constructors"
            >Конструкторы</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/ammo"
            >Аммуниция</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/conflicts"
            >Конфликты</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/types_of_mounts"
            >Типы креплений</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/attachments"
            >Обвесы</router-link>
            <router-link 
                class="flex-sm-fill text-sm-center nav-link" 
                exact-active-class="active" 
                to="/loadouts"
            >Сборки</router-link>
            <li class="nav-item dropdown">
                <a 
                    class="nav-link dropdown-toggle" 
                    data-bs-toggle="dropdown" 
                    href="#" 
                    role="button" 
                    aria-expanded="false"
                >Пользователь</a>
                <ul class="dropdown-menu">
                    <li>
                        <a 
                            class="dropdown-item"
                            href="/admin"
                        >Админка</a>
                    </li>
                </ul>
            </li>
        </nav>
    </div>
    <div class="container">
        <router-view/>
    </div>
</template>

