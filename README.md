# Slope Generator

## What it is

An interactive tool for _generating slope sprites_ that can be used as ground spritesets in NewGRF development.  
The app also offers the option to create an _NML template_, which contains the code that makes a ground with auto-slope work (even for shores).  
It is highly recommended to take advantage of it.

![App](/_readme/default.png)


## How to use it

### Step 1

Prepare an image with a _flat ground tile_.  
It doesn't have to be paletted, the resulting series of sprites will be 32 bpp anyway.  
However, the _background_ has to be one of these three options:

1) **Blue**: `rgb(0, 0, 255)`
2) **White**: `rgb(255, 255, 255)`
3) **Transparent**: `rgb(0, 0, 0, 0)`

![01](/_readme/01.png)


### Step 2

Run the app.
1) Press "_Open file..._" to find and select your ground tile.
2) Use the three sliders to adjust the brightness of lights, the darkness of shadows and, optionally, to add gridlines.
3) Check the preview window to have an idea of the final look.

![02](/_readme/02.png)

4) Press "_Export sprites..._" to save the result. This will export **two PNG files**:  
    32 bpp ground sprites + 8 bpp animated water sprites. Both should be used in the **gfx** folder of your project.

![03](/_readme/03.png)

5) Press "_Save NML template..._" to create a text file with a code snippet that you can **paste** into your NewGRF code.

![04](/_readme/04.png)

**Note**: Keep in mind that the NML code is a template, so some adjustments may be needed.  
It will insert the filenames you entered in "_Export sprites..._", but make sure to adapt the object's properties to your needs  
(i.e. _class_, _classname_, _name_, _num_views_).


### Step 3

After adding the sprites into the **gfx** folder and pasting (and editing) the **NML code**, you should be able to compile your NewGRF and test it in a game.  
The result should be a shore-sensitive ground object with auto-slope.

![05](/_readme/05.png)

<br>

## Author & License

Created by: **chujo**  
@chujo on OpenTTD's Discord ([discord.gg/openttd](https://discord.gg/openttd))

This project is licensed under the [GNU General Public License v2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).


