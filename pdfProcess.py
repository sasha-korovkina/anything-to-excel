import xlwings as xw

wb = xw.Book("M:\\CDB\\Analyst\\Sasha\\Custodian Automation\\pdfTesting.xlsm")
pdf_file = "M:\CDB\Analyst\Rhys\Data\Goldman Sachs Europe DDMMYYYY 30032023 MDXHEALTH S.A._BE0003844611_21-Mar-2023.pdf_decrypted.pdf"

app = xw.App(visible=False)
pdfToExcel = wb.macro("test2")

try:
    pdfToExcel()
except Exception as e:
    error_message = "Expression.Error: The key didn't match any rows in the table."
    wb.sheets['Errors'].range('A1').value = error_message
    raise

