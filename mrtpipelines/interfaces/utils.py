def createTemplateTract(in_tracts, out_tract):
    # Create template from subject tractography
    import vtk
    import os.path as op

    for tract in in_tracts:
        tract = tract[0]
        if op.isfile(tract) is True:
            # VTK readers
            outReader = vtk.vtkPolyDataReader()
            outReader.SetFileName(out_tract)
            inReader = vtk.vtkPolyDataReader()
            inReader.SetFileName(tract)

            # VTK appender
            appender = vtk.vtkAppendPolyData()
            if op.isfile(out_tract) is True:
                appender.AddInputConnection(outReader.GetOutputPort())
                appender.AddInputConnection(inReader.GetOutputPort())
                appender.Update()
            else:
                appender.AddInputConnection(inReader.GetOutputPort())
                appender.Update()

            # VTK writer
            writer = vtk.vtkPolyDataWriter()
            writer.SetFileTypeToBinary()
            writer.SetFileName(out_tract)
            writer.SetInputConnection(appender.GetOutputPort())
            writer.Write()

        else:
            continue

    return out_tract
