from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_contract(filename, name, date, client, amount):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "SERVICE AGREEMENT")

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 140, f"Contract Name: {name}")
    c.drawString(100, height - 160, f"Effective Date: {date}")
    c.drawString(100, height - 180, f"Client: {client}")
    c.drawString(100, height - 200, f"Total Amount: ${amount}")

    c.drawString(100, height - 240, "This agreement is entered into between the Provider and the Client.")
    c.drawString(100, height - 260, "The Provider agrees to deliver software services as described in Annex A.")
    c.drawString(100, height - 280, "The Client agrees to pay the total amount specified above.")

    c.save()

os.makedirs("contracts", exist_ok=True)
create_contract("contracts/contract_1.pdf", "Software Development", "2024-01-01", "Acme Corp", "50,000")
create_contract("contracts/contract_2.pdf", "Cloud Hosting", "2024-02-15", "Globex Corp", "12,000")
create_contract("contracts/contract_3.pdf", "Maintenance Agreement", "2024-03-01", "Soylent Corp", "5,000")

print("Sample contracts generated.")
