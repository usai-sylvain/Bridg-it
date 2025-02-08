import PyPDF2 as pdf
from datetime import datetime
import Rhino.Geometry as rg
import scriptcontext as sc


filePath = "/Users/sjo/Desktop/Hackathon/Testfile.pdf"

def extract_comments(path):
    comments = []
    
    with open(path, "rb") as file:
        reader = pdf.PdfReader(file)
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            
            if "/Annots" in page:
                for annot in page["/Annots"]:
                    annotation = annot.get_object()
                    print(annotation)


                    comment = annotation.get("/Contents", "").strip()
                    creationTime = annotation.get('/CreationDate',"").strip()
                    autor = annotation.get('/T',"").strip()
                    annotationType = annotation.get("/Subtype","").strip()

                    print(annotationType)
                    print(autor)
                    


                    if "/Rect" in annotation:
                        rect = annotation["/Rect"]
                        print(rect)
                        x1, y1, x2, y2 = rect
                        x = (x1 + x2) / 2 
                        y = (y1 + y2) / 2 
                        position = (float(x),float(y))
                    else:
                        position = "unknown" #revisit: what happens after this?

                    if comment:
                        comments.append((position, comment, autor, creationTime, annotationType))

                    else:
                        pass
                        #print("noComment")
                        #revisit: what happens when there is no comment?

    return comments







point = rg.Point3d(0,0,0)

text_dot = rg.TextDot("test", point)


sc.doc.Objects.AddTextDot(text_dot)
sc.doc.Views.Redraw()

print("done")

#pdfAnnotations = extract_comments(filePath)

"""for comment in pdfAnnotations:
    print(comment)
"""