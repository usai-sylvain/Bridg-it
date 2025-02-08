import Rhino
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
from datetime import datetime

def select_object(name):
    message = "Select %s" % name
    obj_id = rs.GetObject(message)
    return obj_id  # Return the object ID instead of Brep

def select_objects(name):
    message = "Select %s" % name
    obj_ids = rs.GetObjects(message)
    return obj_ids if obj_ids else []  # Return list of IDs

def get_surface_normal(surface):
    #surface = rs.coercebrep(surface_id)  # Convert ID to Brep
    if surface:
        centroid = rs.SurfaceAreaCentroid(surface)
        if centroid:
            centroid_point = centroid[0]  # Extract Point3d
            param = rs.SurfaceClosestPoint(surface, (centroid_point.X, centroid_point.Y, centroid_point.Z))
            if param:
                return rs.SurfaceNormal(surface, param)
    return None

def create_normal_line(point, normal):
    if normal:
        normal_scaled = rs.VectorScale(normal,999999)
        reversed_normal = rs.VectorReverse(normal_scaled)
        end_point = rs.PointAdd(point, reversed_normal)
        return Rhino.Geometry.LineCurve(point, end_point)


def intersect_normal_brep(all_elements, normal_line_id, point):
    """Finds the closest intersection point between a normal line and a set of Breps."""
    closest_point = None
    closest_distance = float("inf")
    closest_element = None

    tolerance = 0.01  # Small positive tolerance for intersection

    for element_id in all_elements:
        element_brep = rs.coercebrep(element_id)
        if not element_brep:
            continue  # Skip invalid Breps

        normal_line = rs.coercecurve(normal_line_id)
        if not normal_line:
            continue  # Skip invalid curve

        # Perform intersection
        intersections = Rhino.Geometry.Intersect.Intersection.CurveBrep(normal_line, element_brep, tolerance)

        # Ensure the intersection result is valid and contains intersection points
        if not intersections or len(intersections) < 3 or not intersections[2]:
            continue  # Skip if no valid intersection points

        try:
            # Check all intersection points and find the closest one
            closest_point_i = None
            closest_distance_i = float("inf")

            for point_intersection in intersections[2]:  # Loop over intersection points
                distance = rs.Distance(point, point_intersection)
                if distance < closest_distance_i:
                    closest_distance_i = distance
                    closest_point_i = point_intersection  # Store closest point for this element

            # Compare with global closest point
            if closest_distance_i < closest_distance:
                closest_distance = closest_distance_i
                closest_point = closest_point_i
                closest_element = element_id  # Store object ID

        except Exception as e:
            print("Error processing intersections")
            continue  # Move to the next element instead of exiting the function

    # Return the closest element ID and intersection point
    return [closest_element, closest_point] if closest_element else None

def match_markup_element(surface, list_comments):
    
#    plane_id = select_object("PLANE")
#    if not plane_id:
#        print("No plane selected.")
#        return

#    markups_obj = rs.GetObjects("Select MARKUPS point", rs.filter.point)
#    if not markups_obj:
#        print("No markups point selected.")
#        return
#    markups = []
#    for i in markups_obj:
#        markups.append(rs.PointCoordinates(i))

    all_elements = select_objects("ALL ELEMENTS")
    if not all_elements:
        print("No elements selected.")
        return

    
    surface_normal = get_surface_normal(surface) #evaluate per point if plane is curved
    if not surface_normal:
        print("Could not determine surface normal.")
        return
        

    for comment in list_comments:
        point = comment.Point3d

        normal_line = create_normal_line(point, surface_normal)
#        print(normal_line)

        closest_element_id = intersect_normal_brep(all_elements, normal_line, point)
        if closest_element_id:
            print("Closest element ID:", closest_element_id[0])
            print("Point Closest element:", closest_element_id[1])
            rs.AddPoint(closest_element_id[1])
            comment.SetConnectedElementGuid(closest_element_id[0])
            comment.SetPoint3d(closest_element_id[1])
            comment.SetConnectedElementName(rs.ObjectName(closest_element_id[0]))
        else:
            pass
            #print("No changes to class comment made.")


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
    
    
    list_comments = []
    
    for i in range(3):
        point_test_id = select_object("point")
        point_test = rs.PointCoordinates(point_test_id)
        print(point_test)
        print(type(point_test))
        comment = Comment("SourceFileName", "SourceFileCreationDate", "Author", "Text", point_test, None, None)
        list_comments.append(comment)
    
    surface_test = select_object("surface")
    
    
    match_markup_element(surface_test, list_comments)
    
    for comment in list_comments:
#        print("Point: ", comment.Point3d)
#        print("connectec GUID: ", comment.ConnectedElementGuid)

main()
