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
      <video
        v-if="enableVideoPreview"
        controls
        :src="videoUrl"
        style="width: 100%"
      ></video>
    </a-space>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { message } from "ant-design-vue";
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
    };
  },
  computed: {
    sessionId() {
      return this.$store.state.sessionId;
    },
    videoUrl() {
      return `${this.$store.getters.sessionUrl}/video`;
    },
    enableVideoPreview() {
      return this.$store.state.state >= SessionState.AfterInput;
    },
  },
  methods: {
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
  },
  mounted() {
    this.onRefreshSessionList();
  },
});
</script>
