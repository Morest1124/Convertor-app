
# CSV to VCF Web Application

This project is a web application that converts CSV contact numbers to VCF format using Flask. Users can upload a CSV file containing contact numbers, specify a contact name, and provide a country code to generate a VCF file.

## Project Structure

```
csv-to-vcf-webapp
├── app.py                # Main entry point of the web application
├── requirements.txt      # Project dependencies
├── templates
│   └── index.html       # User interface for uploading CSV files
├── static
│   └── style.css        # CSS styles for the web application
├── utils
│   └── converter.py     # Logic for converting CSV to VCF
└── README.md            # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd csv-to-vcf-webapp
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment. You can create one using:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   Start the Flask server by running:
   ```
   python app.py
   ```
   The application will be accessible at `http://127.0.0.1:5000`.

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000`.
2. Use the form to upload your CSV file containing contact numbers.
3. Enter the desired contact name and country code.
4. Submit the form to generate the VCF file.
5. Download the generated VCF file.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
>>>>>>> b7e14d0 (Prepare for Render deployment)
