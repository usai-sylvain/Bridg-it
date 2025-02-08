

# Vision 
The revision process in the construction industry still heavily relies on the exchange of annotated and commented pdfs. 

Bridge-it aims to bring these annotations and comments back in the 3D model the PDF comes from

# Tech stack
* Rhino for 3D models 
* python for MVP

# Roadmap

## prepare test case
* 3d model
* 
## Export PDF from Rhino with coordinate system marker 
* identify the coordinate system of the view plane used for the pdf export.
* identify the scale.
* hash the coordinate system and scale and store them in the pdf.

## Import and orient PDFs 
* identify our hashed markers in existing pdfs
* orient and scale the pdf in 3D space

## Store Guid of rhino object in the pdf ?
* can we store Rhino Guids in the pdf drawing.

## Identify comments and annotations objects from the pdf 
* what is a comment object ? 
* what is an annotation object ?
* can we retrieve their relative coordinates in page space ?
* import the comments as text dots in rhino 
	* data structure (layer, user text, name, color to be defined)
		* pdf name 
		* date of import 

## Identify the closest geometry from the comment
* use closest point to identify elements that this comment belongs to 
* user input might be required in case of uncertainty 
	* define a distance threshold
	* if more than one objects are within the threshold, ask user for confirmation
* visualise comments per geometry

## warn user if the source pdf has been updated
* upon rhino or plugin start, find our comment annotation and warn user if one of them comes from a pdf that has been modified since it was imported.
* might need an actual Rhino plugin.

## Package into .net plugin

# Further steps / discussions

## Status management
* accept/reject issues from rhino and update it in the pdf accordingly.
