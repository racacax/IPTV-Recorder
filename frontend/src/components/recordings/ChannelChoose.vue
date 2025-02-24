<script setup lang="ts">

import {computed, ref, watch} from "vue";
import {PlaylistClient, PlaylistM3UClient} from "../../service/API";

const props = defineProps({
  id: Number,
  callback: Function
})
const btnModal = ref()
const btnClose = ref()
const playlistSelect = ref()
const searchInput = ref('')
const selectedId = ref()

const {data: playlists, loading, error, fetchFn} = PlaylistClient.list({lazy: true})
const {data: channels, loading: channelsLoading, error: channelsError, fetchFn: channelsFetchFn} = PlaylistM3UClient.get(() => selectedId.value, {lazy: true})
watch(btnModal, () => {
  btnModal.value.click()
  fetchFn()
})
watch(playlists, () => {
  if(playlists.value.length > 0){
    selectedId.value = playlists.value[0].id
  } else {
    alert("Veuillez ajouter au minimum une playlist !")
  }
})
watch([error, channelsError], () => {
  if(error || channelsError){
    alert((error ?? channelsError).value)
  }
})
watch(selectedId, () => {
  if(selectedId){
    channelsFetchFn()
  }
})
const filteredChannels = computed(() => (channels.value ?? []).filter((e) => {
  return e.name.toLowerCase().includes(searchInput.value.toLowerCase())
}))

const modal = ref()
setInterval(() => {
  if(modal.value === null) {
    return
  }
  if(!modal.value.classList.contains("show")) {
    btnModal.value.click()
  }
}, 100)
</script>

<template><!-- Button trigger modal -->
  <button type="button" class="btn btn-primary" data-bs-toggle="modal" ref="btnModal" :data-bs-target="'#modal' + props.id" style="display:none">
    Launch modal
  </button>

  <!-- Modal -->
  <div class="modal fade" ref="modal" :id="'modal' + props.id" tabindex="-1" :aria-labelledby="'#modalLabel' + props.id" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" :id="'modalLabel' + props.id">Sélectionnez une chaine</h1>
          <button type="button" ref="btnClose" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="callback();"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <label for="playlist" class="form-label col-4">Playlist</label>
            <div class="col-8">
              <select id="playlist" class="form-select" ref="playlistSelect" @change="(e) => selectedId = e.target.value">
                <option :value="playlist.id" v-for="playlist in playlists">{{ playlist.name }}</option>
              </select>
            </div>
            <label for="search-channel" class="form-label col-4 mt-2">Rechercher</label>
            <div class="col-8 mt-2">
              <input id="search-channel" class="form-control" @keyup="(e) => searchInput = e.target.value" />
            </div>
          </div>
          <span v-if="loading ?? channelsLoading">Chargement en cours...</span>
          <div class="row" v-if="!loading">
            <div class="list-group channels mt-2 p-2" style="max-height: 500px; overflow-y: scroll; ">
              <a v-for="channel in filteredChannels" href="#" class="list-group-item list-group-item-action" @click="() => {
                btnClose.click();
                callback(channel);
              }">
                <div class="d-flex align-items-center">
                  <div class="d-flex justify-content-center align-items-center logo-container me-3">
                    <img class="logo" v-lazy="channel.logo" alt="Logo" loading="lazy"/>
                  </div>
                  <div><span>{{ channel.name }}</span></div>
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
  width:80px;
  height: 80px;
}
  .logo {
    max-width: 100%;
    max-height: 80px;
  }
</style>
