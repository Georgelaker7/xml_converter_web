from flask import Flask, render_template, request, send_file
import xml.etree.ElementTree as ET
import os
import html

app = Flask(__name__)

def convert_xml(input_xml):
    tree = ET.parse(input_xml)
    root = tree.getroot()

    booking = root.find(".//Booking")
    transfers = ET.Element("transfers", MessageType="Request", FechaCreacion=booking.find("Booking_date").text, Count="1")
    transfer = ET.SubElement(transfers, "transfer")

    ET.SubElement(transfer, "result")
    ET.SubElement(transfer, "client").text = "HER"
    ET.SubElement(transfer, "ttoo").text = booking.find("Company").text if booking.find("Company") is not None else "N/A"

    ET.SubElement(transfer, "brand")
    ET.SubElement(transfer, "carrier")

    ET.SubElement(transfer, "serviceType").text = booking.find("TransferType").text if booking.find("TransferType") is not None else "N/A"
    ET.SubElement(transfer, "flightCompanyCode").text = booking.find("FlightCompanyCode").text if booking.find("FlightCompanyCode") is not None else "N/A"
    ET.SubElement(transfer, "flightNumber").text = booking.find("ArrivalFlightNumber").text if booking.find("ArrivalFlightNumber") is not None else "N/A"
    ET.SubElement(transfer, "flightDate").text = booking.find("ArrivalDate").text if booking.find("ArrivalDate") is not None else "N/A"
    ET.SubElement(transfer, "flightTime").text = booking.find("ArrivalTime").text if booking.find("ArrivalTime") is not None else "N/A"
    ET.SubElement(transfer, "flightOrigin").text = booking.find("ArrivalAirportFrom").text if booking.find("ArrivalAirportFrom") is not None else "N/A"
    ET.SubElement(transfer, "flightDestination").text = booking.find("ArrivalAirportTo").text if booking.find("ArrivalAirportTo") is not None else "N/A"

    ET.SubElement(transfer, "serviceCode")
    ET.SubElement(transfer, "voucher").text = booking.get("ref") if booking.get("ref") is not None else "N/A"

    ET.SubElement(transfer, "paxName").text = booking.find("Customer_name").text if booking.find("Customer_name") is not None else "N/A"

    ET.SubElement(transfer, "arrDepCode")
    ET.SubElement(transfer, "arrDepPhysicalArea").text = booking.find("ArrivalLocTo").text if booking.find("ArrivalLocTo") is not None else "N/A"

    # **Επεξεργασία του SpecificLocation ώστε να πάρουμε μόνο το όνομα του ξενοδοχείου**
    if booking.find("SpecificLocation") is not None:
        hotel_name = booking.find("SpecificLocation").text.split(",")[0]  # Παίρνει μόνο το όνομα
        hotel_name = html.unescape(hotel_name)  # Αποκωδικοποιεί χαρακτήρες HTML
    else:
        hotel_name = "N/A"

    # Χρησιμοποιούμε `ET.SubElement` κανονικά αλλά διασφαλίζουμε ότι η έξοδος δεν θα κωδικοποιηθεί
    arr_dep_name = ET.SubElement(transfer, "arrDepName")
    arr_dep_name.text = hotel_name

    ET.SubElement(transfer, "arrOrder")
    ET.SubElement(transfer, "areaOrder")

    ET.SubElement(transfer, "paxADT").text = booking.find("Adults").text if booking.find("Adults") is not None else "N/A"
    ET.SubElement(transfer, "paxCHD").text = booking.find("Children").text if booking.find("Children") is not None else "N/A"
    ET.SubElement(transfer, "CHD_AGES")
    ET.SubElement(transfer, "paxINF").text = booking.find("Infants").text if booking.find("Infants") is not None else "N/A"

    ET.SubElement(transfer, "vehicle").text = booking.find("Transportation_Unit").text if booking.find("Transportation_Unit") is not None else "N/A"

    ET.SubElement(transfer, "rep")
    ET.SubElement(transfer, "remarks")

    ET.SubElement(transfer, "pickupDate").text = booking.find("DepartureDate").text if booking.find("DepartureDate") is not None else "N/A"
    ET.SubElement(transfer, "pickupTime").text = booking.find("DepartureTime").text if booking.find("DepartureTime") is not None else "N/A"

    ET.SubElement(transfer, "observations")

    # **Αντί να χρησιμοποιήσουμε `tree.write()`, γράφουμε χειροκίνητα**
    output_xml = "converted.xml"
    xml_string = ET.tostring(transfers, encoding="unicode", short_empty_elements=False)  # Αποτρέπει αυτοκλειόμενα tags
    xml_string = html.unescape(xml_string)  # Καθαρίζει τα escapes όπως `&amp;`

    with open(output_xml, "w", encoding="utf-8") as f:
        f.write(xml_string)

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
