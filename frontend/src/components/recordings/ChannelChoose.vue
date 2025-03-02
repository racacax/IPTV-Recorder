<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { PlaylistClient, PlaylistM3UClient } from "../../service/API";
import { gettext } from "../../main";

const props = defineProps({
  id: Number,
  callback: Function,
});
const btnModal = ref();
const btnClose = ref();
const playlistSelect = ref();
const searchInput = ref("");
const selectedId = ref();

const {
  data: playlists,
  loading,
  error,
  fetchFn,
} = PlaylistClient.list({ lazy: true });
const {
  data: channels,
  loading: channelsLoading,
  error: channelsError,
  fetchFn: channelsFetchFn,
} = PlaylistM3UClient.get(() => selectedId.value, { lazy: true });
watch(btnModal, () => {
  btnModal.value.click();
  fetchFn();
});
watch(playlists, () => {
  if (playlists.value.length > 0) {
    selectedId.value = playlists.value[0].id;
  } else {
    alert(gettext("Veuillez ajouter au minimum une playlist !"));
  }
});
watch([error, channelsError], () => {
  if (error || channelsError) {
    alert((error ?? channelsError).value);
  }
});
watch(selectedId, () => {
  if (selectedId.value) {
    channelsFetchFn();
  }
});
const filteredChannels = computed(() =>
  (channels.value ?? []).filter((e) => {
    return e.name.toLowerCase().includes(searchInput.value.toLowerCase());
  }),
);

const modal = ref();
setInterval(() => {
  if (modal.value === null) {
    return;
  }
  if (!modal.value.classList.contains("show")) {
    btnModal.value.click();
  }
}, 100);
</script>

<template>
  <!-- Button trigger modal -->
  <button
    ref="btnModal"
    type="button"
    class="btn btn-primary"
    data-bs-toggle="modal"
    :data-bs-target="'#modal' + props.id"
    style="display: none"
  >
    Launch modal
  </button>

  <!-- Modal -->
  <div
    :id="'modal' + props.id"
    ref="modal"
    class="modal fade"
    tabindex="-1"
    :aria-labelledby="'#modalLabel' + props.id"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 :id="'modalLabel' + props.id" class="modal-title fs-5">
            {{ gettext("Sélectionnez une chaine") }}
          </h1>
          <button
            ref="btnClose"
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
            @click="callback()"
          ></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <label for="playlist" class="form-label col-4">{{
              gettext("Playlist")
            }}</label>
            <div class="col-8">
              <select
                id="playlist"
                ref="playlistSelect"
                class="form-select"
                @change="(e) => (selectedId = e.target.value)"
              >
                <option
                  v-for="playlist in playlists"
                  :key="playlist.id"
                  :value="playlist.id"
                >
                  {{ playlist.name }}
                </option>
              </select>
            </div>
            <label for="search-channel" class="form-label col-4 mt-2">{{
              gettext("Rechercher")
            }}</label>
            <div class="col-8 mt-2">
              <input
                id="search-channel"
                class="form-control"
                @keyup="(e) => (searchInput = e.target.value)"
              />
            </div>
          </div>
          <span v-if="loading ?? channelsLoading">{{
            gettext("Chargement en cours...")
          }}</span>
          <div v-if="!loading" class="row">
            <div
              class="list-group channels mt-2 p-2"
              style="max-height: 500px; overflow-y: scroll"
            >
              <a
                v-for="channel in filteredChannels"
                :key="channel.url"
                href="#"
                class="list-group-item list-group-item-action"
                @click="
                  () => {
                    btnClose.click();
                    callback(channel);
                  }
                "
              >
                <div class="d-flex align-items-center">
                  <div
                    class="d-flex justify-content-center align-items-center logo-container me-3"
                  >
                    <img
                      v-lazy="channel.logo"
                      class="logo"
                      alt="Logo"
                      loading="lazy"
                    />
                  </div>
                  <div>
                    <span>{{ channel.name }}</span>
                  </div>
                </div>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.logo-container {
  width: 80px;
  height: 80px;
}
.logo {
  max-width: 100%;
  max-height: 80px;
}
</style>
