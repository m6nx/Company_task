from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Company, Owner
from . import db
from datetime import datetime
import time

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    query = request.args.get('query', '').strip()
    companies = []

    if query:
        company_results = Company.query.filter(
            (Company.name.ilike(f"%{query}%")) |
            (Company.registration_code.ilike(f"%{query}%"))).all()

        owner_results = Owner.query.filter(
            (Owner.first_name.ilike(f"%{query}%")) |
            (Owner.last_name.ilike(f"%{query}%")) |
            (Owner.personal_id.ilike(f"%{query}%"))).all()

        company_ids = {company.id for company in company_results}
        
        for owner in owner_results:
            company_ids.add(owner.company_id)

        companies = Company.query.filter(Company.id.in_(company_ids)).all()

    return render_template("home_page.html", companies=companies, query=query)

@views.route('/establish', methods=['GET', 'POST'])
def establish_company():
    if request.method == 'POST':
        name = request.form.get('name')
        registration_code = request.form.get('registration_code')
        foundation_date_str = request.form.get('foundation_date')
        capital = int(request.form.get('capital'))

        try:
            foundation_date = datetime.strptime(foundation_date_str, '%Y-%m-%d').date()

            new_company = Company(
                name=name,
                registration_code=registration_code,
                foundation_date=foundation_date,
                capital=capital
            )
            db.session.add(new_company)
            db.session.flush()
    
            owner_types = request.form.getlist('owner_type[]')
            first_names= request.form.getlist('first_name[]')
            last_names = request.form.getlist('last_name[]')
            personal_ids = request.form.getlist('personal_id[]')
            share_amounts = request.form.getlist('share_amount[]')

            total_shares = 0
            for i in range(len(first_names)):
                total_shares += int(share_amounts[i])
                new_owner = Owner(
                    owner_type=owner_types[i],
                    first_name=first_names[i],
                    last_name=last_names[i],
                    personal_id=personal_ids[i],
                    share_amount=int(share_amounts[i]),
                    company_id=new_company.id
                )
                db.session.add(new_owner) 

            if total_shares != capital:
                raise ValueError("Owner(s) capital must equal to company's total capital.")         

            db.session.commit()
            print(f"Total shares: {total_shares}")
            flash("Company established successfully!", category='success')
            time.sleep(1)

            return redirect(url_for('views.data_view'))

        except ValueError as e:
            db.session.rollback()
            flash(e, category='error')
        except Exception as e:
            db.session.rollback()
            flash(f"Unexpected error: {e}", category='error')

    return render_template('establishment.html')

@views.route('/data_view', methods=['GET'])
def data_view():
    company_id = request.args.get('company_id')
    company = Company.query.filter_by(id=company_id).first()

    if company_id:
        company = Company.query.filter_by(id=company_id).first()
    else:
        company = Company.query.order_by(Company.id.desc()).first()

    return render_template("data_view.html", companies=[company])
