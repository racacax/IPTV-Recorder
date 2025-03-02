import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import VueLazyload from "vue-lazyload";
import Recordings from "./components/RecordingsPage.vue";
import Login from "./components/LoginPage.vue";
// Import our custom CSS
import "./scss/styles.scss";
// Import all of Bootstrap's JS
import * as bootstrap from "bootstrap";
/* eslint-disable */
if (bootstrap) {
} // force import of bootstrap, otherwise it is marked as unused

/* import the fontawesome core */
import { library } from "@fortawesome/fontawesome-svg-core";
import fas from "@fortawesome/fontawesome-free-solid";

/* import font awesome icon component */
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { createRouter, createWebHistory } from "vue-router";
import { API } from "./service/API";
// @ts-ignore
library.add(fas);
// @ts-ignore
API.API_ROOT = window.API_ROOT;
// @ts-ignore
API.CSRF_TOKEN = window.CSRF_TOKEN;
// @ts-ignore
export const gettext = window.gettext;
/* eslint-enable */
const routes = [
  { path: "/", component: Recordings },
  { path: "/recordings", component: Recordings },
  { path: "/login", component: Login },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App).component("font-awesome-icon", FontAwesomeIcon);
app.use(router);
app.use(VueLazyload);
app.mount("#app");
