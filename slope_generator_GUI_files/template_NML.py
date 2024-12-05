NML_string = """template template_slopes(x,y) {
    [   0, y, 64, 31, -31,   0, ANIM]
    [  80, y, 64, 31, -31,   0, ANIM]
    [ 160, y, 64, 23, -31,   0, ANIM]
    [ 240, y, 64, 23, -31,   0, ANIM]
    [ 320, y, 64, 31, -31,   0, ANIM]
    [ 400, y, 64, 31, -31,   0, ANIM]
    [ 480, y, 64, 23, -31,   0, ANIM]
    [ 560, y, 64, 23, -31,   0, ANIM]
    [ 640, y, 64, 39, -31,  -8, ANIM]
    [ 720, y, 64, 39, -31,  -8, ANIM]
    [ 800, y, 64, 31, -31,  -8, ANIM]
    [ 880, y, 64, 31, -31,  -8, ANIM]
    [ 960, y, 64, 39, -31,  -8, ANIM]
    [1040, y, 64, 39, -31,  -8, ANIM]
    [1120, y, 64, 31, -31,  -8, ANIM]
    [1200, y, 64, 47, -31, -16, ANIM]
    [1280, y, 64, 15, -31,   0, ANIM]
    [1360, y, 64, 31, -31,  -8, ANIM]
    [1440, y, 64, 31, -31,  -8, ANIM]
}

spriteset(spriteset_INPUTFILE, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "gfx/SPRITESFILE.png") { template_slopes(0,0) }
spriteset(spriteset_INPUTFILE_coast, ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, "gfx/SPRITESFILE.png") { template_slopes(0,50) }
spriteset(spriteset_INPUTFILE_water, "gfx/SPRITESFILE_water.png") { template_slopes(0,0) }
spritelayout layout_INPUTFILE { ground { sprite: spriteset_INPUTFILE(LOAD_TEMP(0)); } }
spritelayout layout_INPUTFILE_coast { 
    ground { sprite: 4061; }
    childsprite { sprite: spriteset_INPUTFILE_coast(LOAD_TEMP(0)); }
    childsprite { sprite: spriteset_INPUTFILE_water(LOAD_TEMP(0)); } }
spritelayout layout_INPUTFILE_menu  { ground { sprite: spriteset_INPUTFILE(0); } }

// check for water class to select coast sprites
switch (FEAT_OBJECTS, SELF, switch_INPUTFILE_coast, [
    (LOAD_TEMP(0) == 0  && nearby_tile_water_class(0, 0))  || // flat
    (LOAD_TEMP(0) == 3  && nearby_tile_water_class(-1, 0)) || // two raised corners
    (LOAD_TEMP(0) == 6  && nearby_tile_water_class(0, -1)) ||
    (LOAD_TEMP(0) == 9  && nearby_tile_water_class(0, 1))  ||
    (LOAD_TEMP(0) == 12 && nearby_tile_water_class(1, 0))  ||
    (LOAD_TEMP(0) == 1  && (nearby_tile_water_class(-1, 0) || nearby_tile_water_class(0, 1)))  || // one raised corner
    (LOAD_TEMP(0) == 2  && (nearby_tile_water_class(-1, 0) || nearby_tile_water_class(0, -1))) ||
    (LOAD_TEMP(0) == 4  && (nearby_tile_water_class(1, 0)  || nearby_tile_water_class(0, -1))) ||
    (LOAD_TEMP(0) == 8  && (nearby_tile_water_class(1, 0)  || nearby_tile_water_class(0, 1)))
]) {
    1: layout_INPUTFILE_coast;
    layout_INPUTFILE;
}

switch (FEAT_OBJECTS, SELF, switch_INPUTFILE, [STORE_TEMP(slope_to_sprite_offset(tile_slope), 0)]) { switch_INPUTFILE_coast; }
switch (FEAT_OBJECTS, SELF, switch_INPUTFILE_view, view) { 0: switch_INPUTFILE; }
switch (FEAT_OBJECTS, SELF, switch_INPUTFILE_menu, view) { 0: layout_INPUTFILE_menu; }

item (FEAT_OBJECTS, obj_INPUTFILE){
    property {
        class:                  " ";
        classname:              string(STR_CLASSNAME);
        name:                   string(STR_NAME);
        climates_available:     ALL_CLIMATES;
        size:                   [1,1];
        build_cost_multiplier:  0;
        remove_cost_multiplier: 0;
        introduction_date:      0x00000000;
        end_of_life_date:       0xFFFFFFFF;
        object_flags:           bitmask(OBJ_FLAG_ANYTHING_REMOVE, OBJ_FLAG_NO_FOUNDATIONS, OBJ_FLAG_ALLOW_BRIDGE, OBJ_FLAG_ON_WATER);
        height:                 0;
        num_views:              1;
    }
    graphics {
        default:    switch_INPUTFILE_view;
        purchase:   switch_INPUTFILE_menu;
        tile_check: return CB_RESULT_LOCATION_ALLOW;
        autoslope:  return CB_RESULT_AUTOSLOPE;
    }
}"""