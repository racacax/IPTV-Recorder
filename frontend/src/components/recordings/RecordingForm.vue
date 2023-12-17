<script setup lang="ts">

import {ref, watch} from "vue";
import {API} from "../../service/API";
import ChannelChoose from "./ChannelChoose.vue";
import {FVideoSource, M3UEntity, VideoSource} from "../../service/entities";

let submitBtn = ref();
let loading = ref(true);
let sources = ref([]);
let isDisplayingModal = ref(false);
function displayModal() {
  isDisplayingModal.value = true;
}

const props = defineProps({
  id: Number,
  start_time: Date,
  end_time: Date,
  is_running: Boolean,
  name: String,
  action: String,
  gap_between_retries: Number,
  use_backup_after: Number,
  callback: Function
})
const id = ref(props.id)
function loadSources() {
  loading.value = true;
  if(props.id !== undefined) {
    API.getVideoSourcesFromRecording(props.id).then((j) => {
      sources.value = j;
      loading.value = false;
    }).catch((e) => {
      alert(e)
      loading.value = false;
    })
  } else {
    loading.value = false;
  }
}
watch(() => props.id, () => {
  loadSources();
  id.value = props.id
  setName(props.name);
  setStartTime(formatDate(props.start_time));
  setEndTime(formatDate(props.end_time));
  setGapBetweenRetries(props.gap_between_retries ?? 5);
  setUseBackupAfter(props.use_backup_after ?? 5)
})
loadSources();
function formatDate(date: Date|undefined) {
  if(date !== undefined) {
    const dt = date;
    const padL = (nr, len = 2, chr = `0`) => `${nr}`.padStart(2, chr);

    return(`${dt.getFullYear()}-${padL(dt.getMonth()+1)}-${
        padL(dt.getDate())} ${
        padL(dt.getHours())}:${
        padL(dt.getMinutes())}`
    );
  }
}



function addSource(source: M3UEntity = null) {
  if(source !== null) {
    sources.value.push({
      id: Date.now(),
      url:              source.url,
      name:             source.name,
      logo:             source.logo,
      recording_method: "ffmpeg",
      action: "create",
      index: sources.value.length
    })
  }
  isDisplayingModal.value = false;
}

const name = ref(props.name);
function setName(e) {
  name.value = e;
}
const startTime = ref(formatDate(props.start_time));
function setStartTime(e) {
  startTime.value = e;
}
const endTime = ref(formatDate(props.end_time));
function setEndTime(e) {
  endTime.value = e;
}
const gapBetweenRetries = ref(props.gap_between_retries ?? 5);
function setGapBetweenRetries(e) {
  gapBetweenRetries.value = e;
}
const useBackupAfter = ref(props.use_backup_after ?? 5);
function setUseBackupAfter(e) {
  useBackupAfter.value = e;
}

function addOrEditOrDeleteSource(source: Partial<FVideoSource>) {
  if (source.action === "delete") {
    return API.deleteVideoSource(source.id)
  } else if (source.action === "create") {
    return API.createVideoSource(id.value, {
      url: source.url,
      name: source.name,
      logo: source.logo,
      recording_method: source.recording_method,
      index: source.index
    })
  } else {
    return API.updateVideoSource(source.id, {
      url: source.url,
      name: source.name,
      logo: source.logo,
      recording_method: source.recording_method,
      index: source.index
    })
  }
}
function addOrEditRecording() {
  submitBtn.value.disabled = "disabled"
  if(sources.value.filter((e) => e.action !== 'delete').length === 0) {
    alert("Vous devez au minimum ajouter une source")
    submitBtn.value.disabled = ""
  } else {
    let promise = null
    if(props.action == "create") {
      promise = API.createRecording({
        name: name.value,
        start_time : new Date(startTime.value),
        end_time: new Date(endTime.value),
        gap_between_retries: gapBetweenRetries.value,
        use_backup_after: useBackupAfter.value,
        writing_directory: "/home/clement/yoyo/"
      }).then((j: {created: boolean, id: number}) => {
        id.value = j.id;
      })
    } else {
      promise = API.updateRecording(props.id, {
        id: props.id,
        name: name.value,
        start_time : new Date(startTime.value),
        end_time: new Date(endTime.value),
        gap_between_retries: gapBetweenRetries.value,
        use_backup_after: useBackupAfter.value,
        writing_directory: "/home/clement/yoyo/"
      })
    }
    promise.then((j) => {
      let promises = []
      sources.value.forEach((e) => promises.push(addOrEditOrDeleteSource(e)))
      Promise.all(promises).then(() => {
        props.callback(id.value);
        alert("Sauvegardé avec succès")
        submitBtn.value.disabled = "";
      }).catch((e) => alert(e))
    }).catch((e) => {
      alert(e)
    })
  }
}
function deleteRecording() {
  if(confirm("Êtes-vous sûr de vouloir supprimer cet enregistrement (fichiers video inclus) ?")) {
    API.deleteRecording(props.id).then(() => {
      props.callback();
    }).catch(
        (e) => alert(e)
    )

  }
}

function stopRecording() {
  if(confirm("Êtes-vous sûr de vouloir stopper l'enregistrement ?")) {
    endTime.value = formatDate(new Date());
    addOrEditRecording();
  }
}
</script>
<template>
  <template v-if="loading">
    <span>Chargement en cours...</span>
  </template>
  <template v-if="!loading">
    <button v-if="props.action !== 'create' && props.is_running" class="btn btn-warning float-end" @click="stopRecording" type="button"><font-awesome-icon icon="fa-solid fa-stop" /> Stopper l'enregistrement</button>
    <h2 v-if="props.action === 'create'">Ajouter un enregistrement</h2>
    <h2 v-else>Modifier un enregistrement</h2>
    <form @submit.prevent="addOrEditRecording">
      <div class="mb-3">
        <label for="recording-name" class="form-label">Nom de l'enregistrement</label>
        <input type="text" class="form-control" id="recording-name" :value="name" @change="(e) => setName(e.target.value)">
      </div>
      <div class="mb-3 row">
        <div class="col-6">
          <label for="start-time" class="form-label">Date et heure de début</label>
          <input required type="datetime-local" class="form-control" id="start-time" :value="startTime" @change="(e) => setStartTime(e.target.value)">
        </div>
        <div class="col-6">
          <label for="end-time" class="form-label">Date et heure de fin</label>
          <input required type="datetime-local" class="form-control" id="end-time" :value="endTime" @change="(e) => setEndTime(e.target.value)">
        </div>
        <div class="col-6">
          <label for="gap-between-retries" class="form-label">Intervalle en secondes entre chaque essai</label>
          <input required type="number" class="form-control" id="gap-between-retries" :value="gapBetweenRetries" @change="(e) => setGapBetweenRetries(e.target.value)">
        </div>
        <div class="col-6">
          <label for="use-backup-after" class="form-label">Nombre d'échecs avant changement</label>
          <input required type="number" class="form-control" id="use-backup-after" :value="useBackupAfter" @change="(e) => setUseBackupAfter(e.target.value)">
        </div>
      </div>
      <div class="mb-3">
        <div class="d-flex justify-content-between">
          <label for="recording-name" class="form-label">Sources ({{ sources.filter((e) => e.action !== 'delete').length }})</label>
          <button type="button" class="btn btn-primary" @click="displayModal()"><font-awesome-icon icon="fa-solid fa-plus" /> Ajouter</button>
        </div>
        <span v-if="sources.filter((e) => e.action !== 'delete').length === 0">Aucune source vidéo</span>
        <div class="row sources-container">
          <template v-for="(source, index) in sources">
            <div v-if="source.action !== 'delete'" class="col-12 col-xl-6 mt-1">
              <div class="card">
                <div class="card-body">
                  <button type="button" class="btn btn-danger float-end ms-2" @click="() => {
                  if(source.action !== 'create') { source.action = 'delete' } else { sources.splice(index, 1) }
                }"><font-awesome-icon icon="fa-solid fa-trash" /></button>
                  <div class="source-grid">
                    <div class="d-flex justify-content-center align-items-center logo-container">
                      <img :src="source.logo" class="channel-logo"/>
                    </div>
                    <div>
                      <span>Nom : {{ source.name }}</span><br/>
                      <div class="d-flex gap-2 align-items-center">
                        <span>Méthode: </span>
                        <select class="form-select" :value="source.recording_method" @change="(e) => source.recording_method = e.target.value">
                          <option value="ffmpeg">ffmpeg</option>
                          <option value="wget">wget</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>
          </div>
        </div>

      <div class="mb-3 d-flex gap-2">
        <button type="submit" ref="submitBtn" class="btn btn-primary">Sauvegarder l'enregistrement</button>
        <button type="button" v-if="props.action !== 'create' && !props.is_running" class="btn btn-danger" @click="deleteRecording">Supprimer l'enregistrement</button>
      </div>
    </form>
    <ChannelChoose v-if="isDisplayingModal" v-bind:id="props.id" v-bind:callback="addSource" />
  </template>
</template>
<style scoped>
.sources-container {
  max-height: 350px;
  overflow: scroll;
}
  .channel-logo {
    max-width: 80px;
    max-height: 80px;
  }
  .source-grid {
    display: grid;
    grid-template-columns: 80px auto;
    grid-gap: 10px;
  }
  .logo-container {
    height: 80px;
  }
</style>
