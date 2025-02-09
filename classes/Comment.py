from datetime import datetime
import PyPDF2 as pdf
import rhinoscriptsyntax as rs
import Rhino 
import Rhino.Geometry as rg


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
        self.RhinoID = None
        self.IntersectionTolerance = 500.0

    def SetRhinoID(self, value):
        self.RhinoID = value
    
    def GetRhinoID(self):
        """retrieve the rhino ID of the text dot representing this comment in the model """
        return self.RhinoID
    
        
    
        
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
    

    @classmethod
    def CreateRootLayer(cls, layer_name, color=(0, 255, 0)):  # Default green color
        """Checks if the main layer exists; if not, creates it."""
        existing_layers = rs.LayerNames()
        
        # Check if the layer exists
        if existing_layers and layer_name in existing_layers:
            # already exists, nothing to do
            # print("Layer '{}' already exists.".format(layer_name))
            return 
        else:
            # Create the new layer with a green color
            rs.AddLayer(layer_name, color, locked=False)
            print("Layer '{}' created with color {}.".format(layer_name, color))

    @classmethod
    def CreateSublayers(cls, parent_layer, sublayer_name, color=(255, 0, 0)):  # Default red color
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
            # nothing to do 
            # print("Sublayer '{}' already exists.".format(full_sublayer_name))
            return
        else:
            # Create the sublayer under the parent layer
            rs.AddLayer(name=sublayer_name, color=color, locked=False, parent=parent_layer)
            rs.AddLayer(name="markups", color=color, locked=False, parent=sublayer_name)
            rs.AddLayer(name="pdf_image", color=color, locked=False, parent=sublayer_name)
            print("Sublayer '{}' created under '{}' with color {}.".format(full_sublayer_name, parent_layer, color))

    def BakeMarkup(self):
        """Creates a TextDot with the given text at the specified location."""
        if self.Point3d:
            textdotID = rs.AddTextDot(self.Text, self.Point3d)
            self.SetRhinoID(textdotID)

            self.BakeAttributes()
            if textdotID:
                print("TextDot '{}' created at {}".format(self.Text, self.Point3d))
            else:
                print("Failed to create TextDot.")
        else:
            print("Invalid location for TextDot.")
            
    def BakeAttributes(self):
        """set the userText to the comment rhino object

        Args:
            textdot (_type_): _description_
            comment (_type_): _description_
        """
        obj = self.GetRhinoID()

        obj.Attributes.SetUserString("SourceFileName", self.SourceFileName)
        obj.Attributes.SetUserString("SourceFileCreationDate", self.SourceFileCreationDate)
        obj.Attributes.SetUserString("ImportDate", self.ImportDate ) 
        obj.Attributes.SetUserString("Author", self.Author)
        obj.Attributes.SetUserString("ConnectedElementGuid", self.ConnectedElementGuid) 
        obj.Attributes.SetUserString("ConnectedElementName", self.ConnectedElementName) 
        obj.CommitChanges()    
        
    def MatchMarkupWithModelGeometry(self, geometryIds, pdfSourcePlane):
        """Finds the closest intersection point between a normal line and a set of Breps.
        Search Tolerance is 50 cm '\_(--')_/' """
        closest_point = None
        closest_distance = float("inf")
        closest_element = None

        point = self.Point3d
        normalVector = pdfSourcePlane.ZAxis * -1

        viewPlane = rg.Plane(point, normalVector)

        for id in geometryIds:
            brep = rs.coercebrep(id)
            if not brep:
                continue  # Skip invalid Breps

            # Perform intersection
            intersections = Rhino.Geometry.Intersect.Intersection.ProjectPointsToBreps([point], [brep], normalVector, self.IntersectionTolerance)

            # Ensure the intersection result is valid and contains intersection points
            if not intersections:
                continue  # Skip if no valid intersection points


            distances = [] 
            positivePoints = [] 
            for intersection in intersections :
                    # project the result intersection on the brep (this is necessary because of the search threshold)
                    dist = viewPlane.DistanceTo(intersection) 
                    if dist > 0 : 
                        distances.append(dist)
                        positivePoints.append(intersections)
                            
            distances, positivePoints = zip(*sorted(zip(distances, positivePoints)))
            bestPoint = positivePoints[0]
            bestDistance = distances[0]

            # Compare with global closest point
            if bestDistance < closest_distance:
                closest_distance = bestDistance
                closest_point = bestPoint
                closest_element = id  # Store object ID

            # except Exception as e:
            #     print("Error processing intersections")
            #     continue  # Move to the next element instead of exiting the function

        if closest_point :
            # set the attributes according to the matched brep 
            self.SetConnectedElementGuid(closest_element)
            self.SetPoint3d(closest_point)
            self.SetConnectedElementName(rs.ObjectName(closest_element))



