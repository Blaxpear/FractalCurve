# Fractal Curve

Python program for generating and animating recursively drawn line fractals,

## Getting Started

The fractal is defined by the root shape and a floating point number called stage parameter. The integer part of the stage parameter tells how many full recursions of the root shape to draw. What ever decimals remains after the integer part defines the stage of the last or "top" shapes in the fractal. 

Stage of a shape is between 0 and 1. 0 stage is the first formation of vertices  to draw when stage has passed a whole number or in other words new shapes start to emerge. 1 corresponds to shape being fully drawn and the shape is ready to draw next shapes onto its lines. Between 0 and 1 the the shape transitions linearly from zero shape to full shape.

Shapes consist of vertices, links, and visuals. Vertices have two positions; zero shape position and full shape position. Vertices will move linearly from zero to full position as the stage of the shape changes from 0 to 1. Links are connections between vertices that will draw their parent shape between their two vertices once the stage of the shape is greater than 1. Visuals are just lines between vertices and will not recursively draw their parent shape like Links.

The shape that the program draws is defined in a shape (regular text) file. The file contains rows that start with a command and after that come command specific parameters. 

Example file defining a square that has no bottom line:
```
vertex: 0, 0
vertex: 0, 10
vertex: 10, 10
vertex: 10, 0

start: first
end: last

link: 1; 2; 0; 0
link: 2; 3; 0; 0
link: 3; 4; 0; 0
```
#### Commands definitions:
###### Vertex
The basic building block of every shape. Vertex position is defined by the stage of the shape. The position moves linearly from zero shape position to full shape position as the stage changes from 0 to 1. If the stage is over 1, it is treated as if it was 1.
```
Vertex: x, y (; x0, y0)
```
- full shape position
    - x, y: (float, float)
- zero shape position (when stage is zero)
    - x0, y0: (float, float) (optional) 
    - if omitted, the zero shape positions will be equally distributed along a line between first and last vertex
###### Start & End
These commands define the length of the shape by measuring the distance of a straight line from start to end vertex. When a shape is recursively drawn onto a line, it is scaled so that the length of the shape matches length of the line.
```
Start: i
```
- i: (int or "first") shape starting vertex index or if set to "first", starting vertex will be defined as the first vertex declared
```
End: i
```
- i: (int or "last") shape ending vertex index or if set to "last", ending vertex will be defined as the last vertex declared.
###### Link
The other core element of each shape. When the stage of the shape is between 0 and 1, the link will be drawn just as a line between two vertices. After the stage goes beyond 1, the link will start to draw the next shape onto itself.

<b>The vertices referred by links as well as start and end must be defined before defining links.</b>
```
Link: i; j; mx; my
```
- Vertex indices
    - i: (int) index (starting from 1) of the first vertex of this link. 
    - j: (int) index of the second vertex
- Mirroring parameters
    - mx: (boolean) if set to "1" mirror the next shape that will be drawn on this link along x-axis
    - my: (boolean) mirror y-axis

###### Visual
A simple visual line, that will not draw another shape onto itself even after the stage surpasses 1.
```
Visual: i; j
```
- Vertex indices
    - i: (int) index of the first vertex 
    - j: (int) index of the second vertex

###### Link All
This command defines links between all (except between last and first vertex) vertices in the order they were declared. Most of the time this command is all you need to achieve what you want.

This command also defines a link mirroring pattern. If the link number (first link is one and so on) is divisible by nx or ny, it will be mirrored along x- or y-axis respectively. If the integer nx or ny is negative, the link will be mirrored always when the link number is NOT divisible. 
```
Link all: nx; ny
```
- nx: x-mirroring pattern
- ny: y-mirroring pattern

###### Comments
Any row that does not start with a command, is treated as a comment.
