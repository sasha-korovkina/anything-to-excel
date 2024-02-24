import xlwings as xw

def run_excel_macro_with_parameter(file_path, macro_name, pdf_file):
    wb = xw.Book(file_path)
    app = xw.App(visible=False)
    macro = wb.macro(macro_name)

    try:
        macro(pdf_file)
    except Exception as e:
        error_message = str(e)
        wb.sheets['Errors'].range('A1').value = error_message
        raise
    finally:
        app.quit()

file_path = "M:\\CDB\\Analyst\\Sasha\\Custodian Automation\\pdfTesting.xlsm"
macro_name = "getDataPDF"
pdf_file = r"M:\CDB\Analyst\Rhys\Data\Goldman Sachs Europe DDMMYYYY 30032023 MDXHEALTH S.A._BE0003844611_21-Mar-2023.pdf_decrypted.pdf"

# Run the macro with the input parameter
run_excel_macro_with_parameter(file_path, macro_name, pdf_file)
