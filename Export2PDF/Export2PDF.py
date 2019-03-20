import arcpy
import os
from arcpy import env
#get parameter input of infc and savefilename 
#Get the value of the input parameter
#MXD folder
mxdpath = arcpy.GetParameterAsText(0)
pdfpath = arcpy.GetParameterAsText(1)
#pdfmergedfile = arcpy.GetParameterAsText(2)
arcpy.AddMessage("MXD Path: " + mxdpath)
arcpy.AddMessage("PDF Save Path: " + pdfpath)
#input file
#infc=r'C:\Dropbox\GIS\01_Analysis_Projects\99_Online_Services\Wikimapia\Test\polyline.shp'
##outpolygon=r'C:\Dropbox\GIS\01_Analysis_Projects\99_Online_Services\Wikimapia\Test\polygon.shp'
#make output file
exporttype="PDF"
# Read lines in the file and append to coordinate list
#get all mxd files in folder
allfiles = os.listdir(mxdpath)
#for mxdfile in mxdfiles:
mxdfiles = [(x) for x in allfiles if x.endswith('.mxd')]
mxdfiles.sort()
#create pdf merged file name
#Set file name and remove if it already exists
#pdfmergedfilename = pdfpath + '\\' + pdfmergedfile + '.pdf'
#if os.path.exists(pdfmergedfilename):
#    os.remove(pdfmergedfilename)
#create new file
    #Create the file and append pages
#pdfDoc = arcpy.mapping.PDFDocumentCreate(pdfmergedfilename)
for mxdfilename in mxdfiles:
    arcpy.AddMessage("Processing File ...: " + mxdfilename)    
    mxd = arcpy.mapping.MapDocument(mxdpath + '\\' + mxdfilename)
    mxd.save()
    pagelayout = arcpy.mapping.ListDataFrames(mxd, "PAGE_LAYOUT") 
    # check to see if there is already a pdf file created for this county
    pdfname = os.path.splitext(mxdfilename)[0]
    pdffilename = pdfpath + '\\' + pdfname + '.pdf'
    if os.path.exists(pdffilename):
        arcpy.AddMessage("Existing pdf found. Replacing file..." + pdffilename)
        arcpy.mapping.ExportToPDF(mxd, pdffilename,pagelayout)
        
    else: # file does not exist, export to new file
        arcpy.AddMessage("No Existing pdf found. Creating new file file..." + pdffilename)
        arcpy.mapping.ExportToPDF(mxd, pdffilename,pagelayout)   

    #pdfDoc.appendPages(pdffilename)
#-----Delete variable reference-----
#Commit changes and delete variable reference
#pdfDoc.saveAndClose()
#del pdfDoc       
