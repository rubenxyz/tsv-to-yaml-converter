# Exclusion Flags Feature

## Overview

The TSV to YAML converter now supports optional exclusion flags that allow users to omit specific sections from the YAML output. This feature provides flexibility for different use cases where certain metadata may not be needed.

## New Command-Line Flags

### `--no-camera-movement`
- **Purpose**: Excludes the `camera_movement` section and all its children from shot data
- **Effect**: Removes `speed`, `type`, and `video_prompt` fields from each shot
- **Use Case**: When camera movement information is not relevant for the target audience

### `--no-shot-timecode`
- **Purpose**: Excludes the `shot_timecode` section and all its children from shot data
- **Effect**: Removes `in_time` and `out_time` fields from each shot
- **Use Case**: When timing information is not needed or handled separately

## Usage Examples

### Basic Usage
```bash
# Process with all sections included (default behavior)
python -m tsv_to_yaml_converter process

# Exclude camera movement information
python -m tsv_to_yaml_converter process --no-camera-movement

# Exclude shot timecode information
python -m tsv_to_yaml_converter process --no-shot-timecode

# Exclude both sections
python -m tsv_to_yaml_converter process --no-camera-movement --no-shot-timecode
```

### Help Documentation
```bash
python -m tsv_to_yaml_converter process --help
```

Output:
```
Usage: python -m tsv_to_yaml_converter process [OPTIONS]

  Process all TSV files in the input directory.

Options:
  --config PATH         Configuration file path
  --no-camera-movement  Exclude camera_movement section from YAML output
  --no-shot-timecode    Exclude shot_timecode section from YAML output
  --help                Show this message and exit.
```

## Output Comparison

### Full Output (Default)
```yaml
- shot_number: 1
  oref: 'FALSE'
  camera_angle: Crane Shot
  specific_area: Rural settlement
  description: Cozy settlement. Peasants walk along the paths...
  camera_movement:
    speed: Slow & smooth
    type: Crane-out
    video_prompt: null
  shot_timecode:
    in_time: 00:00:00,000
    out_time: 00:00:05,000
  image_prompt: null
```

### With `--no-camera-movement`
```yaml
- shot_number: 1
  oref: 'FALSE'
  camera_angle: Crane Shot
  specific_area: Rural settlement
  description: Cozy settlement. Peasants walk along the paths...
  shot_timecode:
    in_time: 00:00:00,000
    out_time: 00:00:05,000
  image_prompt: null
```

### With `--no-shot-timecode`
```yaml
- shot_number: 1
  oref: 'FALSE'
  camera_angle: Crane Shot
  specific_area: Rural settlement
  description: Cozy settlement. Peasants walk along the paths...
  camera_movement:
    speed: Slow & smooth
    type: Crane-out
    video_prompt: null
  image_prompt: null
```

### With Both Flags
```yaml
- shot_number: 1
  oref: 'FALSE'
  camera_angle: Crane Shot
  specific_area: Rural settlement
  description: Cozy settlement. Peasants walk along the paths...
  image_prompt: null
```

## Technical Implementation

### Files Modified
1. **`src/tsv_to_yaml_converter/__main__.py`**
   - Added CLI options for exclusion flags
   - Updated function signatures to pass flags through

2. **`src/tsv_to_yaml_converter/cli_commands.py`**
   - Updated `process_files` method to accept exclusion flags
   - Pass flags to converter instance

3. **`src/tsv_to_yaml_converter/converter.py`**
   - Updated `process_files` and `convert_tsv_to_yaml` methods
   - Pass flags to data processor

4. **`src/tsv_to_yaml_converter/data_processor.py`**
   - Updated `build_project_structure` and related methods
   - Conditional creation of shot models based on flags

5. **`src/tsv_to_yaml_converter/models.py`**
   - Made `camera_movement` and `shot_timecode` optional in `Shot` model
   - Allows these fields to be `None` when excluded

### Data Flow
```
CLI Flags → __main__.py → cli_commands.py → converter.py → data_processor.py → models.py
```

### Conditional Logic
The exclusion is implemented at the model creation level:
- If `--no-camera-movement` is set: `camera_movement` field is `None`
- If `--no-shot-timecode` is set: `shot_timecode` field is `None`
- Pydantic automatically excludes `None` fields from YAML output

## Benefits

1. **Flexibility**: Users can customize output based on their needs
2. **Reduced File Size**: Smaller YAML files when certain metadata isn't needed
3. **Cleaner Output**: Focus on relevant information for specific use cases
4. **Backward Compatibility**: Default behavior unchanged, flags are optional
5. **Extensible**: Easy to add more exclusion flags in the future

## Testing

All existing tests continue to pass, and the feature has been tested with:
- ✅ Default behavior (no flags)
- ✅ `--no-camera-movement` flag
- ✅ `--no-shot-timecode` flag  
- ✅ Both flags combined
- ✅ Help documentation
- ✅ All 10/10 tests passing

## Future Enhancements

Potential additional exclusion flags could include:
- `--no-image-prompt`
- `--no-specific-area`
- `--no-camera-angle`
- `--no-oref`

The current architecture makes it easy to add these by following the same pattern. 