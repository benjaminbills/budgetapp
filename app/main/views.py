from flask import render_template, request, redirect, url_for, flash
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
    expenses_date = []
    check_length = 0
    total_expenses = 0
    user = User.query.filter_by(username = username).first()
    expenses = Expense.query.order_by(asc(Expense.date))
    for expense in expenses:
        expenses_list.append(expense.ammount)
        expenses_date.append(expense.date.strftime('%Y-%m-%d'))
        total_expenses = sum(expenses_list)
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
    return render_template('user_dashboard.html', form=form, expenses=expenses, total_expenses=total_expenses, expenses_date=expenses_date, expenses_list=expenses_list,check_length=check_length, user = user, total_amount_left = total_amount_left)

@main.route('/expense/delete/<int:id>')
@login_required
def delete_expense(id, username):
    user = User.query.filter_by(username = username).first()
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
