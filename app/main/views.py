from flask import render_template, request, redirect, url_for, flash, abort
from . import main
from flask_login import login_required, current_user
from .. import db
from .forms import ExpenseForm, SalaryForm
from ..models import Expense, User
from sqlalchemy import asc


@main.route("/")
def index():
    """
    View root page function that returns the index page and its data
    """
    return render_template(
        "index.html"
    )


@main.route('/dashboard/<username>', methods=['GET', 'POST'])
@login_required
def dashboard(username):
    expenses_list = []
    check_length = 0
    total_expenses = 0
    income_expense = []
    dates_label = []
    over_time_expenditure = []
    category_list = []
    category_amount = []
    category_comparison = db.session.query(db.func.sum(Expense.ammount), Expense.category).group_by(Expense.category).order_by(Expense.category).all()
    dates = db.session.query(db.func.sum(Expense.ammount), Expense.date).group_by(Expense.date).order_by(Expense.date).all()
    print(category_comparison)
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)
    expenses = Expense.query.order_by(asc(Expense.date))
    for amount, date in dates:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_expenditure.append(amount)
    
    
    for expense in expenses:
        expenses_list.append(expense.ammount)
        total_expenses = sum(expenses_list)
    for category in category_comparison:
        category_list.append(category.category)
        category_amount.append(category[0])
    print(category_list)
    print(category_amount)

    total_amount_left = user.salary - total_expenses
    check_length = len(expenses_list)
    form = ExpenseForm()
    if form.validate_on_submit():
        description = form.description.data
        category = form.category.data
        ammount = form.ammount.data
        date = form.date.data
        user_id = current_user._get_current_object().id
        new_expense = Expense(description=description,category=category,ammount=ammount,date=date, user_id=user_id)
        new_expense.save_expense()
        return redirect(url_for('.dashboard', username = user.username))
    return render_template(
        'user_dashboard.html', 
        form=form, 
        expenses=expenses, 
        total_expenses=total_expenses, 
        check_length=check_length, 
        user = user, 
        total_amount_left = total_amount_left,
        over_time_expenditure = over_time_expenditure,
        dates_label = dates_label,
        category_amount = category_amount,
        category_list = category_list
        )

@main.route('/expense/delete/<int:id>/<username>')
@login_required
def delete_expense(id, username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('.dashboard', username=user.username))

@main.route('/update_salary/<username>', methods=['GET', 'POST'])
@login_required
def update_salary(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)
    
    form = SalaryForm()
    if form.validate_on_submit():
        user.salary = form.salary.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.dashboard', username=user.username))
    return render_template('update_salary.html',form =form)
