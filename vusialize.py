#this part is assuming that comment information is extracted

#def -->get guid of object
#get the layer 
#change the colour 
#redraw on layer
#get guid of object
#============================================
#Imports
#============================================
import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs
import sys
from ClassComment import Comment





#import comment

#=============================================
#load comments (text objects) from layer
#=============================================

#load text dot
def get_objects_from_layer(layer_name):
    """Returns a list of object IDs from a given layer."""
    if not rs.IsLayer(layer_name):
        print(f"Layer '{layer_name}' does not exist.")
        return []
    
    obj_ids = rs.ObjectsByLayer(layer_name)  
    return obj_ids if obj_ids else []

#create text dot

# Example usage
if __name__ == '__main__':
    pass
    #here we select text dot
    # layer_name = "bridge_it_comments"
    # objects = get_objects_from_layer(layer_name)
    #comment sample
    





#get guid of objects and add display 

    #create text dots
    #print dots onto layer
    #display pipeline

# #function to unload commenter
# def on_select(sender, e):
#     """Callback function triggered when an object is selected."""
#     for rh_obj in e.RhinoObjects:
#         if rs.IsPolysurface(rh_obj.Id):  # Check if the selected object is a Brep
#         #here call a new function to load the attributes
#             guid = str(rh_obj.Id)
#             #check if guid == guid from comment list (this could be a function)
#                 #if true the show dialog box with
#                 #comment.source_file
#                 #comment.created_date
#                 #comment.
#             Rhino.UI.Dialogs.ShowMessageBox(f"GUID: {guid}", "Brep Information")

# def enable_selection_listener():
#     """Enables the object selection event listener."""
#     sc.doc.SelectObjects += on_select
#     print("Brep selection listener is running...")

# main

# enable_selection_listener()
