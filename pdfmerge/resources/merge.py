import io
import requests

from flask import jsonify, Response
from flask_restful import Resource, reqparse
from PyPDF2 import PdfFileMerger

parser = reqparse.RequestParser()
parser.add_argument('pdf_urls', type=str, required=True, location='form', action='append')


class MergeResource(Resource):
    def post(self):
        args = parser.parse_args()

        merger = PdfFileMerger()

        failed_urls = []
        for pdf_url in args['pdf_urls']:
            if pdf_url == "":
                continue
            try:
                pdf_response = requests.get(pdf_url)
                pdf_bytes = pdf_response.content
                merger.append(fileobj=io.BytesIO(pdf_bytes))
            except Exception:
                failed_urls.append(pdf_url)
                continue

        if len(failed_urls) > 0:
            response = jsonify({'failed_urls': failed_urls})
            response.status_code = 400

            return response

        combined_pdf = io.BytesIO()
        merger.write(combined_pdf)
        combined_pdf.seek(0)

        response = Response(combined_pdf, mimetype='application/pdf')
        response.headers['Content-Disposition'] = "attachment; filename=%s.pdf" % 'pdf_name'

        return response
