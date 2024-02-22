import win32com.client
import os


def convert_and_inject_macro(excel_file_path, macro_code):
    """
    Converts an .xlsx file to .xlsm and injects a macro.
    """
    # Ensure the Excel instance is not visible and alerts are disabled
    com_instance = win32com.client.Dispatch("Excel.Application")
    com_instance.Visible = False
    com_instance.DisplayAlerts = False

    # Derive new file path with .xlsm extension
    new_file_path = os.path.splitext(excel_file_path)[0] + ".xlsm"

    # Open the .xlsx file
    workbook = com_instance.Workbooks.Open(excel_file_path)

    # Save the workbook as .xlsm (macro-enabled workbook)
    workbook.SaveAs(Filename=new_file_path, FileFormat=52)  # 52 corresponds to .xlsm

    # Add a VBA module and inject the macro code
    xlmodule = workbook.VBProject.VBComponents.Add(1)  # 1 is for a standard module
    xlmodule.CodeModule.AddFromString(macro_code)

    # Save changes to the .xlsm file
    workbook.Close(SaveChanges=True)

    # Quit Excel
    com_instance.Quit()

    return new_file_path


# Path to your original Excel file (.xlsx)
original_excel_file_path = "C:\\Users\\sasha\\Desktop\\Sabadell Averages.xlsx"

# Macro code to inject
macro_code = '''
Sub SampleMacro()
   MsgBox "This is a sample macro!"
End Sub
'''

# Convert the .xlsx file to .xlsm and inject the macro
new_file_path = convert_and_inject_macro(original_excel_file_path, macro_code)

print(f"Macro injected successfully into: {new_file_path}")
