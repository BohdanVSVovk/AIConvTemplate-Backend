from flask import (
    Blueprint, render_template, request
)

bp = Blueprint('file_api', __name__)

@bp.route('/file-processing', methods=['GET', 'POST'])
def index():
    data = request.get_json()

    return {
        data['id']
    }
