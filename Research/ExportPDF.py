import rhinoscriptsyntax as rs 
import Rhino 
import scriptcontext 
from scriptcontext import doc
import System 
import Rhino.Geometry as rg



def Execute():
    exporter = PDFExporter()
 
    exporter.Sandbox()
    
    # exporter.Export()

class PDFExporter(object):

    def __init__(self):
        # check requirements 
        if Rhino.RhinoDoc.ActiveDoc.ModelUnitSystem != Rhino.UnitSystem.Millimeters : 
            print("ExportPDF.Warning : model unit is not in mm !")

    def Sandbox(self):
        # get all view pages 
        page = self.GetAllPageViews()[0]
        
        detailViews = page.GetDetailViews()
        print detailViews
        detailView = detailViews[0]
        self.DEBUG_3dSpaceToPage(detailView)

        

        # rs.AddPlaneSurface(coordinate, 500, 500)

    def Export(self):

        # get a target path for our padf
        exportPath = self.GetExportPath()
        if not exportPath :
            print("User aborted PDF export")
            return
        
        
        # create a new instance of RhinoPDF exporter
        pdf = Rhino.FileIO.FilePdf.Create()

        newPage = "create a new page here"
        
        pdf.AddPage(newPage)
        pdf.Write(exportPath)


    def GetAllPageViews(self):
        return Rhino.RhinoDoc.ActiveDoc.Views.GetPageViews()
    
    def GetAllPageNames(self):
        return [p.PageName for p in self.GetAllPageViews()]
    
    def GetPageCornersFromDetailView(self, detailViewObject):
        """retrieve the page this detial is on and return all 4 page corners in 3D model space.

        Args:
            detailViewObject (DetailViewObject): a detail view

        Returns:
            List<rg.Point3d> : a list of point 3d : Lower Left, Lower Right, TopRight, TopLeft
        """
        # retrieve the viewport 
        viewport = detailViewObject.Viewport

        # get the Camera plane from the viewport
        cameraPlane = self.GetRhinoViewportCameraPlane(viewport)
        scale = self.GetDetailToModelScale(detailViewObject)
        
        rhinoPageView = self.GetPageViewFromDetailView(detailViewObject)
        # get the page size 
        width = rhinoPageView.PageWidth
        height = rhinoPageView.PageHeight
        
                
        realWidth = width   * scale 
        realHeight = height * scale 

        # create a debug surface 
        pageRectangle = rg.Rectangle3d(cameraPlane, rg.Interval(-realWidth * 0.5, realWidth * 0.5), rg.Interval(-realHeight * 0.5, realHeight * 0.5))
        corners = [pageRectangle.Corner(i) for i in range(4)]
        return corners
    
    def CreatePagePlaneFromPageCorner(self, pageCorners):
        """Return a plane created from the page corners. 
        Assuming that : 
        Corner0 is the lower left (origin of the plane)
        Corner1 is the lower right (XAxis of the plane)
        corner3 (!not 2!) is the top left corner (YAxis of the page)
        """
        origin = pageCorners[0]
        xAxis = pageCorners[1] - origin
        yAxis = pageCorners[3] - origin 
        pagePlane = rg.Plane(origin, xAxis, yAxis)
        return pagePlane
    
    def DEBUG_3dSpaceToPage(self, detailView, width=100, height=100):
        """add a plane surface with a known "page size" in the 3d model. If the object measurements in page space are 100x100, this is a success.
        """
        pageCorners = self.GetPageCornersFromDetailView(detailView)
        pagePlane = self.CreatePagePlaneFromPageCorner(pageCorners)
        origin = pagePlane.Origin

        otherScale = self.GetModelToDetailScale(detailView)
        
        dbugSrf100 = rg.PlaneSurface(pagePlane, rg.Interval(0.0, width/otherScale), rg.Interval(0.0, height/otherScale))
        doc.Objects.AddSurface(dbugSrf100)

    
    def GetPageViewFromDetailView(self, detailViewObject):
        """I didn't find a way to get the page information from a detail view so i'll look 
        into all pages in the document until I find one that contains my detail view object
        
        returns the first page we find with a detailview that match the input detailview Id, None on failure.
        """
        for page in self.GetAllPageViews() :
            # retrieve all detail view 
            detailViews = page.GetDetailViews()
            for detailView in detailViews : 
                if detailView.Id == detailViewObject.Id:
                    return page
        

    def GetDetailToModelScale(self, detailViewObject):
        """ I didn't find a way to quickly access a detail view object scale other than reading the "formated" scale and removing the formating.
        """
        scaleType = detailViewObject.ScaleFormat.OneToModelLength
        # get the detail view scale 
        success, scaleString = detailViewObject.GetFormattedScale(scaleType)
        scale = float(scaleString.split(":")[-1])
        return scale
    
    def GetUnitScaleFactor(self):
        # we don't solve that at the moment
        return 1 
        unitFactor = Rhino.RhinoMath.UnitScale(Rhino.RhinoDoc.ActiveDoc.ModelUnitSystem, Rhino.UnitSystem.Millimeters) 
        return unitFactor

    
    def GetModelToDetailScale(self, detailViewObject):
        # scaleType = detailViewObject.ScaleFormat.PageLengthToOne
        # get the detail view scale 
        success, scale= detailViewObject.GetFormattedScale(0)
        scale = float(scale)
        scale = scale

        return scale

    def GetRhinoViewportCameraPlane(self, RhinoViewport):
        """retrieves this viewport camera plane centered on the camera target

        Args:
            RhinoViewport (RhinoViewport): a rhino viewport
        """
        

        # retrieve the camera plane 
        origin = RhinoViewport.CameraTarget 
        xAxis = RhinoViewport.CameraX
        yAxis = RhinoViewport.CameraY
        zAxis = RhinoViewport.CameraZ

        # region ----- debug geometry  ----- 
        # self.AdvanceBakePoint(origin, "CameraOrigin", (255, 0, 0))
        # endregion ----- debug geometry  ----- 

        cameraPlane = rg.Plane(origin, xAxis, yAxis)
        return cameraPlane

        
        
    def GetExportPath(self):
        dialog = Rhino.UI.SaveFileDialog()
        
        dialog.InitialDirectory = Rhino.RhinoDoc.ActiveDoc.Path
        dialog.DefaultExt = ".pdf"
        dialog.Filter = ".pdf"
        dialog.ShowSaveDialog()
        fullPath = dialog.FileName

        return fullPath


    @classmethod
    def AdvanceBakePoint(cls, point, name = None, color= None):
        pointId = doc.Objects.AddPoint(point)
        if name : rs.ObjectName(pointId, name)
        if color : rs.ObjectColor(pointId, color)
        return pointId





if __name__ == "__main__":
    Execute()