// const PREPURL = "";
const PREPURL = "http://localhost:5050" // Debug

const App = {
    data() {
        return {
            sessionId: "59a999a0-3c36-11eb-9ac1-c83dd4eac83a",
            currentStep: 1,
            model: {
                selectedStep: 0,
            },
            apiUrl: PREPURL,
            pages: {
                p0: {
                    inputFile: null,
                },
                p1: {
                    result: {
                        name: "",
                        success: false,
                        log: "",
                        duration: 0,
                        frames: [],
                    }
                },
                p2: {
                    result: {
                        name: "",
                        success: false,
                        log: "",
                        duration: 0,
                        subtitles: [],
                    }
                },
                p3: {
                    result: {
                        name: "",
                        success: false,
                        log: "",
                        duration: 0,
                        frames: [],
                    }
                }
            }
        }
    },
    methods: {
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
        onStartKeyframeExtractor() {
            this.workFrames();
        },
        onGetFrames() {
            this.resultFrames();
        },
        //#region frames
        async workFrames() {
            let settings = {
                method: 'PUT',
            };
            await fetch(this.framesUrl, settings).then(res => res.text()).then(text => {
                console.log(text);
            });
        },
        async resultFrames() {
            let result = await fetch(this.framesUrl).then(res => res.json());
            this.pages.p1.result = result;
        },
        frameImageUrl(name) {
            return `${this.framesUrl}/${name}`;
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
        },
        async resultSubtitles() {
            let result = await fetch(this.subtitlesUrl).then(res => res.json());
            this.pages.p1.result = result;
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
        },
        async resultStyles() {
            let result = await fetch(this.stylesUrl).then(res => res.json());
            this.pages.p1.result = result;
        },
        styledImageUrl(name) {
            return `${this.stylesUrl}/${name}`;
        },
        //#endregion
        getStepStatus(id) {
            if (id < this.currentStep) {
                return "finish";
            }
            else if (id == this.currentStep) {
                return "process";
            }
            else if (id > this.currentStep) {
                return "wait";
            }
            return "wait";
        },
        onUploadChange(event) {
            if (event.file.status !== 'uploading') {
            }
            if (event.file.status === 'done') {
                this.sessionId = event.file.response;
                this.currentStep = 1;
                this.model.selectedStep = 1;
                this.$message.success(`${event.file.name} file uploaded successfully`);
            } else if (event.file.status === 'error') {
                this.$message.error(`${event.file.name} file upload failed.`);
            }
        }
    },
    computed: {
        selectedStep: {
            get() {
                return this.model.selectedStep;
            },
            set(newValue) {
                if (newValue > this.currentStep) {
                    this.$message.warning('Please complete this step first.');
                    newValue = this.currentStep;
                }
                this.model.selectedStep = newValue;
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
    }
};
var app = Vue.createApp(App).use(antd);
app.mount("#app");
