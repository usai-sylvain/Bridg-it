import rhinoscriptsyntax as rs 
import Rhino 
import scriptcontext 
from scriptcontext import doc
import System 
import Rhino.Geometry as rg



def ExecuteExportPDF():
    exporter = PDFIO()
 
    exporter.Execute()

def ExecuteImportPDF():
    exporter = PDFIO()

    

class PDFIO(object):

    def __init__(self):
        # check requirements 
        if Rhino.RhinoDoc.ActiveDoc.ModelUnitSystem != Rhino.UnitSystem.Millimeters : 
            print("ExportPDF.Warning : model unit is not in mm !")

        # set the DPI value 
        self.PDF_DPI = 72
        


    def Execute(self):
        # get all view pages 
        page = self.GetAllPageViews()[0]
        
        detailViews = page.GetDetailViews()
        detailView = detailViews[0]
        # self.DEBUG_3dSpaceToPage(detailView)

        hashTextId = self.CreateHashText(detailView)

        # export 
        self.Export(page)

        # delete the hash text


        # rs.AddPlaneSurface(coordinate, 500, 500)
    
    def CreateHashText(self, detailView):
        corners = self.GetPageCornersFromDetailView(detailView)
        # get the corner hash 
        cornerHashes = []
        for i, corner in enumerate(corners) : 
            hash = self.HashCorner(corner, i)
            # print hash
            cornerHashes.append(hash)
            
        bridgeHash = "*BRIDGEIT*%s"%("%".join(cornerHashes[0:3]))

        # make the page viewport active 
        page = self.GetPageViewFromDetailView(detailView)

        Rhino.RhinoDoc.ActiveDoc.Views.ActiveView = page
        # add a text in the page for the first three corners 
    
        hashPlane = rg.Plane.WorldXY
        hashPlane.Origin = rg.Point3d(10.0, 10.0, 0.0)
        hashHeight = 1.0
        hashFont = "Arial"

        hashTextObjectId = Rhino.RhinoDoc.ActiveDoc.Objects.AddText(bridgeHash, hashPlane, hashHeight, hashFont, False, True)

        fakePlane = rg.Plane.WorldXY
        fakePlane.Origin = rg.Point3d(50.0, 100.0, 0.0)
        fakeTextContent = self.GetLoremIpsum()


        fakeText = Rhino.RhinoDoc.ActiveDoc.Objects.AddText(fakeTextContent, fakePlane, hashHeight, hashFont, False, False)
        return hashTextObjectId




    def Export(self, rhinoPage):

        # get a target path for our padf
        exportPath = self.GetExportPath()
        if not exportPath :
            print("User aborted PDF export")
            return
        
        
        # create a new instance of RhinoPDF exporter
        pdf = Rhino.FileIO.FilePdf.Create()

        # make the detail page active 
        Rhino.RhinoDoc.ActiveDoc.Views.ActiveView = rhinoPage
        captureSettings = Rhino.Display.ViewCaptureSettings(rhinoPage, self.PDF_DPI)
        pdf.AddPage(captureSettings)
        
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
    
    def HashCorner(self, corner, cornerIndex):
        """convert a corner to a hash string            
        """
        return "I%s_X%.10f_Y%.10f_Z%.10f"%(cornerIndex, corner.X, corner.Y, corner.Z)
    
    
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


    def GetLoremIpsum(self):
        return "Artificial amateurs aren't at all amazing \nAnalytically, I assault, animate things \nBroken barriers bounded by the bomb beat \nBuildings are broken, basically I'm bombarding \nCasually create catastrophes, casualties \nCanceling cats, got their canopies collapsing \nDetonate \na dime of dank daily doin' dough \nDemonstrations, Don Dada on the down low \nEating other editors with each and every energetic \nEpileptic episode, elevated etiquette \nFurious, fat, \nfabulous, fantastic"



if __name__ == "__main__":
    # ExecuteExportPDF()