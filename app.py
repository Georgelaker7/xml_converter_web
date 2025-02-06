from flask import Flask, render_template, request, send_file
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

def convert_xml(input_xml):
    tree = ET.parse(input_xml)
    root = tree.getroot()

    booking = root.find(".//Booking")
    
    transfers = ET.Element("transfers", MessageType="Request", FechaCreacion=booking.findtext("Booking_date", "N/A"), Count="1")
    transfer = ET.SubElement(transfers, "transfer")

    # Προσθήκη στοιχείων στο XML
    ET.SubElement(transfer, "result")
    ET.SubElement(transfer, "client").text = "HER"
    ET.SubElement(transfer, "ttoo").text = booking.findtext("Company", "N/A")
    
    ET.SubElement(transfer, "brand")
    ET.SubElement(transfer, "carrier")
    
    ET.SubElement(transfer, "serviceType").text = booking.findtext("TransferType", "N/A")
    ET.SubElement(transfer, "flightCompanyCode").text = booking.findtext("ArrivalFlightNumber", "N/A")[:3]  # Εξαγωγή πρώτων 3 χαρακτήρων ως κωδικός
    ET.SubElement(transfer, "flightNumber").text = booking.findtext("ArrivalFlightNumber", "N/A")[3:]  # Αριθμός πτήσης
    ET.SubElement(transfer, "flightDate").text = booking.findtext("ArrivalDate", "N/A")
    ET.SubElement(transfer, "flightTime").text = booking.findtext("ArrivalTime", "N/A") + ":00"
    ET.SubElement(transfer, "flightOrigin").text = booking.findtext("ArrivalAirportFrom", "N/A")
    ET.SubElement(transfer, "flightDestination").text = booking.findtext("ArrivalAirportTo", "N/A")
    
    ET.SubElement(transfer, "serviceCode")
    ET.SubElement(transfer, "voucher").text = booking.get("ref", "N/A")  # Διαβάζει το ref του Booking ως voucher
    
    ET.SubElement(transfer, "paxName").text = booking.findtext("Customer_name", "N/A")
    
    ET.SubElement(transfer, "arrDepCode")
    ET.SubElement(transfer, "arrDepPhysicalArea").text = booking.findtext("DepartureLocFrom", "N/A")
    ET.SubElement(transfer, "arrDepName").text = booking.findtext("SpecificLocation", "N/A")
    ET.SubElement(transfer, "arrOrder")
    ET.SubElement(transfer, "areaOrder")

    ET.SubElement(transfer, "paxADT").text = booking.findtext("Adults", "N/A")
    ET.SubElement(transfer, "paxCHD").text = booking.findtext("Children", "N/A")
    ET.SubElement(transfer, "CHD_AGES")
    ET.SubElement(transfer, "paxINF").text = booking.findtext("Infants", "N/A")
    
    ET.SubElement(transfer, "vehicle").text = booking.findtext("Transportation_Unit", "N/A")

    ET.SubElement(transfer, "rep")
    ET.SubElement(transfer, "remarks")
    
    ET.SubElement(transfer, "pickupDate").text = booking.findtext("DepartureDate", "N/A")
    ET.SubElement(transfer, "pickupTime").text = booking.findtext("DepartureTime", "N/A") + ":00"
    
    ET.SubElement(transfer, "observations")

    output_xml = "converted.xml"
    tree = ET.ElementTree(transfers)
    tree.write(output_xml, encoding="utf-8", xml_declaration=True)

    return output_xml

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    output_file = convert_xml(file_path)

    return send_file(output_file, as_attachment=True)

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True, host="0.0.0.0", port=5000)
