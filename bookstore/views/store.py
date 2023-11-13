import re
from typing_extensions import Self
from flask import Flask, request, template_rendered, Blueprint
from flask import url_for, redirect, flash
from flask import render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from numpy import identity, product
import random, string
from sqlalchemy import null
from link import *
import math
from base64 import b64encode
from api.sql import Member, Order_List, Product, Record, Cart
from api.feature import Feature
from api.task import Task
from api.comment import Comment
from api.filter import Filter
from api.user import TrackUser

store = Blueprint('bookstore', __name__, template_folder='../templates')

@store.route('/', methods=['GET', 'POST'])
@login_required
def search_filter():
    my_filter = Filter()
    action = request.args.get('action', None)
    current_issue_list = request.args.get('issue_list', [])
    if action == "get_all_member":
        member_list = my_filter.get_all_member()
        return render_template('viewissue.html', member_list = member_list,
                               issue_list = current_issue_list)    

@login_required
@store.route('/viewissue')
def viewissue():
    """Shows issue details per provided id; otherwise show issue list per filter.

    issue = task. My bad.
    """
    my_issue = Issue()
    issue_id = request.args.get('id', None)
    user_filter = request.args.get('filter', None)
    feature_id = request.args.get('feature_id', None)
    keyword = request.arg.get('keyword', None)
    my_feature = Feature(feature_id, keyword)
    issue_items = ['taskId', 'status', 'description', 'taskOwner', 'title',
                  'dueDate', 'assigner', 'creator', 'assigntime']
    feature_items = ['featureId','creatorId','maintainerId','title',
                     'description','creator','maintainer']

    if issue_id is not None:
        target_data = my_issue.show_issue_detail(taskid)
        # taskOwner, assigner, and creator are the ids of those people
        # ownerName, assignerName, and creatorName are the names
        data_items = ['taskId', 'status', 'description', 'taskOwner', 'title',
                      'dueDate', 'assigner', 'creator', 'assigntime',
                      'ownerName', 'assignerName', 'creatorName']
        target_issue = dict(zip(data_items, target_data))

        # get comments
        target_issue['commentList'] = []
        issue_comment = Comment(issue_id)
        comment_items = ['commentId', 'commenterId', 'taskId', 'content',
                         'commentTime', 'lastUpdateTime', 'commenterName']
        for comment_entry in issue_comment.get_all_comments():
            target_issue['commentList'].append(dict(zip(comment_items,
                                                        comment_data)))
        return render_template('issuedetail.html', issue_detail = target_issue)

    # if feature is specified, get feature details and the list of issues
    if feature_id is not None:
        target_data = Feature.get_details()
        target_feature = dict(zip(feature_items, target_data))

        # list tasks related to feature
        task_list = []
        for task_data in my_feature.list_tasks():
            task_list.append(dict(zip(issue_items, task_data)))
        return render_template('featuredetail.html',
                               feature_detail = feature_detail,
                               issue_list = task_list)
    # list features
    feature_list = []
    for feature_data in my_feature.list_features():
        feature_list.append(dict(zip(feature_items, feature_data)))
    return render_tempate('viewfeature.html',
                          feature_list = feature_list)

    # list issues
    filtered_issue_data = my_issue.list_issue(user_filter)
    filtered_issue_list = []
    for issue_data in filtered_issue_data:
        filtered_issue_list.append(dict(zip(issue_items, issue_data)))
    return render_template('viewissue.html',
                           issue_list = filtered_issue_list)

@login_required
def bookstore():
    result = Product.count()
    count = math.ceil(result[0]/9)
    flag = 0
    
    if request.method == 'GET':
        if(current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('manager.home'))

    if 'keyword' in request.args and 'page' in request.args:
        total = 0
        single = 1
        page = int(request.args['page'])
        start = (page - 1) * 9
        end = page * 9
        search = request.values.get('keyword')
        keyword = search
        
        cursor.prepare('SELECT * FROM PRODUCT WHERE PNAME LIKE :search')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        book_row = cursor.fetchall()
        book_data = []
        final_data = []
        
        for i in book_row:
            book = {
                '商品編號': i[0],
                '商品名稱': i[1],
                '商品價格': i[2]
            }
            book_data.append(book)
            total = total + 1
        
        if(len(book_data) < end):
            end = len(book_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(book_data[j])
            
        count = math.ceil(total/9)
        
        return render_template('bookstore.html', single=single, keyword=search, book_data=book_data, user=current_user.name, page=1, flag=flag, count=count)    

    
    elif 'pid' in request.args:
        pid = request.args['pid']
        data = Product.get_product(pid)
        
        pname = data[1]
        price = data[2]
        category = data[3]
        description = data[4]
        image = 'sdg.jpg'
        
        product = {
            '商品編號': pid,
            '商品名稱': pname,
            '單價': price,
            '類別': category,
            '商品敘述': description,
            '商品圖片': image
        }

        return render_template('product.html', data = product, user=current_user.name)
    
    elif 'page' in request.args:
        page = int(request.args['page'])
        start = (page - 1) * 9
        end = page * 9
        
        book_row = Product.get_all_product()
        book_data = []
        final_data = []
        
        for i in book_row:
            book = {
                '商品編號': i[0],
                '商品名稱': i[1],
                '商品價格': i[2]
            }
            book_data.append(book)
            
        if(len(book_data) < end):
            end = len(book_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(book_data[j])
        
        return render_template('bookstore.html', book_data=final_data, user=current_user.name, page=page, flag=flag, count=count)    
    
    elif 'keyword' in request.args:
        single = 1
        search = request.values.get('keyword')
        keyword = search
        cursor.prepare('SELECT * FROM PRODUCT WHERE PNAME LIKE :search')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        book_row = cursor.fetchall()
        book_data = []
        total = 0
        
        for i in book_row:
            book = {
                '商品編號': i[0],
                '商品名稱': i[1],
                '商品價格': i[2]
            }

            book_data.append(book)
            total = total + 1
            
        if(len(book_data) < 9):
            flag = 1
        
        count = math.ceil(total/9)    
        
        return render_template('bookstore.html', keyword=search, single=single, book_data=book_data, user=current_user.name, page=1, flag=flag, count=count)    
    
    else:
        book_row = Product.get_all_product()
        book_data = []
        temp = 0
        for i in book_row:
            book = {
                '商品編號': i[0],
                '商品名稱': i[1],
                '商品價格': i[2],
            }
            if len(book_data) < 9:
                book_data.append(book)
        
        return render_template('bookstore.html', book_data=book_data, user=current_user.name, page=1, flag=flag, count=count)

# 會員購物車
@store.route('/cart', methods=['GET', 'POST'])
@login_required # 使用者登入後才可以看
def cart():

    # 以防管理者誤闖
    if request.method == 'GET':
        if( current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('manager.home'))

    # 回傳有 pid 代表要 加商品
    if request.method == 'POST':
        
        if "pid" in request.form :
            data = Cart.get_cart(current_user.id)
            
            if( data == None): #假如購物車裡面沒有他的資料
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                Cart.add_cart(current_user.id, time) # 幫他加一台購物車
                data = Cart.get_cart(current_user.id) 
                
            tno = data[2] # 取得交易編號
            pid = request.values.get('pid') # 使用者想要購買的東西
            # 檢查購物車裡面有沒有商品
            product = Record.check_product(pid, tno)
            # 取得商品價錢
            price = Product.get_product(pid)[2]

            # 如果購物車裡面沒有的話 把他加一個進去
            if(product == None):
                Record.add_product( {'id': tno, 'tno':pid, 'price':price, 'total':price} )
            else:
                # 假如購物車裡面有的話，就多加一個進去
                amount = Record.get_amount(tno, pid)
                total = (amount+1)*int(price)
                Record.update_product({'amount':amount+1, 'tno':tno , 'pid':pid, 'total':total})

        elif "delete" in request.form :
            pid = request.values.get('delete')
            tno = Cart.get_cart(current_user.id)[2]
            
            Member.delete_product(tno, pid)
            product_data = only_cart()
        
        elif "user_edit" in request.form:
            change_order()  
            return redirect(url_for('bookstore.bookstore'))
        
        elif "buy" in request.form:
            change_order()
            return redirect(url_for('bookstore.order'))

        elif "order" in request.form:
            tno = Cart.get_cart(current_user.id)[2]
            total = Record.get_total_money(tno)
            Cart.clear_cart(current_user.id)

            time = str(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            format = 'yyyy/mm/dd hh24:mi:ss'
            Order_List.add_order( {'mid': current_user.id, 'time':time, 'total':total, 'format':format, 'tno':tno} )

            return render_template('complete.html', user=current_user.name)

    product_data = only_cart()
    
    if product_data == 0:
        return render_template('empty.html', user=current_user.name)
    else:
        return render_template('cart.html', data=product_data, user=current_user.name)

@store.route('/order')
def order():
    data = Cart.get_cart(current_user.id)
    tno = data[2]

    product_row = Record.get_record(tno)
    product_data = []

    for i in product_row:
        pname = Product.get_name(i[1])
        product = {
            '商品編號': i[1],
            '商品名稱': pname,
            '商品價格': i[3],
            '數量': i[2]
        }
        product_data.append(product)
    
    total = Record.get_total(tno)[0]

    return render_template('order.html', data=product_data, total=total, user=current_user.name)

@store.route('/orderlist')
def orderlist():
    if "oid" in request.args :
        pass
    
    user_id = current_user.id

    data = Member.get_order(user_id)
    orderlist = []

    for i in data:
        temp = {
            '訂單編號': i[0],
            '訂單總價': i[3],
            '訂單時間': i[2]
        }
        orderlist.append(temp)
    
    orderdetail_row = Order_List.get_orderdetail()
    orderdetail = []

    for j in orderdetail_row:
        temp = {
            '訂單編號': j[0],
            '商品名稱': j[1],
            '商品單價': j[2],
            '訂購數量': j[3]
        }
        orderdetail.append(temp)


    return render_template('orderlist.html', data=orderlist, detail=orderdetail, user=current_user.name)

@store.route('/viewuser')
def viewuser():
    pass

@store.route('/list_table')
def list_table():
    # we use another function for task as it requires filter
    table_class = {
        "task": list_task,
        "issue": list_task,
        "user": TrackUser,
        "feature": Feature
    }
    # to make it case insensitive just in case
    target_table = request.args["target_table"].lower()
    if callable(table_class[target_table]):
        return table_class[target_table](request.args)

    my_table = table_class[target_table]()
    target_data = my_table.get_detail()
    return render_template(my_table.list_page, data = target_data)

def list_task(args: dict):
    # TODO finish filter implementation
    my_filter = args.get("filter", None)
    my_filter = Filter()
    my_table = Task()
    data = my_table.list_item(my_filter)
    return render_template(my_table.list_page, data = data)

@store.route('/show_detail')
def show_detail():
    table_class = {
        "task": Task,
        "issue": Task,
        "user": TrackUser,
        "feature": Feature
    }
    target_table = request.args["target_table"].lower()
    item_id = request.args["id"]
    my_table = table_class[target_table](item_id)
    target_data = my_table.get_detail(item_id)
    return render_template(my_table.detail_page, data = target_data)

@store.route('/create')
def create():
    table_class = {
        "task": Task,
        "issue": Task,
        "user": TrackUser,
        "feature": Feature
    }
    target_table = request.args["target_table"].lower()

def change_order():
    data = Cart.get_cart(current_user.id)
    tno = data[2] # 使用者有購物車了，購物車的交易編號是什麼
    product_row = Record.get_record(data[2])

    for i in product_row:
        
        # i[0]：交易編號 / i[1]：商品編號 / i[2]：數量 / i[3]：價格
        if int(request.form[i[1]]) != i[2]:
            Record.update_product({
                'amount':request.form[i[1]],
                'pid':i[1],
                'tno':tno,
                'total':int(request.form[i[1]])*int(i[3])
            })
            print('change')

    return 0


def only_cart():
    
    count = Cart.check(current_user.id)

    if(count == None):
        return 0
    
    data = Cart.get_cart(current_user.id)
    tno = data[2]
    product_row = Record.get_record(tno)
    product_data = []

    for i in product_row:
        pid = i[1]
        pname = Product.get_name(i[1])
        price = i[3]
        amount = i[2]
        
        product = {
            '商品編號': pid,
            '商品名稱': pname,
            '商品價格': price,
            '數量': amount
        }
        product_data.append(product)
    
    return product_data
