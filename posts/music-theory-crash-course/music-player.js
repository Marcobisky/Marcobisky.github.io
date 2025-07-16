function createMusicPlayer(containerId, abc, instrument = 0) {
    // Render the musical notation
    const visualObj = ABCJS.renderAbc(containerId + "-music", abc, {
        responsive: "resize",
        add_classes: true
    });

    // Create audio controls using the proven approach from the preview
    const instrumentName = ABCJS.synth.instrumentIndexToName[instrument] || 'acoustic_grand_piano';
    const controlsHtml = `
        <div class="audio-controls-custom">
            <span class="instrument-label">${instrumentName}</span>
            <div id="${containerId}-audio"></div>
            <button class="activate-audio-btn" data-container="${containerId}">🎵 Activate Audio</button>
        </div>
    `;
    
    // Insert controls after the music container
    const musicContainer = document.getElementById(containerId + "-music");
    if (musicContainer) {
        musicContainer.insertAdjacentHTML('afterend', controlsHtml);
    }

    // Set up the activation handler
    const activateBtn = document.querySelector(`[data-container="${containerId}"]`);
    if (activateBtn) {
        activateBtn.addEventListener("click", function() {
            activateAudio(containerId, visualObj[0], instrument);
            activateBtn.style.display = 'none'; // Hide the activate button once clicked
        });
    }
}

function activateAudio(containerId, visualObj, instrument) {
    if (ABCJS.synth.supportsAudio()) {
        const controlOptions = {
            displayRestart: true,
            displayPlay: true,
            displayProgress: true,
            displayLoop: false,
            displayWarp: false
        };
        
        const synthControl = new ABCJS.synth.SynthController();
        synthControl.load(`#${containerId}-audio`, null, controlOptions);
        synthControl.disable(true);
        
        const midiBuffer = new ABCJS.synth.CreateSynth();
        midiBuffer.init({
            visualObj: visualObj,
            options: {
                chordsOff: true,  // No accompaniment as requested
                program: instrument  // Use the specified instrument
            }
        }).then(function() {
            synthControl.setTune(visualObj, true, {
                chordsOff: true,  // No accompaniment as requested
                program: instrument  // Use the specified instrument
            }).then(function(response) {
                // Enable the controls once everything is loaded
                synthControl.disable(false);
                document.querySelector(`#${containerId}-audio .abcjs-inline-audio`).classList.remove("disabled");
            }).catch(function(error) {
                console.error('Error setting tune:', error);
            });
        }).catch(function(error) {
            console.error('Error initializing audio:', error);
        });
    } else {
        document.getElementById(containerId + "-audio").innerHTML = '<div class="audio-status">Audio not supported in this browser.</div>';
    }
}
