import streamlit as st
import win32com.client
import os
import pythoncom  # Import pythoncom library
import xlwings as xw

def inject_macro(excel_file_path, macro_code, macro_name):
    # Initialize the COM library for the current thread
    pythoncom.CoInitialize()

    com_instance = win32com.client.Dispatch("Excel.Application")
    com_instance.Visible = False
    com_instance.DisplayAlerts = False

    workbook = com_instance.Workbooks.Add()
    xlmodule = workbook.VBProject.VBComponents.Add(1)
    xlmodule.Name = macro_name  # Set the name of the module
    xlmodule.CodeModule.AddFromString(macro_code)
    workbook.SaveAs(Filename=excel_file_path, FileFormat=52)
    workbook.Close()
    com_instance.Quit()

    pythoncom.CoUninitialize()

def run_excel_macro_with_parameter(file_path, macro_name, pdf_file):
    wb = xw.Book(file_path)
    app = xw.App(visible=False)

    try:
        # Execute the macro with the parameter
        wb.macro(macro_name)(pdf_file)
    except Exception as e:
        error_message = str(e)
        raise
    finally:
        app.quit()

def main():
    st.title('Excel Macro Generator')

    # If at any point we want the user to generate their own macros
    # macro_code = st.text_area("Input your macro code here:", '''
    # Sub SampleMacro()
    #     MsgBox "This is a sample macro!"
    # End Sub
    # ''', height=300)

    macro_code = '''
            Sub getDataPDF(FileName As String)
            ActiveWorkbook.Queries.Add Name:="PDF Query", Formula:= _
                "let" & Chr(13) & "" & Chr(10) & "    Source = Pdf.Tables(File.Contents(""" & FileName & """), [Implementation=""1.3""])," & Chr(13) & "" & Chr(10) & "    #""Expanded Data"" = Table.ExpandTableColumn(Source, ""Data"", {""Column1"", ""Column2"", ""Column3"", ""Column4"", ""Column5""}, {""Data.Column1"", ""Data.Column2"", ""Data.Column3"", ""Data.Column4"", ""Data.Column5""})" & Chr(13) & "" & Chr(10) & "in" & Chr(13) & "" & Chr(10) & "    #""Expanded Data"""
            ActiveWorkbook.Worksheets.Add
            With ActiveSheet.ListObjects.Add(SourceType:=0, Source:= _
                "OLEDB;Provider=Microsoft.Mashup.OleDb.1;Data Source=$Workbook$;Location=""Task pdf"";Extended Properties=""""" _
                , Destination:=Range("$A$1")).QueryTable
                .CommandType = xlCmdSql
                .CommandText = Array("SELECT * FROM [PDF Query]")
                .RowNumbers = False
                .FillAdjacentFormulas = False
                .PreserveFormatting = True
                .RefreshOnFileOpen = False
                .BackgroundQuery = True
                .RefreshStyle = xlInsertDeleteCells
                .SavePassword = False
                .SaveData = True
                .AdjustColumnWidth = True
                .RefreshPeriod = 0
                .PreserveColumnInfo = True
                '.ListObject.DisplayName = "Task_pdf"
                .Refresh BackgroundQuery:=False
            End With
        End Sub
    '''

    if st.button('Generate Excel File with Macro'):
        # Temporary path for the generated Excel file
        excel_file_path = os.path.join(os.getcwd(), "sasha.xlsm")

        # Generate the Excel file
        inject_macro(excel_file_path, macro_code, "pdfLoader")

    if st.button('Run Macro without Displaying Excel'):
        try:
            # Temporary path for the generated Excel file
            excel_file_path = os.path.join(os.getcwd(), "sasha.xlsm")

            # Execute the macro within the Excel
            macro_name = "pdfLoader"
            pdf_file = r"M:\CDB\Analyst\Rhys\Data\Goldman Sachs Europe DDMMYYYY 30032023 MDXHEALTH S.A._BE0003844611_21-Mar-2023.pdf_decrypted.pdf"
            run_excel_macro_with_parameter(excel_file_path, macro_name, pdf_file)
        finally:
            st.success("Macro executed successfully!")
    if st.button('Download'):
        with open(excel_file_path, "rb") as file:
            btn = st.download_button(
                label="Download Excel File with Macro",
                data=file,
                file_name="GeneratedExcelFile.xlsm",
                mime="application/vnd.ms-excel.sheet.macroEnabled.12"
            )

        if btn:
            st.success("Download started!")

if __name__ == "__main__":
    main()
