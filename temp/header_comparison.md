# TSV Header Comparison Analysis

## Overview

This document compares the header structures between two TSV files:
- **V.00.03.ISOF.tsv** (15 columns)
- **V.00.04.ISOF.tsv** (22 columns)

## Header Comparison

### **V.00.03.ISOF.tsv Headers (15 columns):**
```
PHASE_NUM	PHASE_START	PHASE_END	SCENE_NUM	LOC_TYPE	DIURNAL	LOCATION	SPECIFIC AREA	SHOT_NUM	MOVE_SPEED	MOVE_TYPE	ANGLE	SHOT_DESCRIPTION	IN	OUT
```

### **V.00.04.ISOF.tsv Headers (22 columns):**
```
PHASE_NUM	PHASE_START	PHASE_END	SCENE_NUM	SCENE_CONTEXT_COMMENT	LOC_TYPE	DIURNAL	LIGHT_SOURCE(S)	SEASON	PERIOD	WEATHER	LOCATION	SPECIFIC AREA	SHOT_NUM	MOVE_SPEED	MOVE_TYPE	VIDEO_PROMPT	ANGLE	SHOT_DESCRIPTION	IMAGE_PROMPT	OREF	IN	OUT
```

## Detailed Analysis

### **Column-by-Column Comparison:**

| Position | V.00.03 | V.00.04 | Status | Description |
|----------|---------|---------|--------|-------------|
| 1 | PHASE_NUM | PHASE_NUM | ✅ **Same** | Phase number |
| 2 | PHASE_START | PHASE_START | ✅ **Same** | Phase start time |
| 3 | PHASE_END | PHASE_END | ✅ **Same** | Phase end time |
| 4 | SCENE_NUM | SCENE_NUM | ✅ **Same** | Scene number |
| 5 | LOC_TYPE | SCENE_CONTEXT_COMMENT | ❌ **NEW** | **NEW: Scene context/description** |
| 6 | DIURNAL | LOC_TYPE | ❌ **MOVED** | Location type (moved from pos 5) |
| 7 | LOCATION | DIURNAL | ❌ **MOVED** | Time of day (moved from pos 6) |
| 8 | SPECIFIC AREA | LIGHT_SOURCE(S) | ❌ **NEW** | **NEW: Lighting information** |
| 9 | SHOT_NUM | SEASON | ❌ **NEW** | **NEW: Seasonal information** |
| 10 | MOVE_SPEED | PERIOD | ❌ **NEW** | **NEW: Historical period** |
| 11 | MOVE_TYPE | WEATHER | ❌ **NEW** | **NEW: Weather conditions** |
| 12 | ANGLE | LOCATION | ❌ **MOVED** | Location (moved from pos 7) |
| 13 | SHOT_DESCRIPTION | SPECIFIC AREA | ❌ **MOVED** | Specific area (moved from pos 8) |
| 14 | IN | SHOT_NUM | ❌ **MOVED** | Shot number (moved from pos 9) |
| 15 | OUT | MOVE_SPEED | ❌ **MOVED** | Move speed (moved from pos 10) |
| 16 | - | MOVE_TYPE | ❌ **MOVED** | Move type (moved from pos 11) |
| 17 | - | VIDEO_PROMPT | ❌ **NEW** | **NEW: Video prompt field** |
| 18 | - | ANGLE | ❌ **MOVED** | Angle (moved from pos 12) |
| 19 | - | SHOT_DESCRIPTION | ❌ **MOVED** | Shot description (moved from pos 13) |
| 20 | - | IMAGE_PROMPT | ❌ **NEW** | **NEW: Image prompt field** |
| 21 | - | OREF | ❌ **NEW** | **NEW: Reference field** |
| 22 | - | IN | ❌ **MOVED** | In timecode (moved from pos 14) |
| 23 | - | OUT | ❌ **MOVED** | Out timecode (moved from pos 15) |

## Key Differences

### **🆕 New Columns in V.00.04 (7 new fields):**

1. **`SCENE_CONTEXT_COMMENT`** (Position 5)
   - **Purpose**: Provides narrative context and explanation for each scene
   - **Example**: "This is the establishing shot of the film setting the starting point..."

2. **`LIGHT_SOURCE(S)`** (Position 8)
   - **Purpose**: Specifies lighting conditions and sources
   - **Examples**: "Coral pink sun", "Sunlight through stained church", "Golden sun"

3. **`SEASON`** (Position 9)
   - **Purpose**: Indicates seasonal setting
   - **Examples**: "SUMMER", "SNOWLESS_WINTER", "SNOWY_WINTER"

4. **`PERIOD`** (Position 10)
   - **Purpose**: Historical period classification
   - **Examples**: "LATE_1700S", "EARLY_1800S", "MID_1800S", "EARLY_1900S"

5. **`WEATHER`** (Position 11)
   - **Purpose**: Weather conditions for the scene
   - **Examples**: "CLEAR-SKY", "FOGGY", "OVERCAST", "N/A"

6. **`VIDEO_PROMPT`** (Position 17)
   - **Purpose**: Video generation prompt (currently empty in sample data)

7. **`IMAGE_PROMPT`** (Position 20)
   - **Purpose**: Image generation prompt (currently empty in sample data)

8. **`OREF`** (Position 21)
   - **Purpose**: Reference field (shows TRUE/FALSE values)
   - **Usage**: Appears to indicate important/reference shots

### **🔄 Column Reordering:**

**Major shifts in column positions:**
- **Camera movement data** moved from positions 10-12 to positions 15-18
- **Timecode data** moved from positions 14-15 to positions 22-23
- **Location data** moved from positions 7-8 to positions 12-13

### **📊 Data Structure Impact:**

#### **V.00.03 Structure:**
```
Basic Info → Location → Shot → Camera → Description → Timecode
```

#### **V.00.04 Structure:**
```
Basic Info → Context → Location → Environment → Shot → Camera → Prompts → Timecode
```

## Script Compatibility Analysis

### **⚠️ Compatibility Issues:**

1. **Missing Columns**: V.00.03 doesn't have 7 new columns
2. **Column Position Changes**: All data columns have shifted positions
3. **New Data Types**: Environment and prompt fields are new concepts

### **✅ Compatible Elements:**

1. **Core Identifiers**: PHASE_NUM, SCENE_NUM, SHOT_NUM remain in same positions
2. **Time Data**: PHASE_START, PHASE_END, IN, OUT maintain same data types
3. **Basic Structure**: Hierarchical organization (Phase → Scene → Shot) unchanged

## Recommendations

### **For Script Updates:**

1. **Add New Column Support**: Update data processor to handle new columns
2. **Flexible Column Mapping**: Use column names instead of positions
3. **Backward Compatibility**: Maintain support for V.00.03 format
4. **Enhanced Output**: Consider incorporating new metadata into YAML output

### **For Data Migration:**

1. **Column Mapping**: Create mapping between old and new formats
2. **Default Values**: Provide defaults for missing columns in old format
3. **Validation**: Add validation for required vs optional fields

---

**Analysis Date**: $(date)  
**Status**: ⚠️ Significant format changes detected  
**Action Required**: Script updates needed for full compatibility 