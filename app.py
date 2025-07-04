from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import csv
import io

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    mode = request.form.get('mode_toggle')
    country_code = request.form.get('country_code', '').strip()
    contact_name = request.form.get('contact_name', '').strip()
    file = request.files.get('csv_file')

    if not file:
        flash("No file uploaded.")
        return redirect(url_for('index'))

    # Limit file size (e.g., 2MB)
    file.seek(0, io.SEEK_END)
    if file.tell() > 2 * 1024 * 1024:
        flash("File too large. Please upload a file smaller than 2MB.")
        return redirect(url_for('index'))
    file.seek(0)

    try:
        content = file.stream.read()
        # Handle BOM if present
        if content.startswith(b'\xef\xbb\xbf'):
            content = content[3:]
        csvfile = io.StringIO(content.decode("utf-8"))
    except Exception:
        flash("Could not decode CSV file. Please ensure it is UTF-8 encoded.")
        return redirect(url_for('index'))

    try:
        reader = csv.DictReader(csvfile)
        # Normalize headers (strip whitespace)
        reader.fieldnames = [h.strip() for h in reader.fieldnames] if reader.fieldnames else []
        contacts = list(reader)
    except Exception:
        flash("Could not read CSV file. Please check the file format.")
        return redirect(url_for('index'))

    if not contacts:
        flash("CSV file is empty or invalid.")
        return redirect(url_for('index'))

    vcf_lines = []

    if mode == "single":
        phone_keys = ['Phone', 'phone', 'Number', 'number']
        found_phone = any(any(k in row for k in phone_keys) for row in contacts)
        if not found_phone:
            flash("No phone number column found in your CSV.")
            return redirect(url_for('index'))
        for row in contacts:
            phone = next((row.get(k) for k in phone_keys if row.get(k)), None)
            if phone and phone.strip():
                vcf_lines.append(
                    f"BEGIN:VCARD\nVERSION:3.0\nFN:{contact_name}\nTEL;TYPE=CELL:{(country_code if country_code else '')}{phone.strip()}\nEND:VCARD"
                )
    elif mode == "csv":
        name_keys = ['Name', 'name', 'First Name', 'first_name']
        surname_keys = ['Surname', 'surname', 'Last Name', 'last_name']
        phone_keys = ['Phone', 'phone', 'Number', 'number']
        email_keys = ['Email', 'email']

        found_any = False
        for row in contacts:
            name = next((row.get(k) for k in name_keys if row.get(k)), '')
            surname = next((row.get(k) for k in surname_keys if row.get(k)), '')
            phone = next((row.get(k) for k in phone_keys if row.get(k)), '')
            email = next((row.get(k) for k in email_keys if row.get(k)), '')

            # Filter out empty rows
            if not any([name, surname, phone, email]):
                continue

            found_any = True

            # Email only
            if email and not (name or surname or phone):
                vcf_lines.append(
                    f"BEGIN:VCARD\nVERSION:3.0\nEMAIL;TYPE=INTERNET:{email.strip()}\nEND:VCARD"
                )
            # Name and surname only
            elif (name or surname) and not (phone or email):
                full_name = f"{name} {surname}".strip()
                vcf_lines.append(
                    f"BEGIN:VCARD\nVERSION:3.0\nFN:{full_name}\nEND:VCARD"
                )
            # Name, surname, phone, and/or email
            else:
                full_name = f"{name} {surname}".strip() if (name or surname) else ''
                vcard = "BEGIN:VCARD\nVERSION:3.0\n"
                if full_name:
                    vcard += f"FN:{full_name}\n"
                if phone:
                    vcard += f"TEL;TYPE=CELL:{(country_code if country_code else '')}{phone.strip()}\n"
                if email:
                    vcard += f"EMAIL;TYPE=INTERNET:{email.strip()}\n"
                vcard += "END:VCARD"
                vcf_lines.append(vcard)

        if not found_any:
            flash("No valid contact columns found in your CSV.")
            return redirect(url_for('index'))

    if not vcf_lines:
        flash("No valid contacts found in your CSV.")
        return redirect(url_for('index'))

    vcf_content = "\n".join(vcf_lines)
    vcf_io = io.BytesIO()
    vcf_io.write(vcf_content.encode('utf-8'))
    vcf_io.seek(0)
    return send_file(
        vcf_io,
        mimetype='text/vcard',
        as_attachment=True,
        download_name='contacts.vcf'
    )

if __name__ == '__main__':
    app.run(debug=True)