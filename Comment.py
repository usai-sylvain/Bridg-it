from datetime import datetime

class Comment(object):
    
    
    
    
    def __init__(self, SourceFileName=None, SourceFileCreationDate=None, Author = None, Text=None,Point3d=None ConnectedElementGuid=None, ConnectedElementName=None):
        
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
    

    

def main():
    

    
    

main()