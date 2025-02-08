

def extract_comments(path):
    comments = []
    
    with open(path, "rb") as file:
        reader = pdf.PdfReader(file)
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            
            if "/Annots" in page:
                for annot in page["/Annots"]:
                    annotation = annot.get_object()
                    #print(annotation)


                    comment = annotation.get("/Contents", "").strip()
                    creationDate = annotation.get('/CreationDate',"").strip()
                    autor = annotation.get('/T',"").strip()
                    annotationType = annotation.get("/Subtype","").strip()



                    print(annotationType)
                    print(autor)
                    print(creationDate)
                    #print(datetime.strptime(creationDate[2:], "%Y%m%d%H%M%S"))

                    
                    if "/Rect" in annotation:
                        rect = annotation["/Rect"]
                        print(rect)
                        x1, y1, x2, y2 = rect
                        x = (x1 + x2) / 2 
                        y = (y1 + y2) / 2 
                        position = (float(x),float(y))
                    else:
                        position = "Unknown"

                    if comment:
                        comments.append((comment, position))
                    else:
                        pass
                        #print("noComment")
                        #revisit: what happens when there is no comment?

    return comments



pdfAnnotations = extract_comments(filePath)
""" print(pdfAnnotations)
for comment in pdfAnnotations:
    pass """
    #print(comment)
