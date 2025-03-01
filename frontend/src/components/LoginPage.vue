<script setup>
import { ref } from "vue";
import { API } from "../service/API.ts";
import { useRouter } from "vue-router";

const router = useRouter();
const username = ref();
const password = ref();
const loginBtn = ref();
function login() {
  loginBtn.value.disabled = "disabled";
  API.getToken(username.value.value, password.value.value)
    .then(() => {
      router.push({ path: "/" });
      return Promise.resolve();
    })
    .catch((e) => {
      alert(e);
      loginBtn.value.disabled = "";
    });
}
</script>

<template>
  <div class="d-flex justify-content-center align-items-center w-100">
    <form>
      <div class="mb-3">
        <label for="username" class="form-label">Nom d'utilisateur</label>
        <input id="username" ref="username" type="text" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Mot de passe</label>
        <input
          id="password"
          ref="password"
          type="password"
          class="form-control"
        />
      </div>
      <button
        ref="loginBtn"
        type="button"
        class="btn btn-primary"
        @click="login"
      >
        Se connecter
      </button>
    </form>
  </div>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
