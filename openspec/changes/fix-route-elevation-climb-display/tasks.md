## 1. Fix clearMapOverlays

- [x] 1.1 Replace `map.clearOverlays()` with individual `map.removeOverlay()` calls for `currentMarkers`, `distanceMarkers`, and `climbPolylines`, each wrapped in try/catch
- [x] 1.2 Keep `showPowerLegend.value = false` reset (from previous fix)

## 2. Harden selectRoute

- [x] 2.1 Move `clearMapOverlays()` call from outside the try block to inside the try block in `selectRoute()`
- [x] 2.2 Add nullish coalescing guard for `data.elevation_gain` in the `ElMessage.success` call: `(data.elevation_gain ?? 0).toFixed(0)`

## 3. Verification

- [x] 3.1 Verify route elevation panel (distance/gain/loss stats) displays after selecting a route
- [x] 3.2 Verify climb segments are highlighted on the map after selecting a route with climbs
- [x] 3.3 Verify activity power legend and power-colored route still work correctly on activities tab
- [x] 3.4 Verify no JavaScript errors in browser console during route selection
