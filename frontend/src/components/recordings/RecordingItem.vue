<script setup lang="ts">
import { PropType, ref, watch } from "vue";
import { VideoSource } from "../../service/entities";
import { getStatus } from "../../service/utils";
import { gettext } from "../../main";

const props = defineProps({
  isActive: Boolean,
  id: Number,
  start_time: Date,
  end_time: Date,
  name: String,
  gap_between_retries: Number,
  use_backup_after: Number,
  total_retries: Number,
  default_source: Object as PropType<VideoSource>,
});
const type = ref("new");
function changeColor() {
  type.value = getStatus(props);
}
watch(() => props.start_time, changeColor);
changeColor();
</script>

<template>
  <div class="col-12 col-xl-6 mb-2">
    <div
      class="card flex-row p-2 cursor"
      :class="[type, isActive ? 'active' : 'inactive']"
    >
      <div
        class="d-flex justify-content-center align-items-center card-img-left"
      >
        <img
          class="logo"
          :src="props.default_source && props.default_source.logo"
          alt="Logo"
        />
      </div>
      <div class="card-body">
        <h4 class="card-title h5 h4-sm">{{ props.name }}</h4>
        <p class="card-text">
          {{ props.start_time && props.start_time.toLocaleString() }} -
          {{ props.end_time && props.end_time.toLocaleString() }}
        </p>
        <p class="card-text">
          <strong>{{ gettext("Essais :") }}</strong>
          {{ props.total_retries ?? 0 }}
        </p>
        <p class="card-text">
          <strong>{{ gettext("Chaine :") }}</strong>
          {{
            (props.default_source && props.default_source.name) ??
            gettext("Inconnue")
          }}
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.logo {
  max-width: 100%;
}
.cursor {
  cursor: pointer;
}
.card-img-left {
  float: left;
  max-width: 80px;
  max-height: 150px;
}
.recording-item {
  height: 150px;
  cursor: pointer;
}
.new {
  background: #dcdcec;
  &:hover {
    background: $new;
  }
}
.upcoming {
  background: #e7dcec;
  &:hover {
    background: $upcoming;
  }
}
.running {
  background: #e0ecdc;
  &:hover {
    background: $running;
  }
}
.passed {
  background: #ece7dc;
  &:hover {
    background: $passed;
  }
}

.title {
  font-size: 15pt;
}

.active {
  opacity: 0.5;
}
</style>
