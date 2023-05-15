# Tiny-Sequence-Tools
Tools for creating multi-cam 2d animation sequences. Rotate 2D Characters to 3D Cameras, and control the thickness of line art modifiers per scene strips.

## Create Scene Strip
![new_strip](https://github.com/NickTiny/Tiny-2D-Sequence-Tools/assets/86638335/b5c49a3a-03a3-490d-ad74-57f2818b83a3)
1. Open Sequence Editor
2. Use `Add Camera as Scene Strip`

## Change Strip Camera
![change_camera](https://github.com/NickTiny/Tiny-2D-Sequence-Tools/assets/86638335/7db80d93-a2ba-4f40-8475-823828d04a94)
1. Select a Strip
2. Select a Camera from Dropdown
3. Hit `Refresh` to update viewport

## Rotate to Strip Camera
![enable_rotate_to_camera](https://github.com/NickTiny/Tiny-2D-Sequence-Tools/assets/86638335/aefc2eb2-c4f9-4bf6-9d18-09754ba8c7a5)
1. Select an object
2. Open Object Constraints in Properties Panel
3. Select `Enable` Under 'Rotate to Strip Camera'

## Sequence Line Art
![create_line_art](https://github.com/NickTiny/Tiny-2D-Sequence-Tools/assets/86638335/a706d47d-9197-4b8d-aca4-7fb01998800f)
1. Create new Blank Grease Pencil Object
2. Open Object Modifiers in Properties Panel
3. Select `Enable` Under 'Sequence Line Art'
4. In Sequencer SidePanel enable 'Use Sequence Line Art'
5. Use Refresh Button to Update Line Art Items list
6. Select a new thickness value to be set for the current sequence strip 

## Save with Collabration Settings
![save_with_collab](https://github.com/NickTiny/Tiny-2D-Sequence-Tools/assets/86638335/c0568650-094d-407f-b4a9-9318aa43346a)
1. Hit CTRL+S or File>Save
2. Under your Mouse a pop up will appear if your file doesn't meet collaboration standards
3. Select each property to fix the problem in your file
4. Re-attempt CTRL+S save if your settings are correct there will be no prompt

## Rendering
![image](https://github.com/NickTiny/Tiny-2D-Sequence-Tools/assets/86638335/09a38f9f-9a6a-46d7-9bee-c61979863da8)
1. Set Engine to Workbench for Preview Quality Render, otherwise use Eevee
2. Select a disired fraction of your resolution under resolution
3. Enabling `Selection Only` will only render the highlighted clips in the VSE
4. Use `Sequence Batch Render` to begin rendering

**NOTE: Clips render without Sequencer Audio**
