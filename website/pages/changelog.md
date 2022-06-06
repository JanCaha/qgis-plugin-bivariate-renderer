# Changelog

## 0.8.0

- new default color palette when renderer is selected

- new prepared palettes - now there are 12

- new color mixing method multiply

- color mixing methods are renamed, to make them more readble

- Breaking Changes in saving and loading renderer !!! Older projects will not load the renderer correctly. It is unfortunate, but it was necessary to improve the plugin.

- some elements rewritten to make them more readable and maintainable

- legend in layout will now properly update, when the renderer's settings are changed

- new icon for layout item add (with the nice green plus)

- fix error on axis label with underscore, that might not be drawn due to bad text positioning

## 0.7.1

- fix provider error cause by missing export

## 0.7

  - added option to include break values for both axis in legend, with option to style font a specify number precision for each axis

  - added option to rotate texts for y axis clockwise or counter clockwise

  - added text specifying that data are categorized using Equal Interval classification method
  
  - slight refactor of elements position in legend to better work with new options

  - legend preview in Renderer Settings now shows break values in legend

  - renderer has correctly assigned icon in the list of renderers
  
  - fix error in Layout Widget, where attribute names were not correctly into Layout Item when it was created 

  - default style for axis arrow is now stored in separate file, which makes potential changes much simpler

## 0.6

  - add tool to calculate categories as String attribute

  - add tests to ensure better stability of plugin and avoid of unexpected errors

## 0.5

  - Update of the controlling layout widget new options and collapsible boxes

  - axes and axes labels are now optional, does not have to be draw

  - axes labels can now be multiline

## 0.4

  - Implementation of option to rotate legend by 45 degrees

  - Fix wrong default setting for arrows, which did not look good while zooming in the layout 

## 0.3.1

  - Fix bug, where texts were not preserved correctly in legend item (in layout)

## 0.3

  - Major improvements
  
  - Add option to change color mixing method. Replacing default Direct color mixing wit Darken blend color mixing.
    
  - Include set of prepared Bivariate color ramps with option on load them when creating the renderer.
  
  - Legend does not have background anymore.   
  
  - Website created.

## 0.2 

- 0.2.2 Bugfixing making the plugin finally usable.
  
- 0.2.1 Bugfixing.
  
- 0.2.0 First testing version.
