import streamlit as st
import win32com.client
import os
import pythoncom  # Import pythoncom library

def inject_macro(excel_file_path, macro_code):
    # Initialize the COM library for the current thread
    pythoncom.CoInitialize()

    com_instance = win32com.client.Dispatch("Excel.Application")
    com_instance.Visible = False  # Set to False to not show Excel on the screen
    com_instance.DisplayAlerts = False

    workbook = com_instance.Workbooks.Add()
    xlmodule = workbook.VBProject.VBComponents.Add(1)  # 1 is for a standard module
    xlmodule.CodeModule.AddFromString(macro_code)
    workbook.SaveAs(Filename=excel_file_path, FileFormat=52)  # 52 is the file format for .xlsm
    workbook.Close()
    com_instance.Quit()

    # Uninitialize the COM library for the current thread
    pythoncom.CoUninitialize()


def main():
    st.title('Excel Macro Generator')

    macro_code = st.text_area("Input your macro code here:", '''
    Sub SampleMacro()
        MsgBox "This is a sample macro!"
    End Sub
    ''', height=300)

    if st.button('Generate Excel File with Macro'):
        # Temporary path for the generated Excel file
        excel_file_path = os.path.join(os.getcwd(), "GeneratedExcelFile.xlsm")

        # Generate the Excel file
        inject_macro(excel_file_path, macro_code)

        # Read the generated file into a buffer
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
