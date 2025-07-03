def convert_csv_to_vcf(input_file, username, country_code):
    import csv

    contacts = []

    with open(input_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for number in row:
                number = number.strip()
                if number.isdigit():
                    if number.startswith("0"):
                        number = number[1:]
                    formatted_number = f"{country_code}{number}"
                    contacts.append({"Name": username, "Phone": formatted_number})

    vcf_output = []
    for contact in contacts:
        name = contact['Name']
        phone = contact['Phone']
        vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL;TYPE=CELL:{phone}
END:VCARD
"""
        vcf_output.append(vcard)

    return ''.join(vcf_output)