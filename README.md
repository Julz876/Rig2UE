# Rig2UE - Blender to Unreal Rigging Tool
Blender to Unreal Rigging Tool - Convert custom rigs to Unreal-ready skeletons with one-click export.

**Compatible with:** Blender 4.2 and above  
**Author:** KingxJulz

---

## Description

**Rig2UE** is a professional Blender addon that converts custom rigs  
into Unreal Engine's standard skeletons (UE5 / UE4 / MetaHuman),  
Clean parenting, skin weight transfer, blend shape support, and FBX export are ready for retargeting.

---

## Features

- ✅ Auto bone mapping with manual override
- ✅ Save and load mapping presets
- ✅ Correct arm and hand poses (A-Pose ⇆ T-Pose)
- ✅ Copy skin weights **and** blend shapes (shape keys)
- ✅ Export Unreal Engine 5-ready FBX
- ✅ One-click full pipeline (Convert Rig + Copy Weights + Export)
- ✅ Collapsible bone mapping list
- ✅ Safe warnings for preset saving and mapping refresh
- ✅ Advanced Mode ready for future expansion

---

## Installation

1. Open **Blender**
2. Go to **Edit → Preferences → Add-ons**
3. Click **Install...** and select the `Rig2UE.zip`
4. Enable **Rig2UE** in the addon list

---

## Basic Usage

1. Select your **source rig** in the dropdown.
2. Choose a **target profile** (UE5, UE4, or MetaHuman).
3. Press **Convert Rig**.
4. _(Optional)_ Correct Pose (switch A-Pose ⇆ T-Pose if needed).
5. Copy Weights and Blend Shapes automatically.
6. Export a clean FBX for Unreal Engine!

You can also use **[One-Click Full Export]** for the fastest workflow!

---

## Important Notes

- ⚠️ **Save your project** before saving mapping presets.
- Mapping presets are stored relative to your `.blend` file:  
  `//presets/rig2ue_mappings/`
- Saving presets without a saved project will trigger a warning popup.
- Rig2UE handles Blend Shapes (Shape Keys) copying automatically.
- Refreshing the mapping will overwrite manual edits (warning shown).

---
