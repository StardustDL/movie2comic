<template>
  <a-layout style="min-height: 100vh">
    <a-layout-header :style="{ background: '#fff' }">
      <h1>
        <router-link to="/">Movie2Comic</router-link>
      </h1>
      <a-menu theme="light"> </a-menu>
    </a-layout-header>
    <a-layout-content style="margin-top: 30px">
      <a-row type="flex" justify="center" align="top">
        <a-col :span="18">
          <a-space direction="vertical" style="width: 100%">
            <a-steps :current="currentStep" type="navigation">
              <a-step
                :status="getStepStatus(StepPageNames.Start)"
                title="Start"
                description="Create project"
                :disabled="getStepStatus(StepPageNames.Start) == 'wait'"
                @click="onStepClick(StepPageNames.Start)"
              >
              </a-step>
              <a-step
                :status="getStepStatus(StepPageNames.Frame)"
                title="Keyframes"
                description="Extract frames"
                :disabled="getStepStatus(StepPageNames.Frame) == 'wait'"
                @click="onStepClick(StepPageNames.Frame)"
              >
              </a-step>
              <a-step
                :status="getStepStatus(StepPageNames.Subtitle)"
                title="Subtitles"
                description="Generate subtitles"
                :disabled="getStepStatus(StepPageNames.Subtitle) == 'wait'"
                @click="onStepClick(StepPageNames.Subtitle)"
              >
              </a-step>
              <a-step
                :status="getStepStatus(StepPageNames.Style)"
                title="Styles"
                description="Transfer styles"
                :disabled="getStepStatus(StepPageNames.Style) == 'wait'"
                @click="onStepClick(StepPageNames.Style)"
              >
              </a-step>
              <a-step
                :status="getStepStatus(StepPageNames.Comic)"
                title="Comic"
                description="Get the comic"
                :disabled="getStepStatus(StepPageNames.Comic) == 'wait'"
                @click="onStepClick(StepPageNames.Comic)"
              >
              </a-step>
            </a-steps>
            <router-view />
          </a-space>
        </a-col>
      </a-row>
    </a-layout-content>
    <a-layout-footer>
      Copyright <span class="mdi mdi-copyright"></span> 2020 - Movie2Comic -
      StardustDL -
      <a href="https://github.com/StardustDL/movie2comic"
        ><span class="mdi mdi-github"></span> GitHub</a
      >
    </a-layout-footer>
  </a-layout>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { SessionState, SessionStage, StepPageNames } from "@/models/enum";

export default defineComponent({
  data() {
    return {
      SessionStage: SessionStage,
      SessionState: SessionState,
      StepPageNames: StepPageNames,
      updateInterval: -1,
    };
  },
  computed: {
    processStage() {
      if (this.$store.state.state % 2 == 0) {
        // on
        return this.$store.state.stage;
      } else {
        // after
        return Math.min(
          this.$store.state.stage + 1,
          SessionStage.Output
        ) as SessionStage;
      }
    },
    currentStep() {
      switch (this.$router.currentRoute.value.name) {
        case StepPageNames.Start:
          return 0;
        case StepPageNames.Frame:
          return 1;
        case StepPageNames.Subtitle:
          return 2;
        case StepPageNames.Style:
          return 3;
        case StepPageNames.Comic:
          return 4;
      }
      return 0;
    },
  },
  methods: {
    getStepStatus(name: StepPageNames) {
      const ps = this.processStage;
      let id = SessionStage.Create;
      switch (name) {
        case StepPageNames.Frame:
          id = SessionStage.Frame;
          break;
        case StepPageNames.Subtitle:
          id = SessionStage.Subtitle;
          break;
        case StepPageNames.Style:
          id = SessionStage.Style;
          break;
        case StepPageNames.Comic:
          id = SessionStage.Output;
          break;
      }
      if (id == ps || (id == SessionStage.Create && ps == SessionStage.Input)) {
        return "process";
      } else if (id < ps) {
        return "finish";
      }
      return "wait";
    },
    onStepClick(name: StepPageNames) {
      if (this.getStepStatus(name) == "wait") {
        return;
      }
      this.$router.replace({ name: name });
    },
  },
  mounted() {
    if (process && process.env.NODE_ENV === "development") {
      this.$store.commit("setApi", "http://localhost:5050");
    }
    this.updateInterval = setInterval(() => {
      if (this.$store.state.sessionId) {
        this.$store.dispatch("updateState");
      } else {
        this.$store.commit("setState", 0);
        this.$store.commit("setStage", 0);
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

<style lang="scss">
.mdi {
  margin-right: 5px;
  font-size: large;
}
</style>
