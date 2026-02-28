from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db, TenderFile, ProjectRecord, Personnel, Supplier, Equipment
from config import SQLALCHEMY_DATABASE_URI, UPLOAD_FOLDER
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)
db.init_app(app)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

with app.app_context():
    db.create_all()

@app.route('/api/tender-files', methods=['GET', 'POST'])
def handle_tender_files():
    if request.method == 'GET':
        items = TenderFile.query.order_by(TenderFile.created_at.desc()).all()
        return jsonify([{
            'id': item.id,
            'project_name': item.project_name,
            'project_type': item.project_type,
            'region': item.region,
            'owner_name': item.owner_name,
            'tender_date': item.tender_date,
            'tender_file_path': item.tender_file_path,
            'bid_file_path': item.bid_file_path,
            'description': item.description,
            'created_at': item.created_at.strftime('%Y-%m-%d %H:%M') if item.created_at else ''
        } for item in items])
    else:
        data = request.json
        item = TenderFile(
            project_name=data.get('project_name'),
            project_type=data.get('project_type'),
            region=data.get('region'),
            owner_name=data.get('owner_name'),
            tender_date=data.get('tender_date'),
            tender_file_path=data.get('tender_file_path'),
            bid_file_path=data.get('bid_file_path'),
            description=data.get('description')
        )
        db.session.add(item)
        db.session.commit()
        return jsonify({'id': item.id, 'message': '创建成功'}), 201

@app.route('/api/tender-files/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_tender_file(id):
    item = TenderFile.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': item.id,
            'project_name': item.project_name,
            'project_type': item.project_type,
            'region': item.region,
            'owner_name': item.owner_name,
            'tender_date': item.tender_date,
            'tender_file_path': item.tender_file_path,
            'bid_file_path': item.bid_file_path,
            'description': item.description
        })
    elif request.method == 'PUT':
        data = request.json
        item.project_name = data.get('project_name', item.project_name)
        item.project_type = data.get('project_type', item.project_type)
        item.region = data.get('region', item.region)
        item.owner_name = data.get('owner_name', item.owner_name)
        item.tender_date = data.get('tender_date', item.tender_date)
        item.tender_file_path = data.get('tender_file_path', item.tender_file_path)
        item.bid_file_path = data.get('bid_file_path', item.bid_file_path)
        item.description = data.get('description', item.description)
        db.session.commit()
        return jsonify({'message': '更新成功'})
    else:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': '删除成功'})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'filename': filename, 'path': os.path.join(app.config['UPLOAD_FOLDER'], filename)})

@app.route('/api/uploads/<filename>')
def download_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/project-records', methods=['GET', 'POST'])
def handle_project_records():
    if request.method == 'GET':
        items = ProjectRecord.query.order_by(ProjectRecord.created_at.desc()).all()
        return jsonify([{
            'id': item.id,
            'project_name': item.project_name,
            'scale': item.scale,
            'industry': item.industry,
            'completion_date': item.completion_date,
            'contract_value': item.contract_value,
            'description': item.description,
            'created_at': item.created_at.strftime('%Y-%m-%d %H:%M') if item.created_at else ''
        } for item in items])
    else:
        data = request.json
        item = ProjectRecord(
            project_name=data.get('project_name'),
            scale=data.get('scale'),
            industry=data.get('industry'),
            completion_date=data.get('completion_date'),
            contract_value=data.get('contract_value'),
            description=data.get('description')
        )
        db.session.add(item)
        db.session.commit()
        return jsonify({'id': item.id, 'message': '创建成功'}), 201

@app.route('/api/project-records/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_project_record(id):
    item = ProjectRecord.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': item.id,
            'project_name': item.project_name,
            'scale': item.scale,
            'industry': item.industry,
            'completion_date': item.completion_date,
            'contract_value': item.contract_value,
            'description': item.description
        })
    elif request.method == 'PUT':
        data = request.json
        item.project_name = data.get('project_name', item.project_name)
        item.scale = data.get('scale', item.scale)
        item.industry = data.get('industry', item.industry)
        item.completion_date = data.get('completion_date', item.completion_date)
        item.contract_value = data.get('contract_value', item.contract_value)
        item.description = data.get('description', item.description)
        db.session.commit()
        return jsonify({'message': '更新成功'})
    else:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': '删除成功'})

@app.route('/api/personnel', methods=['GET', 'POST'])
def handle_personnel():
    if request.method == 'GET':
        items = Personnel.query.order_by(Personnel.created_at.desc()).all()
        return jsonify([{
            'id': item.id,
            'name': item.name,
            'company': item.company,
            'position': item.position,
            'qualification': item.qualification,
            'specialty': item.specialty,
            'phone': item.phone,
            'email': item.email,
            'experience': item.experience,
            'created_at': item.created_at.strftime('%Y-%m-%d %H:%M') if item.created_at else ''
        } for item in items])
    else:
        data = request.json
        item = Personnel(
            name=data.get('name'),
            company=data.get('company'),
            position=data.get('position'),
            qualification=data.get('qualification'),
            specialty=data.get('specialty'),
            phone=data.get('phone'),
            email=data.get('email'),
            experience=data.get('experience')
        )
        db.session.add(item)
        db.session.commit()
        return jsonify({'id': item.id, 'message': '创建成功'}), 201

@app.route('/api/personnel/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_person(id):
    item = Personnel.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': item.id,
            'name': item.name,
            'company': item.company,
            'position': item.position,
            'qualification': item.qualification,
            'specialty': item.specialty,
            'phone': item.phone,
            'email': item.email,
            'experience': item.experience
        })
    elif request.method == 'PUT':
        data = request.json
        item.name = data.get('name', item.name)
        item.company = data.get('company', item.company)
        item.position = data.get('position', item.position)
        item.qualification = data.get('qualification', item.qualification)
        item.specialty = data.get('specialty', item.specialty)
        item.phone = data.get('phone', item.phone)
        item.email = data.get('email', item.email)
        item.experience = data.get('experience', item.experience)
        db.session.commit()
        return jsonify({'message': '更新成功'})
    else:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': '删除成功'})

@app.route('/api/suppliers', methods=['GET', 'POST'])
def handle_suppliers():
    if request.method == 'GET':
        items = Supplier.query.order_by(Supplier.created_at.desc()).all()
        return jsonify([{
            'id': item.id,
            'name': item.name,
            'contact_person': item.contact_person,
            'phone': item.phone,
            'email': item.email,
            'address': item.address,
            'product_specs': item.product_specs,
            'certifications': item.certifications,
            'cooperation_history': item.cooperation_history,
            'created_at': item.created_at.strftime('%Y-%m-%d %H:%M') if item.created_at else ''
        } for item in items])
    else:
        data = request.json
        item = Supplier(
            name=data.get('name'),
            contact_person=data.get('contact_person'),
            phone=data.get('phone'),
            email=data.get('email'),
            address=data.get('address'),
            product_specs=data.get('product_specs'),
            certifications=data.get('certifications'),
            cooperation_history=data.get('cooperation_history')
        )
        db.session.add(item)
        db.session.commit()
        return jsonify({'id': item.id, 'message': '创建成功'}), 201

@app.route('/api/suppliers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_supplier(id):
    item = Supplier.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': item.id,
            'name': item.name,
            'contact_person': item.contact_person,
            'phone': item.phone,
            'email': item.email,
            'address': item.address,
            'product_specs': item.product_specs,
            'certifications': item.certifications,
            'cooperation_history': item.cooperation_history
        })
    elif request.method == 'PUT':
        data = request.json
        item.name = data.get('name', item.name)
        item.contact_person = data.get('contact_person', item.contact_person)
        item.phone = data.get('phone', item.phone)
        item.email = data.get('email', item.email)
        item.address = data.get('address', item.address)
        item.product_specs = data.get('product_specs', item.product_specs)
        item.certifications = data.get('certifications', item.certifications)
        item.cooperation_history = data.get('cooperation_history', item.cooperation_history)
        db.session.commit()
        return jsonify({'message': '更新成功'})
    else:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': '删除成功'})

@app.route('/api/equipment', methods=['GET', 'POST'])
def handle_equipment():
    if request.method == 'GET':
        items = Equipment.query.order_by(Equipment.created_at.desc()).all()
        return jsonify([{
            'id': item.id,
            'name': item.name,
            'model': item.model,
            'brand': item.brand,
            'tech_params': item.tech_params,
            'performance': item.performance,
            'supplier_id': item.supplier_id,
            'supplier_name': item.supplier.name if item.supplier else '',
            'price': item.price,
            'created_at': item.created_at.strftime('%Y-%m-%d %H:%M') if item.created_at else ''
        } for item in items])
    else:
        data = request.json
        item = Equipment(
            name=data.get('name'),
            model=data.get('model'),
            brand=data.get('brand'),
            tech_params=data.get('tech_params'),
            performance=data.get('performance'),
            supplier_id=data.get('supplier_id'),
            price=data.get('price')
        )
        db.session.add(item)
        db.session.commit()
        return jsonify({'id': item.id, 'message': '创建成功'}), 201

@app.route('/api/equipment/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_equipment_item(id):
    item = Equipment.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': item.id,
            'name': item.name,
            'model': item.model,
            'brand': item.brand,
            'tech_params': item.tech_params,
            'performance': item.performance,
            'supplier_id': item.supplier_id,
            'price': item.price
        })
    elif request.method == 'PUT':
        data = request.json
        item.name = data.get('name', item.name)
        item.model = data.get('model', item.model)
        item.brand = data.get('brand', item.brand)
        item.tech_params = data.get('tech_params', item.tech_params)
        item.performance = data.get('performance', item.performance)
        item.supplier_id = data.get('supplier_id', item.supplier_id)
        item.price = data.get('price', item.price)
        db.session.commit()
        return jsonify({'message': '更新成功'})
    else:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': '删除成功'})

@app.route('/api/search', methods=['GET'])
def global_search():
    keyword = request.args.get('keyword', '')
    category = request.args.get('category', 'all')
    results = {}
    
    if category in ['all', 'tender']:
        tender_results = TenderFile.query.filter(
            db.or_(
                TenderFile.project_name.contains(keyword),
                TenderFile.project_type.contains(keyword),
                TenderFile.region.contains(keyword),
                TenderFile.owner_name.contains(keyword),
                TenderFile.description.contains(keyword)
            )
        ).all()
        results['tender_files'] = [{
            'id': item.id,
            'project_name': item.project_name,
            'project_type': item.project_type,
            'region': item.region,
            'owner_name': item.owner_name,
            'tender_date': item.tender_date,
            'description': item.description
        } for item in tender_results]
    
    if category in ['all', 'project']:
        project_results = ProjectRecord.query.filter(
            db.or_(
                ProjectRecord.project_name.contains(keyword),
                ProjectRecord.scale.contains(keyword),
                ProjectRecord.industry.contains(keyword),
                ProjectRecord.description.contains(keyword)
            )
        ).all()
        results['project_records'] = [{
            'id': item.id,
            'project_name': item.project_name,
            'scale': item.scale,
            'industry': item.industry,
            'completion_date': item.completion_date,
            'description': item.description
        } for item in project_results]
    
    if category in ['all', 'personnel']:
        personnel_results = Personnel.query.filter(
            db.or_(
                Personnel.name.contains(keyword),
                Personnel.company.contains(keyword),
                Personnel.qualification.contains(keyword),
                Personnel.specialty.contains(keyword),
                Personnel.experience.contains(keyword)
            )
        ).all()
        results['personnel'] = [{
            'id': item.id,
            'name': item.name,
            'company': item.company,
            'position': item.position,
            'qualification': item.qualification,
            'specialty': item.specialty
        } for item in personnel_results]
    
    if category in ['all', 'supplier']:
        supplier_results = Supplier.query.filter(
            db.or_(
                Supplier.name.contains(keyword),
                Supplier.product_specs.contains(keyword),
                Supplier.certifications.contains(keyword),
                Supplier.cooperation_history.contains(keyword)
            )
        ).all()
        results['suppliers'] = [{
            'id': item.id,
            'name': item.name,
            'contact_person': item.contact_person,
            'phone': item.phone,
            'product_specs': item.product_specs,
            'certifications': item.certifications
        } for item in supplier_results]
    
    if category in ['all', 'equipment']:
        equipment_results = Equipment.query.filter(
            db.or_(
                Equipment.name.contains(keyword),
                Equipment.model.contains(keyword),
                Equipment.brand.contains(keyword),
                Equipment.tech_params.contains(keyword),
                Equipment.performance.contains(keyword)
            )
        ).all()
        results['equipment'] = [{
            'id': item.id,
            'name': item.name,
            'model': item.model,
            'brand': item.brand,
            'tech_params': item.tech_params,
            'price': item.price
        } for item in equipment_results]
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
