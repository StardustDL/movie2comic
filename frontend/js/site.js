// const PREPURL = "";
const PREPURL = "http://localhost:5050" // Debug

const App = {
    data() {
        return {
            stages: {
                Create: 0,
                Input: 1,
                Frame: 2,
                Subtitle: 3,
                Style: 4,
                Output: 5
            },
            states: {
                AfterCreate: 0,
                AfterInitialize: 1,
                OnInput: 2,
                AfterInput: 3,
                OnFrame: 4,
                AfterFrame: 5,
                OnSubtitle: 6,
                AfterSubtitle: 7,
                OnStyle: 8,
                AfterStyle: 9,
                OnOutput: 10,
                AfterOutput: 11
            },
            apiUrl: PREPURL,
            // sessionId: null,
            sessionId: "59a999a0-3c36-11eb-9ac1-c83dd4eac83a", // DEBUG
            stage: 0,
            state: 0,
            model: {
                selectedStage: -1,
                auto: false,
            },
            pages: {
                start: {
                    type: 0,
                    sid: null,
                    auto: false,
                },
                frames: {
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
                            time: 0
                        }
                    },
                    info: {
                        enable: false
                    }
                },
                subtitles: {
                    result: {
                        name: "",
                        success: false,
                        log: "",
                        duration: 0,
                        subtitles: [],
                    },
                    info: {
                        enable: false
                    }
                },
                styles: {
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
                        }
                    },
                    info: {
                        enable: false
                    }
                }
            }
        }
    },
    methods: {
        async updateState() {
            if (this.sessionId != null) {
                let state = await fetch(`${this.sessionUrl}/state`).then(res => res.text());
                let stage = await fetch(`${this.sessionUrl}/stage`).then(res => res.text());
                this.state = parseInt(state);
                this.stage = parseInt(stage);
                if (this.model.selectedStage < 0) {
                    this.model.selectedStage = this.processStage;
                }
                if (this.state >= this.states.AfterFrame && this.pages.frames.result.name == "") {
                    this.resultFrames();
                }
                if (this.state >= this.states.AfterSubtitle && this.pages.subtitles.result.name == "") {
                    this.resultSubtitles();
                }
                if (this.state >= this.states.AfterStyle && this.pages.styles.result.name == "") {
                    this.resultStyles();
                }
            }
        },
        getStageStatus(id) {
            let ps = this.processStage;
            if (id < ps) {
                return "finish";
            }
            else if (id == ps) {
                return "process";
            }
            return "wait";
        },
        readableSecondTimeString(value) {
            let minute = Math.floor(value / 60);
            let second = Math.floor(value % 60);
            if (minute == 0) {
                return `${second}''`;
            }
            else if (second == 0) {
                return `${minute}'`;
            }
            else {
                return `${minute}'${second}''`;
            }
        },
        //#region start
        onStartNew(event) {
            if (event.file.status !== 'uploading') {
            }
            if (event.file.status === 'done') {
                this.sessionId = event.file.response;
                this.model.selectedStage = 0;
                this.model.auto = this.pages.start.auto;
                console.log(this.model.auto);
                this.$message.success(`${event.file.name} file uploaded successfully`);
            } else if (event.file.status === 'error') {
                this.$message.error(`${event.file.name} file upload failed.`);
            }
        },
        onStartExisted(event) {
            this.sessionId = this.pages.start.sid;
            this.model.auto = this.pages.start.auto;
        },
        //#endregion
        onWorkFrames() {
            if (this.state < this.states.AfterFrame) {
                this.workFrames();
            }
            else {
                this.pages.frames.info.enable = true;
            }
        },
        onPreviewFrame(frame) {
            this.pages.frames.preview.frame = frame;
            this.pages.frames.preview.enable = true;
        },
        onWorkSubtitles() {
            if (this.state < this.states.AfterSubtitle) {
                this.workSubtitles();
            }
            else {
                this.pages.subtitles.info.enable = true;
            }
        },
        onWorkStyles() {
            if (this.state < this.states.AfterStyle) {
                this.workStyles();
            }
            else {
                this.pages.styles.info.enable = true;
            }
        },
        onPreviewStyledFrame(frame) {
            this.pages.styles.preview.frame = frame;
            this.pages.styles.preview.enable = true;
        },
        //#region libs
        //#region frames
        async workFrames() {
            let settings = {
                method: 'PUT',
            };
            await fetch(this.framesUrl, settings).then(res => res.text()).then(text => {
                console.log(text);
            });
            this.$notification.info({ message: "Start frame extracting." });
        },
        async resultFrames() {
            let result = await fetch(this.framesUrl).then(res => res.json());
            this.pages.frames.result = result;
            let noti = { message: "Frame extracting finished." }
            if (result.success) {
                this.$notification.success(noti);
            }
            else {
                this.$notification.error(noti);
            }
        },
        frameImageUrl(name) {
            return `${this.framesUrl}/${name}`;
        },
        styledFrameImageUrl(name) {
            return `${this.stylesUrl}/${name}`;
        },
        //#endregion
        //#region subtitles
        async workSubtitles() {
            let settings = {
                method: 'PUT',
            };
            await fetch(this.subtitlesUrl, settings).then(res => res.text()).then(text => {
                console.log(text);
            });
            this.$notification.info({ message: "Start subtitle generating." });
        },
        async resultSubtitles() {
            let result = await fetch(this.subtitlesUrl).then(res => res.json());
            this.pages.subtitles.result = result;
            let noti = { message: "Subtitle generating finished." }
            if (result.success) {
                this.$notification.success(noti);
            }
            else {
                this.$notification.error(noti);
            }
        },
        //#endregion
        //#region styles
        async workStyles() {
            let settings = {
                method: 'PUT',
            };
            await fetch(this.stylesUrl, settings).then(res => res.text()).then(text => {
                console.log(text);
            });
            this.$notification.info({ message: "Start style transferring." });
        },
        async resultStyles() {
            let result = await fetch(this.stylesUrl).then(res => res.json());
            this.pages.styles.result = result;
            let noti = { message: "Style transferring finished." }
            if (result.success) {
                this.$notification.success(noti);
            }
            else {
                this.$notification.error(noti);
            }
        },
        styledImageUrl(name) {
            return `${this.stylesUrl}/${name}`;
        },
        //#endregion
        //#endregion
    },
    computed: {
        processStage() {
            if (this.state % 2 == 0) { // on
                return this.stage;
            }
            else { // after
                return this.stage + 1;
            }
        },
        selectedStage: {
            get() {
                return this.model.selectedStage >= 0 ? this.model.selectedStage : 0;
            },
            set(newValue) {
                this.model.selectedStage = newValue;
            }
        },
        sessionRootUrl() {
            return `${this.apiUrl}/api/session`;
        },
        sessionUrl() {
            return `${this.sessionRootUrl}/${this.sessionId}`;
        },
        videoUrl() {
            return `${this.sessionUrl}/video`;
        },
        framesUrl() {
            return `${this.sessionUrl}/frames`;
        },
        subtitlesUrl() {
            return `${this.sessionUrl}/subtitles`;
        },
        stylesUrl() {
            return `${this.sessionUrl}/styles`;
        },
    },
    mounted() {
        setInterval(() => {
            if (this.sessionId != null) {
                this.updateState();
                if (this.model.auto) {
                    switch (this.state) {
                        case this.states.AfterInput:
                            this.model.selectedStage = this.stages.Input;
                            this.workFrames();
                            break;
                        case this.states.AfterFrame:
                            this.model.selectedStage = this.stages.Frame;
                            this.workSubtitles();
                            break;
                        case this.states.AfterSubtitle:
                            this.model.selectedStage = this.stages.Subtitle;
                            this.workStyles();
                            break;
                        case this.states.AfterStyle:
                            this.model.selectedStage = this.stages.Style;
                            break;
                        case this.states.AfterOutput:
                            this.model.auto = false;
                            break;
                    }
                }
            }
        }, 2000);
    }
};
var app = Vue.createApp(App).use(antd);
app.mount("#app");
