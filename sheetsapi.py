from oauth2client.service_account import ServiceAccountCredentials
import gspread


class Sheets:
    # Authentication from credentials in client_secret.json
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    password = "admin"
    sheetname = "sheet"  # Change to name of Spreadsheet

    def getRow(str, worksheet, client=client):
        # Gets the complete row of a cell specified by it's label
        sheet = client.open(Sheets.sheetname).worksheet(worksheet)
        row = sheet.row_values(sheet.find(str).row)
        return row

    def createRow(*args, worksheet, client=client):
        # Creates a new row in the chosen worksheet
        sheet = client.open(Sheets.sheetname).worksheet(worksheet)
        sheet.append_row(args)

    def checkID(id, worksheet, client=client):
        # Checks if ID exists in database and returns corresponding name
        try:
            row = Sheets.getRow(id, worksheet)
        except gspread.exceptions.CellNotFound:
            return "null"
        return row[1]
