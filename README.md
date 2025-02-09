

# Vision 
The revision process in the construction industry still heavily relies on the exchange of annotated and commented pdfs. 

Bridge-it aims to bring these annotations and comments back in the 3D model the PDF comes from

# How-to-use
The current version is a POC demonstration export & import of annotated pdfs.
Until a proper UI is implemented, the magic happens in the `PDFIO.py` class : the `main()` method contains two method : `ExecuteExportPDF()` and `ExectureImportPDF()` that can be commented in and out at will. 
Run the script using Rhino's very own "ScriptEditor". Make sure to pip-install the `PyPDF2` package beforehand and check the list of known limitation at the end this page.


# Tech stack
* Rhino for 3D models 
* python for MVP

# Resources 
https://drive.google.com/drive/folders/1fKvYx9CQI1Ge1QQD2Nd4pJelUiMq1YnE?usp=sharing

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


# Known Limitations 
Beyond the flagrant lack of UI, the main problem user could face during utilisation is a feeling of pure joy and bliss which can be intimidating at first.
Minor known limitations includes :

* Model unit needs to be set to millimieter. Scale conflict resolution between page and model is not yet robust enough.
* Tolerance for geometrically matching the annotation to model objects can be tweaked in the `Comment.IntersectionTolerance`. 
* PDF DPi needs to be fixed at 72 DPis for now. 
* pyPDF2 turned out to be a weak choice as it ca only process a limited amount of text in a PDF page. This limitation does not apply to the amount of comments but to the amount of "writing" in the page and prevent us from retrieving our precious "BridgeIt" key. Different PDF importer library has been identified but needs to be implemented. see https://stackoverflow.com/questions/35090948/pypdf2-wont-extract-all-text-from-pdf 