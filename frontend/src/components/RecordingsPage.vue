<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { RecordingClient } from "../service/API.ts";
import RecordingForm from "./recordings/RecordingForm.vue";
import RecordingItem from "./recordings/RecordingItem.vue";
import { FRecording } from "../service/entities.ts";
import { getStatus } from "../service/utils";
import { gettext } from "../main";

const selectedRecording = ref({});
const additionalRecordings = ref([]);
function setSelectedRecording(i) {
  selectedRecording.value = allRecordings.value[i];
}
const { loading, data: recordings, error, fetchFn } = RecordingClient.list();

const allRecordings = computed(() => [
  ...(recordings.value ?? []),
  ...additionalRecordings.value,
]);
const reloadRecordings = (id: number) => {
  selectedRecording.value = { id: id };
  fetchFn();
  additionalRecordings.value = [];
};
watch(recordings, () => {
  let found = false;
  if (allRecordings.value && allRecordings.value.length > 0) {
    if (!selectedRecording.value) {
      setSelectedRecording(0);
    } else {
      allRecordings.value.forEach((e, i) => {
        if (e.id == selectedRecording.value.id) {
          setSelectedRecording(i);
          found = true;
          return;
        }
      });
      if (!found) {
        setSelectedRecording(0);
      }
    }
  }
});

watch(error, () => {
  if (error) {
    alert(error.value);
  }
});

const addRecordingBtn = ref();
function addRecording() {
  const recording: Partial<FRecording> = {
    name: gettext("Nouvel enregistrement"),
    id: Date.now(),
    action: "create",
  };
  additionalRecordings.value.push(recording);
  setSelectedRecording(allRecordings.value.length - 1);
}
const recordingsContainer = ref();
const w = window;
const search = ref("");
function setSearch(str: string) {
  search.value = str;
}

const passed = ref(true);
const running = ref(true);
const upcoming = ref(true);
function getFilteredRecordings() {
  return (allRecordings.value ?? []).filter((e) => {
    if (e.name.toLowerCase().includes(search.value.toLowerCase())) {
      const type = getStatus(e);
      if (type == "passed" && !passed.value) {
        return false;
      } else if (type == "running" && !running.value) {
        return false;
      } else if (type == "upcoming" && !upcoming.value) {
        return false;
      }
      return true;
    }
    return false;
  });
}
</script>

<template>
  <div class="row gy-3">
    <div class="col-12 col-lg-6">
      <h2>
        {{ gettext("Mes enregistrements") }}
        <button
          ref="addRecordingBtn"
          type="button"
          class="btn btn-primary"
          @click="addRecording"
        >
          <font-awesome-icon icon="fa-solid fa-plus" /> {{ gettext("Ajouter") }}
        </button>
      </h2>
      <div class="row mb-2">
        <div class="d-flex gap-2 col-lg-6 col-12">
          <label for="search-recording" class="form-label col-4 mt-2"
            >{{ gettext("Rechercher :") }}
          </label>
          <input
            id="search-channel"
            class="form-control"
            @keyup="(e) => setSearch(e.target.value)"
          />
        </div>
        <div class="d-flex col-lg-6 col-12 gap-2 align-items-center">
          <div class="d-inline-flex gap-2">
            <input
              id="passed"
              class="form-check-input passed"
              type="checkbox"
              :checked="passed"
              @change="passed = !passed"
            /><label for="passed">{{ gettext("Passés") }}</label>
          </div>
          <div class="d-inline-flex gap-2">
            <input
              id="running"
              class="form-check-input running"
              type="checkbox"
              :checked="running"
              @change="running = !running"
            /><label for="running">{{ gettext("En cours") }}</label>
          </div>
          <div class="d-inline-flex gap-2">
            <input
              id="upcoming"
              class="form-check-input upcoming"
              type="checkbox"
              :checked="upcoming"
              @change="upcoming = !upcoming"
            /><label for="upcoming">{{ gettext("A venir") }}</label>
          </div>
        </div>
      </div>
      <div v-if="loading">{{ gettext("Chargement en cours...") }}</div>
      <div
        ref="recordingsContainer"
        class="overflow-y-scroll overflow-x-hidden"
        :style="[
          'max-height:' +
            (w.innerHeight - (recordingsContainer ?? w).offsetTop - 10) +
            'px',
        ]"
      >
        <div class="row">
          <template
            v-for="(recording, index) in getFilteredRecordings()"
            :key="recording.id"
          >
            <RecordingItem
              v-bind="recording"
              :is-active="recording.id === selectedRecording.id"
              @click="setSelectedRecording(index)"
            />
          </template>
        </div>
      </div>
    </div>
    <div class="col-12 col-lg-6">
      <RecordingForm
        v-if="Object.keys(selectedRecording).length > 0 && selectedRecording.id"
        :key="`${selectedRecording.id}-${loading}`"
        v-bind="selectedRecording"
        :callback="reloadRecordings"
      />
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
