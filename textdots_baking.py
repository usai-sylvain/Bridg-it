import Rhino
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
from datetime import datetime

def select_object(name):
    message = "Select %s" % name
    obj_id = rs.GetObject(message)
    return obj_id  # Return the object ID instead of Brep

def main():

    class Comment(object):
        def __init__(self, SourceFileName=None, SourceFileCreationDate=None, Author = None, Text=None,Point3d=None, ConnectedElementGuid=None, ConnectedElementName=None):
            
            self.SourceFileName = SourceFileName
            self.SourceFileCreationDate = SourceFileCreationDate
            self.ImportDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.Author = Author
            self.Text = Text
            self.Point3d=Point3d
            self.ConnectedElementGuid = ConnectedElementGuid
            self.ConnectedElementName = ConnectedElementName
            
        def SetSourceFileName(self, value):
            self.SourceFileName = value
        
        def SetSourceFileCreationDate(self, value):
            self.SourceFileCreationDate = value
        
        def SetImportdate(self):
            self.Importdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        def SetAuthor(self, value):
            self.Author = value
        
        def SetText(self, value):
            self.Text = value
        
        def SetPoint3d(self, value):
            self.Point3d = value
        
        def SetConnectedElementGuid(self, value):
            self.ConnectedElementGuid = value
        
        def SetConnectedElementName(self, value):
            self.ConnectedElementName = value
    
    #create dummy commentlist
    list_comments = []
    
    for i in range(2):
        point_test_id = select_object("point")
        point_test = rs.PointCoordinates(point_test_id)
        print(point_test)
        print(type(point_test))
        comment = Comment("SourceFileName", "SourceFileCreationDate", "Author", "Text", point_test, " ", " ")
        list_comments.append(comment)
#    
#    surface_test = select_object("surface")

    check_main_layer("pdf_markups")  # Check or create main layer
    create_sublayer("pdf_markups", datetime.now().strftime("%Y%m%d") + " PDF")  # Create a sublayer

    for comment in list_comments:
        create_textdots(comment)

def check_main_layer(layer_name, color=(0, 255, 0)):  # Default green color
    """Checks if the main layer exists; if not, creates it."""
    existing_layers = rs.LayerNames()
    
    # Check if the layer exists
    if existing_layers and layer_name in existing_layers:
        print("Layer '{}' already exists.".format(layer_name))
    else:
        # Create the new layer with a green color
        rs.AddLayer(layer_name, color, locked=False)
        print("Layer '{}' created with color {}.".format(layer_name, color))

def create_sublayer(parent_layer, sublayer_name, color=(255, 0, 0)):  # Default red color
    """Creates a sublayer under the specified parent layer."""
    
    # Ensure the parent layer exists
    if not rs.IsLayer(parent_layer):
        print("Error: Parent layer '{}' does not exist.".format(parent_layer))
        return None
    
    # Unlock the parent layer if it's locked
    if rs.IsLayerLocked(parent_layer):
        rs.UnlockLayer(parent_layer)

    # Properly format the sublayer name
    full_sublayer_name = "{}::{}".format(parent_layer, sublayer_name)
    
    # Check if the sublayer already exists
    if rs.IsLayer(full_sublayer_name):
        print("Sublayer '{}' already exists.".format(full_sublayer_name))
    else:
        # Create the sublayer under the parent layer
        rs.AddLayer(name=sublayer_name, color=color, locked=False, parent=parent_layer)
        rs.AddLayer(name="markups", color=color, locked=False, parent=sublayer_name)
        rs.AddLayer(name="pdf_image", color=color, locked=False, parent=sublayer_name)
        print("Sublayer '{}' created under '{}' with color {}.".format(full_sublayer_name, parent_layer, color))

def create_textdots(comment):
    """Creates a TextDot with the given text at the specified location."""
    if comment.Point3d:
        textdot = rs.AddTextDot(comment.Text, comment.Point3d)
        create_attributes(textdot, comment)
        if textdot:
            print("TextDot '{}' created at {}".format(comment.Text, comment.Point3d))
        else:
            print("Failed to create TextDot.")
    else:
        print("Invalid location for TextDot.")
        
def create_attributes(textdot, comment):
    obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(textdot)
    obj.Attributes.SetUserString("SourceFileName", comment.SourceFileName)
    obj.Attributes.SetUserString("SourceFileCreationDate", comment.SourceFileCreationDate)
    obj.Attributes.SetUserString("ImportDate", comment.ImportDate ) 
    obj.Attributes.SetUserString("Author", comment.Author)
    obj.Attributes.SetUserString("ConnectedElementGuid", comment.ConnectedElementGuid) 
    obj.Attributes.SetUserString("ConnectedElementName", comment.ConnectedElementName) 
    obj.CommitChanges()

main()