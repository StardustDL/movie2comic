<template>
  <a-space direction="vertical" style="width: 100%">
    <a-button
      @click="onWork"
      size="large"
      style="width: 100%"
      :loading="$store.state.state == SessionState.OnSubtitle"
      :disabled="$store.state.state == SessionState.OnSubtitle"
    >
      {{
        $store.state.state > SessionState.OnSubtitle
          ? "Information"
          : "Generate"
      }}
    </a-button>

    <a-collapse>
      <a-collapse-panel key="1" header="Operation">
        <a-space>
          <a-button @click="onRefresh">
            <span class="mdi mdi-autorenew"></span>
            Refresh
          </a-button>
          <a-button
            @click="onRedo"
            v-if="$store.state.state >= SessionState.AfterSubtitle"
          >
            <span class="mdi mdi-refresh"></span>
            Redo
          </a-button>
          <a-switch
            v-model:checked="isZhcn"
            checked-children="zh-CN"
            un-checked-children="en-US"
          />
        </a-space>
      </a-collapse-panel>
    </a-collapse>
    <a-card v-if="$store.state.state >= SessionState.AfterSubtitle">
      <template v-slot:title>
        <span class="mdi mdi-subtitles"></span>
        Subtitles
      </template>
      <a-card-grid
        v-for="subtitle in result.subtitles"
        :key="subtitle.name"
        @click="onPreview(subtitle)"
        style="width: 100%"
      >
        <a-card-meta :title="subtitle.text">
          <template v-slot:description>
            <span class="mdi mdi-clock"></span>
            {{ readableSecondTimeString(subtitle.start) }} ~
            {{ readableSecondTimeString(subtitle.end) }}
          </template>
        </a-card-meta>
      </a-card-grid>
    </a-card>
  </a-space>
  <a-modal
    width="1080px"
    v-model:visible="preview.enable"
    :title="`${preview.subtitle.name} ${readableSecondTimeString(
      preview.subtitle.start
    )} ~ ${readableSecondTimeString(preview.subtitle.end)}`"
    :footer="null"
  >
    <h1>{{ preview.subtitle.text }}</h1>
    <br />
    <audio
      controls
      :src="previewUrl(preview.subtitle.name)"
      style="width: 100%"
    ></audio>
  </a-modal>
  <a-drawer
    title="Subtitles Generating Result"
    placement="right"
    :closable="false"
    width="512"
    v-model:visible="info.enable"
  >
    <a-result
      :status="result.success ? 'success' : 'error'"
      :title="readableSecondTimeString(result.duration)"
      :sub-title="result.log"
    >
    </a-result>
  </a-drawer>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { notification } from "ant-design-vue";
import { readableSecondTimeString } from "@/helpers";
import { SessionState } from "@/models/enum";

export default defineComponent({
  name: "Subtitle",
  data() {
    return {
      SessionState: SessionState,
      isZhcn: false,
      result: {
        name: "",
        success: false,
        log: "",
        duration: 0,
        subtitles: [],
      },
      preview: {
        enable: false,
        subtitle: {
          name: "",
          text: "",
          start: 0,
          end: 0,
        },
      },
      info: {
        enable: false,
      },
    };
  },
  computed: {
    basicUrl() {
      return `${this.$store.getters.sessionUrl}/subtitles`;
    },
  },
  methods: {
    readableSecondTimeString(value: number) {
      return readableSecondTimeString(value);
    },
    async work(redo = false) {
      const data = {
        redo: redo,
        isZhcn: this.isZhcn,
      };
      const settings = {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      };
      await fetch(this.basicUrl, settings)
        .then((res) => res.text())
        .then((text) => {
          console.log(text);
        });
      notification.info({ message: "Start subtitle generating." });
    },
    async getResult() {
      const result = await fetch(this.basicUrl).then((res) => res.json());
      this.result = result;
      const noti = { message: "Subtitle generating finished." };
      if (result.success) {
        notification.success(noti);
      } else {
        notification.error(noti);
      }
    },
    previewUrl(name: string) {
      return `${this.basicUrl}/${name}`;
    },
    onWork() {
      if (this.$store.state.state < SessionState.AfterSubtitle) {
        this.work();
      } else {
        this.info.enable = true;
      }
    },
    onRefresh() {
      this.getResult();
    },
    onRedo() {
      this.work(true);
      this.result.name = "";
    },
    onPreview(subtitle: any) {
      this.preview.subtitle = subtitle;
      this.preview.enable = true;
    },
  },
  mounted() {
    if (this.$store.state.state >= SessionState.AfterSubtitle) {
      this.getResult();
    }
  },
});
</script>
