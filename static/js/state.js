
// keeps track of what the app is doing
export const state = {
    currentPlaylistUri: null, // curent playlist 
    isTransitioningPlaylist: false, 
    lastDecisionTime: null, // when program asked user to cahnge last
    lastMoodChange: null    // when mood changed last
};

export const constants = {
    DECISION_COOLDOWN: 60000,
    MOOD_CHECK_INTERVAL: 10000,
    EMOTION_DISPLAY_INTERVAL: 1000 // 1 sec
};


