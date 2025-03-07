<script setup lang="ts">
import { computed, ref, watch } from "vue";
import {
  RecordingClient,
  RecordingMethodClient,
  VideoSourceClient,
  VideoSourcesClient,
} from "../../service/API";
import ChannelChoose from "./ChannelChoose.vue";
import { FVideoSource, M3UEntity } from "../../service/entities";
import { gettext } from "../../main.ts";

const submitBtn = ref();
const isDisplayingModal = ref(false);
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
  callback: Function,
});
const id = ref(props.id);
const deleteVideoSource = (id: number) => {
  const { fetchFn: deleteFn } = VideoSourceClient.delete(() => id, {
    lazy: true,
  });
  return deleteFn();
};
const addVideoSource = (body: Record<string, unknown>) => {
  const { fetchFn: postFn } = VideoSourcesClient.post({ lazy: true });
  return postFn(body);
};
const updateVideoSource = (id: number, body: Record<string, unknown>) => {
  const { fetchFn: putFn } = VideoSourceClient.put(() => id, { lazy: true });
  return putFn(body);
};

const deleteRecording = (id: number) => {
  const { fetchFn: deleteFn } = RecordingClient.delete(() => id, {
    lazy: true,
  });
  return deleteFn();
};
const addRecording = (body: Record<string, unknown>) => {
  const { fetchFn: postFn } = RecordingClient.post({ lazy: true });
  return postFn(body);
};
const updateRecording = (id: number, body: Record<string, unknown>) => {
  const { fetchFn: putFn } = RecordingClient.put(() => id, { lazy: true });
  return putFn(body);
};

const {
  data: sources,
  loading,
  error,
} = VideoSourcesClient.get(() => props.id);
const {
  data: recordingMethods,
  loading: recordingMethodsLoading,
  error: recordingMethodsError,
} = RecordingMethodClient.list();

const allSources = ref([]);
watch(sources, () => {
  allSources.value = [...(sources.value ?? [])];
});
watch([error, recordingMethodsError], () => {
  if (error || recordingMethodsError) {
    alert((error ?? recordingMethodsError).value);
  }
});
watch(
  () => props.id,
  () => {
    id.value = props.id;
    setName(props.name);
    setStartTime(formatDate(props.start_time));
    setEndTime(formatDate(props.end_time));
    setGapBetweenRetries(props.gap_between_retries ?? 5);
    setUseBackupAfter(props.use_backup_after ?? 5);
  },
);
function formatDate(date: Date | undefined) {
  if (date !== undefined) {
    const dt = date;
    const padL = (nr, len = 2, chr = `0`) => `${nr}`.padStart(len, chr);

    return `${dt.getFullYear()}-${padL(dt.getMonth() + 1)}-${padL(
      dt.getDate(),
    )} ${padL(dt.getHours())}:${padL(dt.getMinutes())}`;
  }
}

function addSource(source: M3UEntity = null) {
  if (source !== null) {
    allSources.value.push({
      id: Date.now(),
      url: source.url,
      name: source.name,
      logo: source.logo,
      recording_method_id: recordingMethods.value[0].id,
      action: "create",
      index: allSources.value.length,
    });
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
const minMaxTime = computed(() => {
  if (new Date(startTime.value).getTime() > new Date().getTime()) {
    return startTime;
  } else {
    return formatDate(new Date());
  }
});

function addOrEditOrDeleteSource(source: Partial<FVideoSource>) {
  if (source.action === "delete") {
    return deleteVideoSource(source.id);
  } else if (source.action === "create") {
    return addVideoSource({
      url: source.url,
      name: source.name,
      logo: source.logo,
      recording_method_id: source.recording_method_id,
      index: source.index,
      recording_id: id.value,
    });
  } else {
    return updateVideoSource(source.id, {
      url: source.url,
      name: source.name,
      logo: source.logo,
      recording_method_id: source.recording_method_id,
      index: source.index,
      recording_id: id.value,
    });
  }
}
function addOrEditRecording() {
  submitBtn.value.disabled = "disabled";
  if (allSources.value.filter((e) => e.action !== "delete").length === 0) {
    alert(gettext("Vous devez au minimum ajouter une source"));
    submitBtn.value.disabled = "";
  } else {
    let promise = null;
    if (props.action == "create") {
      promise = addRecording({
        name: name.value,
        start_time: new Date(startTime.value),
        end_time: new Date(endTime.value),
        gap_between_retries: gapBetweenRetries.value,
        use_backup_after: useBackupAfter.value,
      }).then((j) => {
        id.value = j.id;
      });
    } else {
      promise = updateRecording(props.id, {
        id: props.id,
        name: name.value,
        start_time: new Date(startTime.value),
        end_time: new Date(endTime.value),
        gap_between_retries: gapBetweenRetries.value,
        use_backup_after: useBackupAfter.value,
      });
    }
    promise
      .then(() => {
        const promises = [];
        allSources.value.forEach((e) =>
          promises.push(addOrEditOrDeleteSource(e)),
        );
        Promise.all(promises)
          .then(() => {
            props.callback(id.value);
            alert(gettext("Sauvegardé avec succès"));
            submitBtn.value.disabled = "";
          })
          .catch((e) => alert(e));
      })
      .catch((e) => {
        alert(e);
      });
  }
}
function deleteRecordingFn() {
  if (
    confirm(
      gettext(
        "Êtes-vous sûr de vouloir supprimer cet enregistrement (fichiers video inclus) ?",
      ),
    )
  ) {
    deleteRecording(props.id)
      .then(() => {
        props.callback();
      })
      .catch((e) => alert(e));
  }
}

function stopRecording() {
  if (confirm(gettext("Êtes-vous sûr de vouloir stopper l'enregistrement ?"))) {
    endTime.value = formatDate(new Date());
    addOrEditRecording();
  }
}
</script>
<template>
  <template v-if="loading || recordingMethodsLoading">
    <span>Chargement en cours...</span>
  </template>
  <template v-if="!loading && !recordingMethodsLoading">
    <button
      v-if="props.action !== 'create' && props.is_running"
      class="btn btn-warning float-end"
      type="button"
      @click="stopRecording"
    >
      <font-awesome-icon icon="fa-solid fa-stop" />
      {{ gettext("Stopper l'enregistrement") }}
    </button>
    <h2 v-if="props.action === 'create'">
      {{ gettext("Ajouter un enregistrement") }}
    </h2>
    <h2 v-else>{{ gettext("Modifier un enregistrement") }}</h2>
    <form @submit.prevent="addOrEditRecording">
      <div class="mb-3">
        <label for="recording-name" class="form-label">{{
          gettext("Nom de l'enregistrement")
        }}</label>
        <input
          id="recording-name"
          type="text"
          class="form-control"
          :value="name"
          @change="(e) => setName(e.target.value)"
        />
      </div>
      <div class="mb-3 row">
        <div class="col-6">
          <label for="start-time" class="form-label">{{
            gettext("Date et heure de début")
          }}</label>
          <input
            id="start-time"
            required
            type="datetime-local"
            class="form-control"
            :value="startTime"
            :max="endTime"
            @change="(e) => setStartTime(e.target.value)"
          />
        </div>
        <div class="col-6">
          <label for="end-time" class="form-label">{{
            gettext("Date et heure de fin")
          }}</label>
          <input
            id="end-time"
            required
            type="datetime-local"
            class="form-control"
            :min="minMaxTime"
            :value="endTime"
            @change="(e) => setEndTime(e.target.value)"
          />
        </div>
        <div class="col-6">
          <label for="gap-between-retries" class="form-label">{{
            gettext("Intervalle en secondes entre chaque essai")
          }}</label>
          <input
            id="gap-between-retries"
            required
            type="number"
            class="form-control"
            :value="gapBetweenRetries"
            @change="(e) => setGapBetweenRetries(e.target.value)"
          />
        </div>
        <div class="col-6">
          <label for="use-backup-after" class="form-label">{{
            gettext("Nombre d'échecs avant changement")
          }}</label>
          <input
            id="use-backup-after"
            required
            type="number"
            class="form-control"
            :value="useBackupAfter"
            @change="(e) => setUseBackupAfter(e.target.value)"
          />
        </div>
      </div>
      <div class="mb-3">
        <div class="d-flex justify-content-between">
          <label for="recording-name" class="form-label"
            >{{ gettext("Sources") }} ({{
              allSources.filter((e) => e.action !== "delete").length
            }})</label
          >
          <button type="button" class="btn btn-primary" @click="displayModal()">
            <font-awesome-icon icon="fa-solid fa-plus" />
            {{ gettext("Ajouter") }}
          </button>
        </div>
        <span
          v-if="allSources.filter((e) => e.action !== 'delete').length === 0"
          >{{ gettext("Aucune source vidéo") }}</span
        >
        <div class="row sources-container">
          <template v-for="(source, index) in allSources">
            <div v-if="source.action !== 'delete'" class="col-12 col-xl-6 mt-1">
              <div class="card">
                <div class="card-body">
                  <button
                    type="button"
                    class="btn btn-danger float-end ms-2"
                    @click="
                      () => {
                        if (source.action !== 'create') {
                          source.action = 'delete';
                        } else {
                          allSources.splice(index, 1);
                        }
                      }
                    "
                  >
                    <font-awesome-icon icon="fa-solid fa-trash" />
                  </button>
                  <div class="source-grid">
                    <div
                      class="d-flex justify-content-center align-items-center logo-container"
                    >
                      <img :src="source.logo" class="channel-logo" />
                    </div>
                    <div>
                      <span>{{ gettext("Nom :") }} {{ source.name }}</span
                      ><br />
                      <div class="d-flex gap-2 align-items-center">
                        <span class="text-nowrap"
                          >{{ gettext("Méthode :") }}
                        </span>
                        <select
                          class="form-select"
                          :value="source.recording_method_id"
                          @change="
                            (e) =>
                              (source.recording_method_id = parseInt(
                                e.target.value,
                              ))
                          "
                        >
                          <option
                            v-for="recordingMethod in recordingMethods"
                            v-if="recordingMethods"
                            :value="recordingMethod.id"
                          >
                            {{ recordingMethod.name }}
                          </option>
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
        <button ref="submitBtn" type="submit" class="btn btn-primary">
          {{ gettext("Sauvegarder l'enregistrement") }}
        </button>
        <button
          v-if="props.action !== 'create' && !props.is_running"
          type="button"
          class="btn btn-danger"
          @click="deleteRecordingFn"
        >
          {{ gettext("Supprimer l'enregistrement") }}
        </button>
      </div>
    </form>
    <ChannelChoose
      v-if="isDisplayingModal"
      :id="props.id"
      :callback="addSource"
    />
  </template>
</template>
<style scoped>
.sources-container {
  max-height: 350px;
  overflow-y: scroll;
  overflow-x: hidden;
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
