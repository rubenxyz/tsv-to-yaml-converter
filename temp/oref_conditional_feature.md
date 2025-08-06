# Conditional OREF Feature

## Overview

The TSV to YAML converter now implements conditional inclusion of the `oref` field. The `oref` field is only included in the YAML output when the OREF value from the TSV is "TRUE". When the OREF value is "FALSE" or any other value, the `oref` field is completely omitted from the output.

## Behavior Change

### Before (Always Included)
```yaml
- shot_number: 1
  oref: 'FALSE'  # Always included regardless of value
  camera_angle: Crane Shot
  specific_area: Rural settlement
  description: Cozy settlement. Peasants walk along the paths...
```

### After (Conditional)
```yaml
# When OREF = "FALSE" (no oref field)
- shot_number: 1
  camera_angle: Crane Shot
  specific_area: Rural settlement
  description: Cozy settlement. Peasants walk along the paths...

# When OREF = "TRUE" (oref field included)
- shot_number: 10
  oref: 'TRUE'
  camera_angle: Close Up
  description: Two pair of hands are holding a ROYAL_SILVER SEAL_MATRIX.
```

## Implementation Details

### Files Modified

1. **`src/tsv_to_yaml_converter/data_processor.py`**
   - **`_create_shot_data` method**: Modified to conditionally include `oref` only when value is "TRUE"
   - **`_create_shot_model` method**: Updated to handle cases where `oref` might not exist in shot data

### Logic Flow

```python
# In _create_shot_data method
oref_value = row_data.get('OREF')
if oref_value == 'TRUE':
    shot_data['oref'] = oref_value
# If not "TRUE", oref is not added to shot_data

# In _create_shot_model method  
if 'oref' in shot_data:
    shot_kwargs['oref'] = shot_data['oref']
# Only includes oref in model if it exists in shot_data
```

## Benefits

1. **Cleaner Output**: Eliminates redundant `oref: 'FALSE'` entries
2. **Smaller File Size**: Reduces YAML file size by removing unnecessary fields
3. **Better Readability**: Focuses attention on shots that actually have OREF significance
4. **Logical Consistency**: Only shows `oref` when it has meaningful value

## File Size Impact

| Version | File Size | Change |
|---------|-----------|--------|
| **Previous** (with exclusion flags) | **86KB** | Baseline |
| **New** (conditional oref) | **83KB** | **-3KB** (3.5% reduction) |

## Testing Results

- ✅ **All 10/10 tests passing**
- ✅ **Conditional logic working correctly**
- ✅ **No regressions in functionality**
- ✅ **File size reduction achieved**

## Examples from Live Output

### Shots with OREF = "TRUE" (field included)
```yaml
- shot_number: 10
  oref: 'TRUE'
  camera_angle: Close Up
  description: Two pair of hands are holding a ROYAL_SILVER SEAL_MATRIX.

- shot_number: 11
  oref: 'TRUE'
  camera_angle: Wide Shot
  description: GUSTAVIII is holding the ROYAL_SILVER SEAL_MATRIX in front of him...
```

### Shots with OREF = "FALSE" (field omitted)
```yaml
- shot_number: 1
  camera_angle: Crane Shot
  specific_area: Rural settlement
  description: Cozy settlement. Peasants walk along the paths...

- shot_number: 13
  camera_angle: Close Up
  specific_area: Work bench
  description: With his back towards us, sitting in the center of the workshop...
```

## Backward Compatibility

- ✅ **Existing functionality preserved**
- ✅ **All other fields work as before**
- ✅ **Exclusion flags still work correctly**
- ✅ **No breaking changes to API**

## Future Considerations

This pattern could be extended to other boolean fields if needed:
- `image_prompt` (only if not null/empty)
- `specific_area` (only if not null/empty)
- Other conditional fields based on business logic

The implementation provides a clean, maintainable approach for conditional field inclusion. 