import io
import requests

from flask import Flask, Response
from flask_restful import Resource, reqparse
from PyPDF2 import PdfFileMerger

parser = reqparse.RequestParser()
parser.add_argument('pdf_urls', type=str, required=True, location='form', action='append')

class MergeResource(Resource):
    def post(self):
        merger = PdfFileMerger()

        args = parser.parse_args()

        for pdf_url in args['pdf_urls']:
            try:
                pdf_response = requests.get(pdf_url)
                pdf_bytes = pdf_response.content
                merger.append(fileobj=io.BytesIO(pdf_bytes))
            except Exception:
                continue

        combined_pdf = io.BytesIO()
        merger.write(combined_pdf)
        combined_pdf.seek(0)

        response = Response(combined_pdf, mimetype='application/pdf')
        response.headers['Content-Disposition'] = "attachment; filename=%s.pdf" % 'pdf_name'

        return response
