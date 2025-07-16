// Music configuration for harmony crash course
const MUSIC_CONFIG = {
    // Default player settings
    defaultOptions: {
        chordsOff: true,
        showControls: true,
        responsive: "resize",
        add_classes: true,
        tempo: null, // Use tempo from ABC notation
        volume: 80
    },
    
    // Button texts
    ui: {
        playText: "Play Music",
        playingText: "Playing...",
        stopText: "Stop",
        loadingText: "Loading audio...",
        preparingText: "Preparing audio...",
        errorPrefix: "Audio error: ",
        unsupportedText: "Audio not supported in this browser."
    },
    
    // CSS selectors and IDs
    selectors: {
        musicSuffix: "-music",
        playBtnSuffix: "-play-btn",
        stopBtnSuffix: "-stop-btn",
        statusSuffix: "-audio-status"
    }
};
