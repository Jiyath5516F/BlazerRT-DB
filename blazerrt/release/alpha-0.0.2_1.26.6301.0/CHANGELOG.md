# BlazerRT alpha 0.0.2: every change since the first release (6 September 2026)

## Minecraft support
### Minecraft 1.26.6301 (release)
### Minecraft Preview 1.26.7022
### All five shader files for each version, star files included
### Works with the new shader file layout from Minecraft 1.26.60 on

## Live settings: BlazerRT Live Settings Controller
### New name for RTXControl
### Your RTXControl settings come over on first start
### Works on Minecraft 1.26.6301 and Preview 1.26.7022
### 233 live settings, 218 of them in the F6 panel
### Changes show up in the image within a second
### Presets from Potato to Cinematic that you can actually see
### Presets never touch Clouds, Depth of field, Aurora or Lens flare
### Settings that do nothing right now are greyed out, with a one-click fix
### Search and saved profiles
### Status line says Live, Waiting for ray tracing, Paused or Game version not supported
### A signature file brings live settings back after a game update, no rebuild needed
### The camera and mouse stay put when you open or close the panel
### Game input is blocked while the panel is open
### The mod's built-in defaults match the shader
### Glow multiplier and Light source multiplier moved to Advanced
### Panel settings that had no effect are gone
### Smooth panel motion, the BlazerRT logo typeface and an acrylic background
### Reduce motion and Acrylic background switches
### Without the mod, the pack runs on its own defaults

## Mob, item and held-block PBR
### Mobs get metal, roughness, glow and height
### Held, framed and dropped items get materials
### Pixel-edge bevels on mobs and items
### Glowing mobs and items
### Inventory icons stay solid with item PBR
### Animated blocks get the right material on every frame
### Finer relief on high-resolution mob textures
### BlazerBake: bake mob, item and held-block PBR into your own packs
### BlazerBake: clear a bake again

## Rain and snow
### Ray-traced rain and snow
### Fine, short raindrop streaks
### No rain indoors or under roofs
### Raindrops catch the light of the sun, moon and lamps
### BlazerRT Rain Off pack hides Minecraft's own rain
### Rain dims the sun and sky instead of a grey screen overlay
### Wet surfaces and puddles in rain, dry under roofs
### Softer shadows in rain
### Rainy weather feels colder

## Light
### Up to three bounces of light (was one)
### Torches and lamps: up to 16 nearby lights (was two)
### Light range and brightness you can change live
### Glowstone, sea lanterns and froglights light up a room properly
### Glowing blocks keep their own colour, day and night
### Flames and lava keep their colour and texture
### Glowing textures keep their pattern at night
### Light blocks glow evenly on every face
### Lamps keep their colour
### The floor next to a lamp is no longer brighter than the lamp
### Fire and campfire light stays steady
### Lanterns and other animated lights stop flickering on the floor
### Flames no longer cast shadows of their own light
### A torch in your hand lights up the world
### Held light no longer picks up lights placed near you
### Light through stained glass takes the glass colour
### Barrier blocks and other invisible blocks no longer block or tint light
### The End and other fixed-colour skies light the world in their own colour
### No light seams along block diagonals
### Even colour in shadowed corners
### Fewer bright specks after loading a world or teleporting
### Optional extras, off by default: sky light probe, reused screen shadows, blue-noise light sampling, physical moonlight colour, EON diffuse

## Shadows
### The sun casts shadows at its real size
### Shadows get softer further from what casts them
### Shadow softness is its own setting
### 1 to 16 sun shadow rays, set by the preset
### Shadow distance, trace rate, half-rate fog shadows and simpler leaf shadows for more speed
### Cloud shadows on the ground, soft or realistic

## Sky and night
### New physical sky
### The sun and moon stop at 50 degrees, and the limit is a setting
### Midnight looks like midnight
### No leftover daylight after /time set
### Sunsets and sunrises without flickering light
### New star field
### A moon with phases
### Milky Way haze and a warmer glow on the horizon at night
### Aurora on clear nights
### A rotating spiral galaxy in the End sky

## Clouds
### Volumetric clouds with low, mid and high thin layers
### Cloud cover follows the weather
### Billowy clouds with flatter bases
### Clouds reach the horizon
### Silver linings, sunset colours and moonlit clouds

## Fog
### Physical height fog, out to your render distance
### Dawn and dusk mist, rain and snow haze, patchy humidity
### Soft light shafts when the sun is low
### Fog follows the ground: no fog wall over superflat worlds or in caves
### No glowing fog columns over lava and fire
### Mist and weather haze only under the open sky
### No bright haze over a field of lamps at night
### No blocky fog around lights with DLSS
### No speckled glow in the fog around lamps

## Water and surfaces
### New water surface with drifting waves
### Clear water by default
### Wave speed and strength you can change live
### Underwater looks like the sea, not lime
### Smoother highlights on water and normal-mapped blocks
### Sharper roads and floors at low angles
### MER roughness used as you made it
### Cracks and gaps between stones catch less light
### Animated blocks with height maps no longer show a grid of lines

## Exposure and colour
### Night exposure with its own limit, no fixed night boost
### Exposure adapts when lava or a big fire fills the view at night
### Daylight exposure and adaptation speed you can change live
### GT7 tone mapping
### AgX (Standard, Punchy, Soft) and Neutral tone mapping
### White menus and text are no longer dimmed
### Live colour grading: contrast, gain, gamma, lift, white balance, tint, vibrance, saturation

## Lens and bloom
### Physical depth of field with near and far blur, autofocus and real bokeh, off by default
### Physical, Cinematic and Gameplay lens looks
### The bloom slider works
### Bloom is back on Minecraft 1.26.60 and later
### Sun and moon lens flare, and lamps never make flare ghosts
### Optional chromatic aberration, film grain, sharpening and vignette, all off by default

## Performance
### The last two full-screen passes are about 3 ms faster each with DLSS Performance
### Lighter default cost for clouds, reflections and shadow rays
### Presets timed on real game frames: Potato at about 56% of High's frame time, Cinematic at about 127%

## Removed or replaced
### The fixed +2.5 EV night boost
### The daytime washed-out look of glowing blocks and the lava re-colouring
### The hidden 1.7x glow boost in bounce light
### Two-lamp light sampling and the one-bounce limit
### The roughness remap
### The old foliage wrap lighting
### The exposure dip after teleports and dimension changes
### The 60 degree sun limit and the oversized shadow sun
### The old bloom and the radial colour fringing
### The old disabled depth of field
### The Star Nest End sky and the old star field
### The old glow fade on glowing blocks

## Known issues
### DLSS can still streak animated flames
### Mobs, items and held blocks use height for relief, not normal maps
