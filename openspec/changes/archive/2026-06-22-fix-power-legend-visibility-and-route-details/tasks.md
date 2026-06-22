## 1. Fix Power Legend Visibility

- [x] 1.1 Add `currentTab === 'activities' && selectedActivity` conditions to power legend `v-show` in `static/index.html` (line ~246)
- [x] 1.2 Add `showPowerLegend.value = false` to `clearMapOverlays()` function in `static/index.html`

## 2. Fix Route Details Loading (Root Cause)

- [x] 2.1 Replace fragile per-overlay `map.removeOverlay()` loops in `clearMapOverlays()` with robust `map.clearOverlays()` wrapped in try/catch, matching `clearMap()`'s approach

## 3. Verification

- [x] 3.1 Verify power legend is NOT displayed on chat tab map (even after viewing an activity with power data)
- [x] 3.2 Verify power legend is NOT displayed on routes tab map (even after viewing an activity with power data)
- [x] 3.3 Verify power legend IS displayed on activities tab when an activity with power data is selected
- [x] 3.4 Verify route details (climb segments, elevation panel, distance markers) load correctly on routes tab after switching from activities tab
