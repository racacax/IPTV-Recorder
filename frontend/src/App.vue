<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">IPTV Recorder</a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div
        v-if="router.currentRoute.value.fullPath !== '/login'"
        id="navbarSupportedContent"
        class="collapse navbar-collapse"
      >
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/recordings">{{
              gettext("Mes enregistrements")
            }}</router-link>
          </li>
          <li class="nav-item">
            <a
              class="nav-link"
              target="_blank"
              :href="API.API_ROOT + 'admin'"
              >{{ gettext("Admin") }}</a
            >
          </li>
        </ul>
        <div class="d-flex">
          <button class="btn btn-outline-success" type="button" @click="logout">
            <font-awesome-icon :icon="['fas', 'unlock']" />
            {{ gettext("Se déconnecter") }}
          </button>
        </div>
      </div>
    </div>
  </nav>
  <div class="w-100 p-2">
    <router-view />
  </div>
</template>
<script setup>
import { API, CheckClient } from "./service/API.ts";
import { useRouter } from "vue-router";
import { gettext } from "./main.ts";
import { watch } from "vue";
const router = useRouter();
const { error } = CheckClient.list();
watch(error, () => {
  if (error) {
    router.push({ path: "/login" });
  }
});

function logout() {
  localStorage.removeItem("iptvRecorderToken");
  router.push({ path: "/login" });
}
</script>
