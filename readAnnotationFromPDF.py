import PyPDF2 as pdf
from datetime import datetime
import Rhino.Geometry as rg
import scriptcontext as sc
import rhinoscriptsyntax as rs


filePath = "/Users/sjo/Desktop/Hackathon/Bridg-it/Research/Test1.pdf"

def getMarker(path):
    marker = []
    with open(path, "rb") as file:
        reader = pdf.PdfReader(file)
        
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            textOnPage = page.extract_text()

            
            for text in textOnPage.split("\n"):

                if text[:10] == "*BRIDGEIT*":
                    marker.append(text)
    
    return marker


def extract_comments(path):
    comments = []
    marker = []
    
    with open(path, "rb") as file:
        reader = pdf.PdfReader(file)
        
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            textOnPage = page.extract_text()

            
            for text in textOnPage.split("\n"):

                if text[:10] == "*BRIDGEIT*":
                    marker.append(text)
            
            print(marker)
            pageSize = page.mediabox

            pageOrigin = (pageSize[0], pageSize[1])
            pageTopLeft = (pageSize[0], pageSize[3])
            pageLowRight = (pageSize[0], pageSize[2])

            pageRec = rg.Rectangle3d(rg.Plane.WorldXY, pageSize[2], pageSize[3])

            print(pageOrigin)
            print(pageTopLeft)
            print(pageLowRight)
            
            if "/Annots" in page:
                for annot in page["/Annots"]:
                    annotation = annot.get_object()
                    #print(annotation)


                    comment = annotation.get("/Contents", "").strip()
                    creationTime = annotation.get('/CreationDate',"").strip()
                    autor = annotation.get('/T',"").strip()
                    annotationType = annotation.get("/Subtype","").strip()

                    #date = datetime.strptime(creationTime[2:10], "%Y%m%d")
                    #print(creationTime[2:10])
                    


                    if "/Rect" in annotation:
                        rect = annotation["/Rect"]
                        #print(rect)
                        x1, y1, x2, y2 = rect
                        x = (x1 + x2) / 2 
                        y = (y1 + y2) / 2 
                        position = (float(x),float(y))
                    else:
                        position = "unknown" #revisit: what happens after this?


                    
                    if "/CL" in annotation:
                        arrowStartX = float(annotation["/CL"][0])
                        arrowStartY = float(annotation["/CL"][1])
                        arrowStart = (arrowStartX, arrowStartY)

                    else:
                        arrowStart = None


                    if comment:
                        date = datetime.strptime(creationTime[2:10], "%Y%m%d")
                        formatedTime = date.strftime("%m.%d.%Y")

                        comments.append((position, comment, autor, formatedTime, annotationType, arrowStart))

                    else:
                        pass
                        #print("noComment")
                        #revisit: what happens when there is no comment?

    return comments, pageRec

def addTextObjects(Annotations, pageRec, targetRec):

    #####SCALE
    inputWidth = pageRec.Width
    inputHeight = pageRec.Height
    
    targetWidth = targetRec.Width
    targetHeight = targetRec.Height

    scaleX = targetWidth / inputWidth
    scaleY = targetHeight / inputHeight

    #####TRANSLATION
    inputCenter = pageRec.Center
    targetCenter = targetRec.Center
    translation = targetCenter - inputCenter

    print(inputCenter)
    print(scaleX)
    print(scaleY)

    #####ROTATION
    inputPlane = pageRec.Plane
    targetPlane = targetRec.Plane
    rotation = rg.Transform.Rotation(inputPlane.XAxis, inputPlane.XAxis, inputCenter)
    rotation *= rg.Transform.Rotation(targetPlane.YAxis, targetPlane.YAxis, targetCenter)


    #####TRANSFORMATION
    transformation = rg.Transform.Translation(translation)
    transformation *= rotation
    #transformation *= rg.Transform.Scale(inputCenter, scaleX, scaleX)
    

    print(rotation)
    for comment in Annotations:
        location = rg.Point3d(comment[0][0], comment[0][1], 0)
        text_dot = rg.TextDot(f"{comment[2]} ({comment[3]}): {comment[1]}", location)
        sc.doc.Objects.AddTextDot(text_dot)

        if comment[5] != None:
            rs.AddPoint(comment[5][0], comment[5][1], 0)
            
    sc.doc.Views.Redraw()
    

planeOrigin = rg.Point3d(0,0,0)
planeX = rg.Point3d(1,5,0)
planeY = rg.Point3d(0,1,0.3)

plane = rg.Plane.CreateFromPoints(planeOrigin, planeX, planeY)
dummyRec = rg.Rectangle3d(plane, 29.7, 21.0)
sc.doc.Objects.AddRectangle(dummyRec)



pdfAnnotations, pageRec = extract_comments(filePath)
addTextObjects(pdfAnnotations, pageRec, dummyRec)
sc.doc.Objects.AddRectangle(pageRec)
print("done")

for comment in pdfAnnotations:
    print(comment)


mark = getMarker(filePath)

print(mark)