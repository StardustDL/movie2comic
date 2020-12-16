<template>
  <div v-if="!sessionId">
    <a-space direction="vertical" style="width: 100%">
      <a-space>
        <a-radio-group v-model:value="type" button-style="solid" size="large">
          <a-radio-button :value="0">
            <span class="mdi mdi-plus"></span>
            New
          </a-radio-button>
          <a-radio-button :value="1">
            <span class="mdi mdi-open-in-app"></span>
            Existed
          </a-radio-button>
        </a-radio-group>
        <a-switch
          v-model:checked="auto"
          checked-children="Auto"
          un-checked-children="Manual"
        />
      </a-space>
      <div>
        <a-upload-dragger
          v-if="type == 0"
          :action="$store.getters.sessionRootUrl"
          name="file"
          @change="onNew"
        >
          <p class="ant-upload-drag-icon">
            <span class="mdi mdi-upload" style="font-size: xx-large"></span>
          </p>
          <p class="ant-upload-text">
            Click or drag file to this area to upload
          </p>
          <p class="ant-upload-hint">Only one video file is allowed.</p>
        </a-upload-dragger>
        <div v-else>
          <a-space direction="vertical" style="width: 100%">
            <a-input placeholder="session ID" v-model:value="sid">
              <template v-slot:suffix>
                <a-button-group>
                  <a-button type="primary" @click="onExisted">
                    <span class="mdi mdi-check"></span>
                    OK
                  </a-button>
                  <a-button @click="onRefreshSessionList">
                    <span class="mdi mdi-autorenew"></span>
                    Refresh
                  </a-button>
                </a-button-group>
              </template>
            </a-input>
            <a-card title="Sessions">
              <a-card-grid
                v-for="sid in sessions"
                :key="sid"
                @click="onSelectSession(sid)"
                style="width: 100%"
              >
                <a-card-meta :title="sid"> </a-card-meta>
              </a-card-grid>
            </a-card>
          </a-space>
        </div>
      </div>
    </a-space>
  </div>
  <div v-else>
    <a-space direction="vertical" style="width: 100%">
      <a-input
        :value="sessionId"
        readonly
        addon-before="Session ID"
        size="large"
      >
        <template v-slot:suffix>
          <a-button type="danger" @click="onClose">
            <span class="mdi mdi-close"></span>
            Close
          </a-button>
        </template>
      </a-input>
      <a-button
        @click="onWork"
        size="large"
        style="width: 100%"
        :loading="$store.state.state == SessionState.OnInput"
        :disabled="$store.state.state == SessionState.OnInput"
      >
        {{
          $store.state.state > SessionState.OnInput ? "Information" : "Analysis"
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
              v-if="$store.state.state >= SessionState.AfterInput"
            >
              <span class="mdi mdi-refresh"></span>
              Redo
            </a-button>
          </a-space>
        </a-collapse-panel>
      </a-collapse>
      <div v-if="$store.state.state >= SessionState.AfterInput">
        <a-descriptions title="Video Info">
          <a-descriptions-item label="Name">
            {{ result.info.name }}
          </a-descriptions-item>
          <a-descriptions-item label="Format">
            {{ result.info.format }}
          </a-descriptions-item>
          <a-descriptions-item label="Duration">
            {{ readableSecondTimeString(result.info.duration) }}
          </a-descriptions-item>
          <a-descriptions-item label="Width">
            {{ result.info.width }}
          </a-descriptions-item>
          <a-descriptions-item label="Height">
            {{ result.info.height }}
          </a-descriptions-item>
        </a-descriptions>
      </div>
      <a-card v-if="$store.state.state >= SessionState.AfterInput">
        <template v-slot:title>
          <span class="mdi mdi-video"></span>
          Input
        </template>
        <video controls :src="videoUrl" style="width: 100%"></video>
      </a-card>
    </a-space>
    <a-drawer
      title="Input Analyzing Result"
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
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { message } from "ant-design-vue";
import { notification } from "ant-design-vue";
import { readableSecondTimeString } from "@/helpers";
import { SessionState, SessionStage } from "@/models/enum";

export default defineComponent({
  name: "Start",
  data() {
    return {
      SessionStage: SessionStage,
      SessionState: SessionState,
      type: 0,
      sid: null,
      auto: false,
      sessions: [],
      result: {
        name: "",
        success: false,
        log: "",
        duration: 0,
        info: {
          duration: 0,
          name: "",
          format: "",
          width: 0,
          height: 0,
        },
      },
      info: {
        enable: false,
      },
      updateInterval: -1,
    };
  },
  computed: {
    sessionId() {
      return this.$store.state.sessionId;
    },
    videoUrl() {
      return `${this.$store.getters.sessionUrl}/video`;
    },
    basicUrl() {
      return `${this.$store.getters.sessionUrl}/input`;
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
      notification.info({ message: "Start input analyzing." });
    },
    async getResult() {
      const result = await fetch(this.basicUrl).then((res) => res.json());
      this.result = result;
      const noti = { message: "Input analyzing finished." };
      if (result.success) {
        notification.success(noti);
      } else {
        notification.error(noti);
      }
    },
    onNew(event: any) {
      if (event.file.status == "done") {
        this.$store.commit("setSession", event.file.response.toString());
        message.success(`${event.file.name} file uploaded successfully`);
      } else if (event.file.status == "error") {
        message.error(`${event.file.name} file upload failed.`);
      }
    },
    onRefreshSessionList() {
      fetch(`${this.$store.getters.sessionRootUrl}/all`)
        .then((res) => res.json())
        .then((sids) => {
          this.sessions = sids;
        });
    },
    onExisted() {
      this.$store.commit("setSession", this.sid);
    },
    onSelectSession(sid: string) {
      this.$store.commit("setSession", sid);
    },
    onClose() {
      this.$store.commit("setSession", "");
    },
    onWork() {
      if (this.$store.state.state < SessionState.AfterInput) {
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
    this.onRefreshSessionList();
    this.updateInterval = setInterval(() => {
      if (
        this.$store.state.state >= SessionState.AfterInput &&
        this.result.name == ""
      ) {
        this.getResult();
      }
    }, 2000);
  },
  unmounted() {
    if (this.updateInterval >= 0) {
      clearInterval(this.updateInterval);
      this.updateInterval = -1;
    }
  },
});
</script>
