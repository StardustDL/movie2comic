export enum SessionStage {
    Create = 0,
    Input = 1,
    Frame = 2,
    Subtitle = 3,
    Style = 4,
    Output = 5
}

export enum SessionState {
    AfterCreate = 0,
    AfterInitialize = 1,
    OnInput = 2,
    AfterInput = 3,
    OnFrame = 4,
    AfterFrame = 5,
    OnSubtitle = 6,
    AfterSubtitle = 7,
    OnStyle = 8,
    AfterStyle = 9,
    OnOutput = 10,
    AfterOutput = 11
}

export enum StepPageNames {
    Start = "start",
    Frame = "frame",
    Subtitle = "subtitle",
    Style = "style",
    Comic = "comic",
}