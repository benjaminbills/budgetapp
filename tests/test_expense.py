import unittest
from app.models import Expense,User
from app import db

class ExpenseModelTest(unittest.TestCase):
      def setUp(self):
              self.user_ben = User(username = 'ben',password = 'ben', email = 'ben@test.com')
              self.new_expense = Expense(
                category='Eat Out',
                description='Dinner with friends',
                ammount = 200,
                date = '2020-10-10',
                user = self.user_ben
                )
      def tearDown(self):
              Expense.query.delete()
              User.query.delete()

      def test_check_instance_variables(self):
                self.assertEquals(self.new_expense.category,'Eat Out')
                self.assertEquals(self.new_expense.description,'Dinner with friends')
                self.assertEquals(self.new_expense.ammount,200)
                self.assertEquals(self.new_expense.date,'2020-10-10')
                self.assertEquals(self.new_expense.user,self.user_ben)
      def test_save_expense(self):
              self.new_expense.save_expense()
              self.assertTrue(len(Expense.query.all())>0)
