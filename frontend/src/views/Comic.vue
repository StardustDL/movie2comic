<template>
  <a-space direction="vertical" style="width: 100%">
    <a-button
      @click="onWork"
      size="large"
      style="width: 100%"
      :loading="$store.state.state == SessionState.OnOutput"
      :disabled="$store.state.state == SessionState.OnOutput"
    >
      {{
        $store.state.state > SessionState.OnOutput ? "Information" : "Combine"
      }}
    </a-button>
    <a-collapse>
      <a-collapse-panel key="1" header="Operation">
        <a-space>
          <a-button @click="onRefresh">
            <span class="mdi mdi-autorenew"></span>
            Refresh
          </a-button>
          <a-button @click="onRedo" v-if="$store.state.state >= SessionState.AfterOutput">
            <span class="mdi mdi-refresh"></span>
            Redo
          </a-button>
        </a-space>
      </a-collapse-panel>
    </a-collapse>
    <a-card v-if="$store.state.state >= SessionState.AfterOutput">
      <template v-slot:title>
        <span class="mdi mdi-image"></span>
        Comic
      </template>
      <img :src="previewUrl(result.file)" style="width: 100%" />
    </a-card>
  </a-space>
  <a-drawer
    title="Comic Combination Result"
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
  name: "Comic",
  data() {
    return {
      SessionState: SessionState,
      result: {
        name: "",
        success: false,
        log: "",
        duration: 0,
        file: "",
      },
      info: {
        enable: false,
      },
    };
  },
  computed: {
    basicUrl() {
      return `${this.$store.getters.sessionUrl}/comics`;
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
      notification.info({ message: "Start comic combining." });
    },
    async getResult() {
      const result = await fetch(this.basicUrl).then((res) => res.json());
      this.result = result;
      const noti = { message: "Comic combining finished." };
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
      if (this.$store.state.state < SessionState.AfterOutput) {
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
  },
  mounted() {
    if (this.$store.state.state >= SessionState.AfterOutput) {
      this.getResult();
    }
  },
});
</script>
