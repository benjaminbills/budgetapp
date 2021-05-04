from flask import render_template, request, redirect, url_for, flash
from . import main
from flask_login import login_required, current_user
from .. import db
from .forms import ExpenseForm
from ..models import Expense
from sqlalchemy import desc


@main.route("/")
def index():
    """
    View root page function that returns the index page and its data
    """
    return render_template(
        "index.html"
    )


@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    expenses_list = []
    total_expenses = 0
    expenses = Expense.query.order_by(desc(Expense.date))
    for expense in expenses:
        expenses_list.append(expense.ammount)
        total_expenses = sum(expenses_list)
    print(total_expenses)
    form = ExpenseForm()
    if form.validate_on_submit():
        description = form.description.data
        category = form.category.data
        ammount = form.ammount.data
        date = form.date.data
        user_id = current_user._get_current_object().id
        new_expense = Expense(description=description,category=category,ammount=ammount,date=date, user_id=user_id)
        new_expense.save_expense()
        return redirect(url_for('.dashboard'))
    return render_template('user_dashboard.html', form=form, expenses=expenses)

@main.route('/expense/delete/<int:id>')
@login_required
def delete_expense(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('.dashboard'))