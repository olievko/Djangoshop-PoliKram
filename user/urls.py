
from django.urls import path

from .views import account_view, registration_form, login_form, logout_func,\
                    user_update, user_password_change, user_password_reset,\
                    user_wishlist_add, user_wishlist_del,\
                    user_orders, user_order_detail, user_comments, user_wishlist, user_deletecomment, email_list_signup
from django.contrib.auth import views as auth_views
from .forms import FormSetPassword, FormChangePassword

# app_name = 'user'

urlpatterns = [
    # USER PROFILE
    path('', account_view, name='user_profile'),
    # USER ACCOUNT
    path('login/', login_form, name='login'),
    path('logout/', logout_func, name='logout'),
    path('signup/', registration_form, name='signup'),
    # USER PASSWORD CHANGE
    # path('password/', user_password_change, name='user_password'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="account/user_password.html", form_class=FormChangePassword), name='user_password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"), name='password_change_done'),
    # USER PASSWORD RESET
    path('password_reset/', user_password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html", form_class=FormSetPassword), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    # USER PROFILE UPDATE
    path('update/', user_update, name='user_update'),
    # USER ORDERS
    path('orders/', user_orders, name='user_orders'),
    path('order-detail/<int:id>', user_order_detail, name='user_order_detail'),
    # USER COMMENT
    path('comments/', user_comments, name='user_comments'),
    path('deletecomment/<int:id>', user_deletecomment, name='user_deletecomment'),
    # USER WHISHLIST
    path('addtowishlist/<int:id>', user_wishlist_add, name='user_wishlist_add'),
    path('deletefromwishlist/<int:id>', user_wishlist_del, name='user_wishlist_del'),
    path('wishlist/', user_wishlist, name='user_wishlist'),
    # USER EMAIL-SIGNUP
    path('email-signup/', email_list_signup, name='email-list-signup'),
]

