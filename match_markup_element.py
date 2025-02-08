import Rhino
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs

def select_object(name):
    message = "Select %s" % name
    obj_id = rs.GetObject(message)
    return obj_id  # Return the object ID instead of Brep

def select_objects(name):
    message = "Select %s" % name
    obj_ids = rs.GetObjects(message)
    return obj_ids if obj_ids else []  # Return list of IDs

def get_plane_normal(plane_id):
    plane = rs.coercebrep(plane_id)  # Convert ID to Brep
    if plane:
        centroid = rs.SurfaceAreaCentroid(plane)
        if centroid:
            centroid_point = centroid[0]  # Extract Point3d
            param = rs.SurfaceClosestPoint(plane, (centroid_point.X, centroid_point.Y, centroid_point.Z))
            if param:
                return rs.SurfaceNormal(plane, param)
    return None

def create_normal_line(markup, normal):
    if normal:
        normal_scaled = rs.VectorScale(normal,999999999 )
        reversed_normal = rs.VectorReverse(normal_scaled)
        end_point = rs.PointAdd(markup, reversed_normal)
        return Rhino.Geometry.LineCurve(markup, end_point)

def intersect_normal_brep(all_elements, normal_line_id, markup):
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

            for point in intersections[2]:  # Loop over intersection points
                distance = rs.Distance(markup, point)
                if distance < closest_distance_i:
                    closest_distance_i = distance
                    closest_point_i = point  # Store closest point for this element

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

def match_markup_element(surface, list_comment:list): --> list
    
#    plane_id = select_object("PLANE")
#    if not plane_id:
#        print("No plane selected.")
#        return

    markups_obj = rs.GetObjects("Select MARKUPS point", rs.filter.point)
    if not markups_obj:
        print("No markups point selected.")
        return
    markups = []
    for i in markups_obj:
        markups.append(rs.PointCoordinates(i))

    all_elements = select_objects("ALL ELEMENTS")
    if not all_elements:
        print("No elements selected.")
        return

    plane_normal = get_plane_normal(plane_id)
    if not plane_normal:
        print("Could not determine plane normal.")
        return
    
    plane_id = surface 
    
    
    for markup in markups:
        normal_line = create_normal_line(markup, plane_normal)
#        print(normal_line)

        closest_element_id = intersect_normal_brep(all_elements, normal_line, markup)
        if closest_element_id:
            print("Closest element ID:", closest_element_id[0])
            print("Point Closest element:", closest_element_id[1])
            rs.AddPoint(closest_element_id[1])
        else:
            print("No intersection found.")

main()
