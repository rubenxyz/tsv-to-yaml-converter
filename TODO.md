# TODO: Simple TSV to YAML Converter for Hierarchical Data

## Overview
Modify the existing converter to handle the V.00.02.ISOF.tsv file and output YAML matching the jewish_sweden_shotlist_yaml.yml format.

## Simple Implementation Plan

### 1. Analyze the Data Structure
- [x] Examine V.00.02.ISOF.tsv structure (done)
- [x] Examine expected YAML output format (done)
- [x] Document the field mappings needed
- [ ] Provide user with refactoring and cleanup candidates

### 2. Modify the Converter
- [x] Update converter.py to handle hierarchical grouping (EPOCH → SCENE → SHOT)
- [x] Add field mappings for the specific TSV columns
- [x] Handle empty fields as null in YAML output
- [x] Ensure proper YAML formatting and indentation
- [x] Provide user with refactoring and cleanup candidates

### 3. Test and Validate
- [ ] Test with V.00.02.ISOF.tsv file
- [ ] Compare output with expected YAML format
- [ ] Fix any formatting issues
- [ ] Verify all data is preserved correctly
- [ ] Provide user with refactoring and cleanup candidates

### 4. Code Review
- [x] Review code and prompt user to review list of *.py files in codebase that could be candidates for refactoring
- [x] Review code and prompt user to review list of *.py files in codebase that could be candidates for being moved to the macOS dust bin

## Field Mappings Needed
```
EPOCH_NUM → project.epochs[].epoch_number
EPOCH_START → project.epochs[].time_period.start
EPOCH_END → project.epochs[].time_period.end
SCENE_NUM → project.epochs[].scenes[].scene_number
LOC_TYPE → project.epochs[].scenes[].location_type
TIME → project.epochs[].scenes[].time
LOCATION → project.epochs[].scenes[].location
SPECIFIC_AREA → project.epochs[].scenes[].shots[].specific_area
SHOT_NUM → project.epochs[].scenes[].shots[].shot_number
IN → project.epochs[].scenes[].shots[].shot_timecode.in
OUT → project.epochs[].scenes[].shots[].shot_timecode.out
MOVE_SPEED → project.epochs[].scenes[].shots[].camera_movement.speed
MOVE_TYPE → project.epochs[].scenes[].shots[].camera_movement.type
ANGLE → project.epochs[].scenes[].shots[].angle
SHOT_DESCRIPTION → project.epochs[].scenes[].shots[].description
```

## Success Criteria
- [ ] Converter processes V.00.02.ISOF.tsv successfully
- [ ] Output matches jewish_sweden_shotlist_yaml.yml format
- [ ] All data is preserved correctly
- [ ] Empty fields are handled as null

## Notes
- **Complexity**: Low-Medium - just need to group data and map fields
- **Timeline**: 2-4 hours, not days
- **Approach**: Modify existing converter, no need for new architecture
- **Focus**: Simple, working solution over enterprise patterns 