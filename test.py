import unittest
import datetime
from app import User, Payment

class UserTest(unittest.TestCase):
    def test_register(self):
        # 测试用户注册功能

        # 新建用户
        user = User(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
            # trial_max_count=100,
            # trial_max_chars=1000
        )
        user.save()

        # 检查用户是否成功创建
        self.assertIsNotNone(user.id)

        # 根据用户名查找用户
        found_user = User.find_by_username('testuser')
        self.assertEqual(user.username, found_user.username)
        self.assertEqual(user.password, found_user.password)
        self.assertEqual(user.email, found_user.email)
        # self.assertEqual(user.trial_max_count, found_user.trial_max_count)
        # self.assertEqual(user.trial_max_chars, found_user.trial_max_chars)

    def test_update_payment_info(self):
        # 测试更新用户支付信息

        # 新建用户和支付记录
        user = User(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
            # trial_max_count=100,
            # trial_max_chars=1000
        )
        user.save()

        payment = Payment(
            user_id=user.id,
            payment_type='credit_card',
            payment_amount=100
        )
        payment.save()

        # 更新用户支付信息
        user.update_payment_info(payment)

        # 检查用户试用信息是否更新成功
        self.assertEqual(User.trial_end_date().date(), user.trial_end_date.date())
        # self.assertIsNone(user.trial_max_count)
        # self.assertIsNone(user.trial_max_chars)

        # 根据用户 ID 查找支付记录
        found_payment = Payment.find_by_user_id(user.id)
        self.assertIsNotNone(found_payment)
        self.assertEqual(payment.payment_type, found_payment.payment_type)
        self.assertEqual(payment.payment_amount, found_payment.payment_amount)

class PaymentTest(unittest.TestCase):
    def test_save_and_find_by_id(self):
        # 测试保存和根据 ID 查找支付记录

        # 新建支付记录
        payment = Payment(
            user_id=1,
            payment_type='credit_card',
            payment_amount=100
        )
        payment.save()

        # 根据 ID 查找支付记录
        found_payment = Payment.find_by_id(payment.id)
        self.assertEqual(payment.payment_type, found_payment.payment_type)
        self.assertEqual(payment.payment_amount, found_payment.payment_amount)

if __name__ == '__main__':
    unittest.main()
