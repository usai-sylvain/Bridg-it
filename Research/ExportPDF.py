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

class PDFExporter():


    def Sandbox(self):
        # get all view pages 
        views = self.GetAllPageViews()
        # get the coordinate system 
        coordinate = self.GetCoordinateSystemFromPage(views[0])
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
    

    def GetCoordinateSystemFromPage(self, rhinoPageView):
        """retrieves the viewport of this page and its coordinate system

        Args:
            rhinoPageView (RhinoPageView): The view we want to use
        """

        detailViews = rhinoPageView.GetDetailViews()
        for detailViewObject in detailViews : 
            # retrieve the viewport 
            viewport = detailViewObject.Viewport

            # get the Camera plane from the viewport
            cameraPlane = self.GetRhinoViewportCameraPlane(viewport)
            scale = self.GetDetailToModelScale(detailViewObject)
            

            # get the page size 
            width = rhinoPageView.PageWidth
            height = rhinoPageView.PageHeight
            
                    
            realWidth = width   * scale
            realHeight = height * scale

            # create a debug surface 
            dbugSrf = rg.PlaneSurface(cameraPlane, rg.Interval(-realWidth * 0.5, realWidth * 0.5), rg.Interval(-realHeight * 0.5, realHeight * 0.5))
            doc.Objects.AddSurface(dbugSrf)

            otherScale = self.GetModelToDetailScale(detailViewObject)

            print(scale, otherScale)
            dbugSrf10 = rg.PlaneSurface(cameraPlane, rg.Interval(-10 * 0.5 / otherScale, 10 * 0.5 / otherScale), rg.Interval(-10 * 0.5 / otherScale, 10 * 0.5 / otherScale))
            doc.Objects.AddSurface(dbugSrf10)

            return cameraPlane

    def GetDetailToModelScale(self, detailViewObject):
        """ I didn't find a way to quickly access a detail view object scale other than reading the "formated" scale and removing the formating.
        """
        scaleType = detailViewObject.ScaleFormat.OneToModelLength
        # get the detail view scale 
        success, scaleString = detailViewObject.GetFormattedScale(scaleType)
        scale = float(scaleString.split(":")[-1])
        return scale
    
    def GetModelToDetailScale(self, detailViewObject):
        scaleType = detailViewObject.ScaleFormat.PageLengthToOne
        # get the detail view scale 
        success, scaleString = detailViewObject.GetFormattedScale(scaleType)
        scale = float(scaleString.split(":")[0])
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


        





if __name__ == "__main__":
    Execute()