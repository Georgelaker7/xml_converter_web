from flask import Flask, request, render_template, send_file
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

def convert_xml(input_xml):
    root = ET.fromstring(input_xml)
    booking = root.find(".//Booking")

    transfers = ET.Element("transfers", MessageType="Request", FechaCreacion=booking.find("Booking_date").text, Count="1")
    transfer = ET.SubElement(transfers, "transfer")

    ET.SubElement(transfer, "result")
    ET.SubElement(transfer, "client").text = "HER"
    ET.SubElement(transfer, "ttoo").text = booking.find("Company").text
    ET.SubElement(transfer, "flightNumber").text = booking.find("ArrivalFlightNumber").text
    ET.SubElement(transfer, "flightDate").text = booking.find("ArrivalDate").text
    ET.SubElement(transfer, "paxName").text = booking.find("Customer_name").text
    ET.SubElement(transfer, "pickupDate").text = booking.find("DepartureDate").text

    return ET.tostring(transfers, encoding="unicode")

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded"

        file = request.files["file"]
        if file.filename == "":
            return "No file selected"

        input_xml = file.read().decode("utf-8")
        converted_xml = convert_xml(input_xml)

        output_path = "output.xml"
        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write(converted_xml)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
