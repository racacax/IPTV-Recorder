import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import Home from './components/Home.vue'
import VueLazyload from 'vue-lazyload'
import Recordings from './components/Recordings.vue'
import Playlists from './components/Playlists.vue'
import Login from './components/Login.vue'
// Import our custom CSS
import './scss/styles.scss'
// Import all of Bootstrap's JS
import * as bootstrap from 'bootstrap'
if(bootstrap){} // force import of bootstrap, otherwise it is marked as unused

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'
import fas from '@fortawesome/fontawesome-free-solid';

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {createRouter, createWebHistory} from "vue-router";
import {API} from "./service/API";
library.add(fas)
API.API_ROOT = window.API_ROOT
API.CSRF_TOKEN = window.CSRF_TOKEN
const routes = [
    { path: '/', component: Recordings },
    { path: '/recordings', component: Recordings },
    { path: '/login', component: Login },
    { path: '/playlists', component: Playlists },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

const app = createApp(App).component('font-awesome-icon', FontAwesomeIcon)
app.use(router)
//@ts-ignore
app.use(VueLazyload)
app.mount('#app')
