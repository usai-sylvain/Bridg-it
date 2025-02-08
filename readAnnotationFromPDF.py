import PyPDF2 as pdf
from datetime import datetime
import Rhino.Geometry as rg
import scriptcontext as sc
import rhinoscriptsyntax as rs


filePath = "/Users/sjo/Desktop/Hackathon/Testfile.pdf"

def extract_comments(path):
    comments = []
    
    with open(path, "rb") as file:
        reader = pdf.PdfReader(file)
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            #pageSize = 
            
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

    return comments

def addTextObjects(Annotations):
    for comment in Annotations:
        location = rg.Point3d(comment[0][0], comment[0][1], 0)
        text_dot = rg.TextDot(f"{comment[2]} ({comment[3]}): {comment[1]}", location)
        sc.doc.Objects.AddTextDot(text_dot)

        if comment[5] != None:
            rs.AddPoint(comment[5][0], comment[5][1], 0)
            
    sc.doc.Views.Redraw()
    





pdfAnnotations = extract_comments(filePath)
addTextObjects(pdfAnnotations)

print("done")
"""for comment in pdfAnnotations:
    print(comment)
"""