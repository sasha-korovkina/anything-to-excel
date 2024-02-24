import streamlit as st
import win32com.client
import os
import pythoncom  # Import pythoncom library
import xlwings as xw
import base64

def inject_macro(excel_file_path, macro_name):
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
    macro = wb.macro(macro_name)

    try:
        macro(pdf_file)
    except Exception as e:
        error_message = str(e)
        raise
    finally:
        app.quit()

def main():
    st.title('Excel Macro Generator')

    uploaded_files = st.file_uploader("Upload PDF Files", accept_multiple_files=True)

    if st.button('Generate Excel Files with Macros') and uploaded_files:
        for pdf_file in uploaded_files:
            # Temporary path for the generated Excel file
            excel_file_path = os.path.join(os.getcwd(), f"{pdf_file.name.split('.')[0]}.xlsm")

            # Generate the Excel file
            inject_macro(excel_file_path, "pdfLoader")

            # Execute the macro
            execute_macro(excel_file_path, pdf_file.name)

            # Display a download button for the Excel file
            download_button_str = generate_download_button(excel_file_path, pdf_file.name.split('.')[0])
            st.markdown(download_button_str, unsafe_allow_html=True)

        st.success("Excel files generated successfully!")
#
def execute_macro(file_path, pdf_file_name):
    # Open the Excel file
    app = xw.App(visible=False)
    wb = app.books.open(file_path)

    try:
        # Run the macro with the PDF file name as parameter
        macro_name = "pdfLoader"
        pdf_file = os.path.join(os.getcwd(), pdf_file_name)
        wb.macro(macro_name)(pdf_file)
    except Exception as e:
        print(f"Error occurred while running macro: {e}")
    finally:
        # Save and close the workbook
        wb.save()
        wb.close()
        app.quit()

def generate_download_button(file_path, file_name):
    with open(file_path, "rb") as file:
        bytes_data = file.read()
    b64_data = base64.b64encode(bytes_data).decode()
    download_button_str = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_data}" download="{file_name}.xlsm"><button>Download {file_name}</button></a>'
    return download_button_str

if __name__ == "__main__":
    main()