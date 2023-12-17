<script setup lang="ts">
import { ref } from 'vue'
import {API} from "../service/API.ts";
import RecordingForm from "./recordings/RecordingForm.vue";
import RecordingItem from "./recordings/RecordingItem.vue";
import {FRecording, Recording} from "../service/entities.ts";
import {getStatus} from "../service/utils";

const recordings = ref([]);
const selectedRecording = ref({})
function setSelectedRecording(i) {
  selectedRecording.value = recordings.value[i]
}
let loading = true;
function loadRecordings(selectedRecording = -1) {
  API.getRecordings().then((r) => {
    recordings.value = r;
    loading = false;
    if(r.length > 0) {
      if(selectedRecording == -1) {
        setSelectedRecording(0);
      } else {
        r.forEach((e, i) => {
          if(e.id == selectedRecording) {
            setSelectedRecording(i);
            return;
          }
        })
      }
    }
  }).catch((e) => {
    alert(e)
    loading = false;
  })
}
loadRecordings();

const addRecordingBtn = ref();
function addRecording() {
  const recording : Partial<FRecording> = {name: "Nouvel enregistrement", id: Date.now(), action: "create"}
  recordings.value.push(recording)
  setSelectedRecording(recordings.value.length - 1)
}
const recordingsContainer = ref()
const w = window;
const search = ref("")
function setSearch(str: string) {
  search.value = str;
}

const passed = ref(true);
const running = ref(true);
const upcoming = ref(true);
function getFilteredRecordings() {
  return recordings.value.filter((e) => {
    if(e.name.toLowerCase().includes(search.value.toLowerCase())) {
      const type = getStatus(e);
      if(type == "passed" && !passed.value) {
        return false;
      } else if(type == "running" && !running.value) {
        return false;
      } else if(type == "upcoming" && !upcoming.value) {
        return false;
      }
      return true;
    }
    return false;
  })
}
</script>

<template>
  <div class="row gy-3">
    <div class="col-12 col-lg-6">
      <h2>Mes enregistrements
        <button type="button" ref="addRecordingBtn" class="btn btn-primary" @click="addRecording"><font-awesome-icon icon="fa-solid fa-plus" /> Ajouter</button>
      </h2>
      <div class="row mb-2">
        <div class="d-flex gap-2 col-lg-6 col-12">
          <label for="search-recording" class="form-label col-4 mt-2">Rechercher : </label>
          <input id="search-channel" class="form-control" @keyup="(e) => setSearch(e.target.value)" />
        </div>
        <div class="d-flex col-lg-6 col-12 gap-2 align-items-center">
          <div class="d-inline-flex gap-2"><input class="form-check-input passed" type="checkbox" :checked="passed" id="passed" @change="passed = !passed"/><label for="passed">Passés</label></div>
          <div class="d-inline-flex gap-2"><input class="form-check-input running" type="checkbox" :checked="running" id="running" @change="running = !running" /><label for="running">En cours</label></div>
          <div class="d-inline-flex gap-2"><input class="form-check-input upcoming" type="checkbox" :checked="upcoming" id="upcoming"  @change="upcoming = !upcoming"/><label for="upcoming">A venir</label></div>
        </div>
      </div>
      <div v-if="loading">
        Chargement en cours...
      </div>
      <div ref="recordingsContainer" class="overflow-y-scroll overflow-x-hidden" :style="['max-height:' + (w.innerHeight - (recordingsContainer ?? w).offsetTop - 10) + 'px']">
        <div class="row">
          <template v-for="(recording, index) in getFilteredRecordings()" :key="recording.id">
            <RecordingItem v-bind="recording" v-bind:is-active="recording.id === selectedRecording.id" @click="setSelectedRecording(index)" />
          </template>
        </div>
      </div>
    </div>
    <div class="col-12 col-lg-6">
      <RecordingForm v-if="Object.keys(selectedRecording).length > 0" v-bind="selectedRecording" v-bind:callback="loadRecordings" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.passed:checked {
  background-color: $passed;
  border-color: $passed;
}
.upcoming:checked {
  background-color: $upcoming;
  border-color: $upcoming;
}
.running:checked {
  background-color: $running;
  border-color: $running;
}
</style>
