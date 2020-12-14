<template>
  <a-space direction="vertical" style="width: 100%">
    <a-button
      @click="onWork"
      size="large"
      style="width: 100%"
      :loading="$store.state.state == SessionState.OnStyle"
      :disabled="$store.state.state == SessionState.OnStyle"
    >
      {{
        $store.state.state > SessionState.OnStyle ? "Information" : "Transfer"
      }}
    </a-button>
    <a-card>
      <template v-slot:title>
        <span class="mdi mdi-flower"></span>
        Styled Frames
      </template>
      <a-card-grid
        v-for="frame in result.frames"
        :key="frame.name"
        @click="onPreview(frame)"
        style="width: 25%; text-align: center"
      >
        <img :src="previewUrl(frame.name)" style="width: 100%" />
        <a-card-meta :title="frame.name"> </a-card-meta>
      </a-card-grid>
    </a-card>
  </a-space>
  <a-modal
    width="1080px"
    v-model:visible="preview.enable"
    :title="`${preview.frame.name}`"
    :footer="null"
  >
    <img :src="previewUrl(preview.frame.name)" style="width: 100%" />
  </a-modal>
  <a-drawer
    title="Style Transferring Result"
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
      <template v-slot:extra>
        <a-button @click="onRedo">
          <span class="mdi mdi-refresh"></span>
          Redo
        </a-button>
      </template>
    </a-result>
  </a-drawer>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { notification } from "ant-design-vue";
import { readableSecondTimeString } from "@/helpers";
import { SessionState } from "@/models/enum";

export default defineComponent({
  name: "Style",
  data() {
    return {
      SessionState: SessionState,
      result: {
        name: "",
        success: false,
        log: "",
        duration: 0,
        frames: [],
      },
      preview: {
        enable: false,
        frame: {
          name: "",
        },
      },
      info: {
        enable: false,
      },
    };
  },
  computed: {
    basicUrl() {
      return `${this.$store.getters.sessionUrl}/styles`;
    },
  },
  methods: {
    readableSecondTimeString(value: number) {
      return readableSecondTimeString(value);
    },
    async work(redo = false) {
      const data = {
        redo: redo,
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
      notification.info({ message: "Start style transferring." });
    },
    async getResult() {
      const result = await fetch(this.basicUrl).then((res) => res.json());
      this.result = result;
      const noti = { message: "Style transferring finished." };
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
      if (this.$store.state.state < SessionState.AfterStyle) {
        this.work();
      } else {
        this.info.enable = true;
      }
    },
    onRedo() {
      this.work(true);
      this.result.name = "";
    },
    onPreview(frame: any) {
      this.preview.frame = frame;
      this.preview.enable = true;
    },
  },
  mounted() {
    if (this.$store.state.state >= SessionState.AfterStyle) {
      this.getResult();
    }
  },
});
</script>
